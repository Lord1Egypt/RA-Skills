# MCP Server 生成 Playbook（Python）

> 增量信息：决策树 + 命令 + 踩坑 + 检查清单。配套 [skills/mcp-server-generation/SKILL.md](../skills/mcp-server-generation/SKILL.md)，不重复子技能内容。

## 1. 决策树：要不要做 MCP Server

```
你的能力是想被 Agent/客户端「当工具调用」吗？
├─ 否（只是给模型一次性上下文）→ 直接写进 prompt，别造 server
└─ 是
   ├─ 目标环境是本地桌面客户端（Claude Desktop / Code）→ transport=stdio
   └─ 目标环境是远程 / 多租户 / 要上网暴露 → transport=streamable-http
      ├─ 有状态会话（保持连接）→ 默认 streamable-http
      └─ 无状态（每次请求独立、易扩缩）→ streamable-http + stateless=true
```

经验法则：**能 stdio 就 stdio**（部署最简单、无需网络）；只有「别人要从别的机器调用」才上 http。

## 2. 脚手架命令

```bash
# 1) 新建工程并初始化 uv 环境
uv init mcp-my-server && cd mcp-my-server
uv venv && source .venv/bin/activate

# 2) 装官方 MCP Python SDK（cli 含 mcp 命令与 Inspector 入口）
uv add "mcp[cli]"

# 3) 最小 server（stdio）
cat > src/mcp_my_server/server.py <<'PY'
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数相加。"""
    return a + b

if __name__ == "__main__":
    mcp.run()          # 默认 stdio
PY
```

streamable-http 变体（在 `mcp.run()` 前配置 transport）：

```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http")          # 默认 127.0.0.1:8000
    # 或：mcp.settings.host="0.0.0.0"; mcp.settings.port=8000; mcp.run(transport="streamable-http")
    # 无状态：mcp.run(transport="streamable-http", stateless=True)
```

## 3. 能力定义（装饰器 + 类型提示 = 自动 schema）

```python
@mcp.tool()
def search_db(q: str, limit: int = 10) -> list[str]:
    """按关键词查数据库，返回命中行文本。"""
    # 入参即 schema：q/limit 由类型提示生成；docstring 当工具描述
    ...

@mcp.resource("db://row/{row_id}")
def get_row(row_id: str) -> str:
    """把一行数据暴露成可读资源。"""
    ...

@mcp.prompt()
def review_prompt(code: str) -> str:
    """生成代码评审提示词。"""
    return f"请评审以下代码：\n{code}"
```

- **tool**：Agent 可调用的函数；返回结构化结果。
- **resource**：可被读取的「只读数据」（URI 模板）。
- **prompt**：预置的提示词模板。

Pydantic 入参做校验（推荐）：

```python
from pydantic import BaseModel, Field
class AddIn(BaseModel):
    a: int = Field(..., ge=0)
    b: int = Field(..., ge=0)

@mcp.tool()
def add(inp: AddIn) -> int:
    return inp.a + inp.b
```

## 4. 联调与运行

```bash
# MCP Inspector（浏览器里逐步调用 tool / 看 schema / 排错）
uv run mcp dev src/mcp_my_server/server.py

# 本地直接跑（stdio，供客户端拉起）
uv run python src/mcp_my_server/server.py
```

接 Claude Desktop（`claude_desktop_config.json`）/ Claude Code（`~/.claude.json` 的 mcpServers）：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["--directory", "/abs/path/mcp-my-server", "run", "python", "src/mcp_my_server/server.py"]
    }
  }
}
```

## 5. 踩坑清单

1. **transport 选错**：桌面客户端用 http 会连不上；确认客户端支持 streamable-http 再上。
2. **schema 不生成**：tool 必须有类型提示；无类型提示的参数不会进 schema。docstring 当描述，写清楚。
3. **async 混用**：tool 里做 IO 用 `async def` + `await`；同步阻塞函数会卡住事件循环。
4. **资源没清理**：开文件/连接要用 `async with` 或上下文管理器，否则连接泄漏。
5. **错误裸抛**：捕获异常返回结构化错误信息，别让整个 server 崩；stdio 下崩溃客户端直接掉线。
6. **http 鉴权缺失**：streamable-http 暴露到网络必须加 auth（token/Bearer），否则任何人可调用。
7. **路径用绝对路径**：客户端配置里的 `command`/`args` 用绝对路径，相对路径在客户端 cwd 下会找不到。
8. **依赖没锁**：用 `uv` 锁 `mcp[cli]` 版本，SDK 小版本可能改 API。

## 6. 收尾检查清单

- [ ] transport 与部署环境匹配（stdio 本地 / streamable-http 远程）
- [ ] 每个 tool 有类型提示 + docstring（schema 已生成、描述清晰）
- [ ] 入参有 Pydantic 校验或显式校验
- [ ] 资源/连接在上下文管理器里清理
- [ ] 错误被捕获并返回结构化信息（server 不裸崩）
- [ ] `uv run mcp dev` 在 Inspector 跑通至少一个 tool
- [ ] 客户端配置用绝对路径、已实际拉起验证
- [ ] 远程暴露已加鉴权
