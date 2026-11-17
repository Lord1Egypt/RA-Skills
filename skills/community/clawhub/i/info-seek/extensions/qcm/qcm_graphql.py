#!/usr/bin/env python3
"""qcm_graphql.py — QCM MCP GraphQL 适配

提供 GraphQL API（graphql-core 3.x）：
  Query:
    - tools: [ToolInfo!]!          # 工具列表
    - tool(name: String!): ToolInfo # 单工具
    - health: HealthInfo!          # 健康状态
    - stats: StatsInfo!            # 统计（含 rate limit）
  Mutation:
    - callTool(name: String!, arguments: JSON): JSON # 调用工具

用法：
  from graphql import build_schema
  schema = build_schema(tools_provider, call_provider)
  result = schema.execute_sync(query, variable_values=...)
"""
from typing import Any, Dict, List, Callable, Optional

from graphql import (
    GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString,
    GraphQLInt, GraphQLList, GraphQLNonNull, GraphQLBoolean,
    GraphQLFloat, GraphQLScalarType, GraphQLArgument, parse, execute_sync,
    GraphQLError, Undefined,
)
# Subscription
import asyncio
from typing import AsyncIterator

# ============ 自定义 JSON 标量 ============
def _json_serialize(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (dict, list)):
        return value
    return str(value)


def _json_parse_literal(node, _vars=None):
    """递归解析 GraphQL 字面量（对象/列表/标量/变量）"""
    from graphql.language import (
        ObjectValueNode, ListValueNode, StringValueNode, IntValueNode,
        FloatValueNode, BooleanValueNode, NullValueNode, VariableNode,
    )
    if isinstance(node, ObjectValueNode):
        return {f.name.value: _json_parse_literal(f.value, _vars) for f in node.fields}
    if isinstance(node, ListValueNode):
        return [_json_parse_literal(v, _vars) for v in node.values]
    if isinstance(node, StringValueNode):
        return node.value
    if isinstance(node, IntValueNode):
        return int(node.value)
    if isinstance(node, FloatValueNode):
        return float(node.value)
    if isinstance(node, BooleanValueNode):
        return node.value
    if isinstance(node, NullValueNode):
        return None
    if isinstance(node, VariableNode) and _vars:
        return _vars.get(node.name.value)
    return getattr(node, "value", None)


JSONScalar = GraphQLScalarType(
    name="JSON",
    serialize=_json_serialize,
    parse_value=lambda v: v,
    parse_literal=_json_parse_literal,
)

# ============ 类型 ============
ToolInfoType = GraphQLObjectType(
    "ToolInfo",
    lambda: {
        "name": GraphQLField(GraphQLNonNull(GraphQLString)),
        "description": GraphQLField(GraphQLString),
        "inputSchema": GraphQLField(JSONScalar),
    },
)

HealthInfoType = GraphQLObjectType(
    "HealthInfo",
    lambda: {
        "status": GraphQLField(GraphQLNonNull(GraphQLString)),
        "version": GraphQLField(GraphQLString),
        "uptime": GraphQLField(GraphQLFloat),
    },
)

StatsInfoType = GraphQLObjectType(
    "StatsInfo",
    lambda: {
        "requests_total": GraphQLField(GraphQLInt),
        "tools_called": GraphQLField(GraphQLInt),
        "active_sessions": GraphQLField(GraphQLInt),
    },
)


def build_schema(tools_provider: Callable[[], List[Dict]],
                 call_provider: Callable[[str, Dict], Dict],
                 health_provider: Optional[Callable[[], Dict]] = None,
                 stats_provider: Optional[Callable[[], Dict]] = None) -> GraphQLSchema:
    """构建 GraphQL schema

    Args:
        tools_provider: () -> [{"name", "description", "inputSchema"}]
        call_provider: (name, arguments) -> result dict
        health_provider: () -> {"status", "version", "uptime"} (optional)
        stats_provider: () -> {"requests_total", ...} (optional)
    """
    health_provider = health_provider or (lambda: {"status": "ok", "version": "unknown"})
    stats_provider = stats_provider or (lambda: {})

    query = GraphQLObjectType(
        "Query",
        lambda: {
            "tools": GraphQLField(
                GraphQLNonNull(GraphQLList(GraphQLNonNull(ToolInfoType))),
                resolve=lambda _root, _info: tools_provider(),
            ),
            "tool": GraphQLField(
                ToolInfoType,
                args={"name": GraphQLArgument(GraphQLNonNull(GraphQLString))},
                resolve=lambda _root, info, **args: next(
                    (t for t in tools_provider() if t.get("name") == args.get("name")),
                    None,
                ),
            ),
            "health": GraphQLField(
                GraphQLNonNull(HealthInfoType),
                resolve=lambda _root, _info: health_provider(),
            ),
            "stats": GraphQLField(
                GraphQLNonNull(StatsInfoType),
                resolve=lambda _root, _info: stats_provider(),
            ),
        },
    )

    mutation = GraphQLObjectType(
        "Mutation",
        lambda: {
            "callTool": GraphQLField(
                JSONScalar,
                args={
                    "name": GraphQLArgument(GraphQLNonNull(GraphQLString)),
                    "arguments": GraphQLArgument(JSONScalar, default_value={}),
                },
                resolve=lambda _root, info, **args: call_provider(
                    args.get("name"),
                    args.get("arguments") or {},
                ),
            ),
        },
    )

    return GraphQLSchema(query=query, mutation=mutation)


def execute_graphql(schema: GraphQLSchema, query: str,
                    variables: Optional[Dict] = None) -> Dict:
    """执行 GraphQL 查询（返回可 JSON 序列化的 dict）"""
    try:
        parsed = parse(query)
        # 显式 validation（graphql-core 3.x execute_sync 不校验）
        from graphql import validate as _validate
        v_errors = _validate(schema, parsed)
        if v_errors:
            return {
                "errors": [
                    {"message": str(e), "locations": getattr(e, "locations", None)}
                    for e in v_errors
                ]
            }
        result = execute_sync(schema, parsed, variable_values=variables or {})
        if result.errors:
            return {
                "errors": [
                    {"message": str(e), "locations": getattr(e, "locations", None)}
                    for e in result.errors
                ]
            }
        return {"data": result.data}
    except GraphQLError as e:
        return {"errors": [{"message": str(e)}]}
    except Exception as e:
        return {"errors": [{"message": f"GraphQL 执行失败: {e}"}]}


# ============ : GraphQL Subscription（WS 实时推送）============
# 简单事件总线：工具调用事件实时推送
# 订阅者记录所属 loop → 跨线程发布用 call_soon_threadsafe（线程安全）
_event_subscribers: List["_SubscriptionIterator"] = []


def publish_tool_event(event: Dict) -> None:
    """发布工具调用事件（通知所有订阅者 · 跨线程安全）

    - 同线程/同 loop：put_nowait（直通）
    - 跨线程（http 主线程 → 旁路 loop）：call_soon_threadsafe（线程安全唤醒）
    """
    import threading
    for sub in list(_event_subscribers):
        try:
            loop = getattr(sub, "_loop", None)
            if loop is not None and loop.is_running():
                loop_thread = getattr(loop, "_thread_id", None)
                if loop_thread is not None and threading.get_ident() != loop_thread:
                    # 跨线程发布：线程安全唤醒旁路 loop
                    loop.call_soon_threadsafe(sub.q.put_nowait, event)
                else:
                    sub.q.put_nowait(event)
            else:
                sub.q.put_nowait(event)
        except Exception:
            pass


class _SubscriptionIterator:
    """订阅迭代器（修复：创建时立即注册队列，避免 async generator 惰性）

    : 记录 _loop（订阅 resolver 运行于服务器 event loop 内）
    """

    def __init__(self):
        self.q: asyncio.Queue = asyncio.Queue(maxsize=100)
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = None
        self._closed = False
        _event_subscribers.append(self)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._closed:
            raise StopAsyncIteration
        return await self.q.get()

    async def aclose(self):
        if not self._closed:
            self._closed = True
            if self in _event_subscribers:
                _event_subscribers.remove(self)


def subscribe_tool_events() -> AsyncIterator:
    """订阅工具调用事件（立即注册队列 · WS 推送）"""
    return _SubscriptionIterator()


ToolCallEventType = GraphQLObjectType(
    "ToolCallEvent",
    lambda: {
        "tool": GraphQLField(GraphQLNonNull(GraphQLString)),
        "arguments": GraphQLField(JSONScalar),
        "time": GraphQLField(GraphQLString),
    },
)


def build_subscription_schema(subscription_resolver: Callable = None) -> GraphQLObjectType:
    """构建 Subscription 类型（可附加到 schema）"""
    resolver = subscription_resolver or subscribe_tool_events
    return GraphQLObjectType(
        "Subscription",
        lambda: {
            "toolCalled": GraphQLField(
                GraphQLNonNull(ToolCallEventType),
                resolve=lambda event, _info: event,
                subscribe=lambda _root, _info: resolver(),
            ),
        },
    )


if __name__ == "__main__":
    # Demo
    schema = build_schema(
        tools_provider=lambda: [{"name": "demo", "description": "demo tool",
                                 "inputSchema": {"type": "object"}}],
        call_provider=lambda name, args: {"called": name, "args": args},
        health_provider=lambda: {"status": "ok", "version": "demo", "uptime": 1.5},
    )
    r = execute_graphql(schema, "{ health { status version } tools { name } }")
    print(r)
    r = execute_graphql(schema,
        "mutation { callTool(name: \"demo\", arguments: {q: \"x\"}) }")
    print(r)
