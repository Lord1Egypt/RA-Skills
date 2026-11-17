# Claude API / Agent SDK 实战手册

> 配套 [skills/claude-agent-sdk/](../skills/claude-agent-sdk/SKILL.md)。这里放代码骨架、决策树、命令与踩坑清单；
> 路由层只索引能力，不重复这些内容。所有示例以 Anthropic 官方 SDK 为准，
> 模型 ID 以 [docs.anthropic.com](https://docs.anthropic.com) 最新为准（示例用 `claude-sonnet-4-5`）。

## 1. 接入方式决策树

```
要把 Claude 接进项目？
├─ 单次问答 / 一次性生成（摘要、抽取、翻译）
│   └─ 直接 Messages API 单次 create()            → 最简单
├─ 输出要逐字流式展示（聊天 UI / 长文）
│   └─ Messages API 流式（.stream() / stream 事件） → 显式 stream:true
├─ 模型需要调用外部函数 / API / 查数据库
│   └─ tool use（tools + tool_use/tool_result 循环） → 见 §4
└─ 要构建能多步自主完成任务、或编排多个子 Agent
    └─ Agent 模式（自管工具循环 或 Agent SDK）      → 见 §5
```

判断要点：**不需要模型主动调外部能力 → 单次/流式即可；需要 → tool use；
需要反复多轮决策 → Agent 循环**。不要一上来就上 Agent 框架，最小可用优先。

## 2. 安装与初始化

```bash
# Python
pip install anthropic

# TypeScript / Node
npm install @anthropic-ai/sdk

# Agent SDK（构建程序化 Agent，Python/TS）
pip install claude-agent-sdk
```

```bash
# API Key 走环境变量，不要硬编码进代码
export ANTHROPIC_API_KEY="sk-ant-..."   # 或用兼容网关的 BASE_URL
```

Python 最小初始化：

```python
from anthropic import Anthropic

client = Anthropic()  # 自动读 ANTHROPIC_API_KEY
```

TypeScript 最小初始化：

```ts
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();  // 自动读 process.env.ANTHROPIC_API_KEY
```

## 3. 最小调用骨架

Python 单次调用（**max_tokens 必填**）：

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="你是一名严谨的 ML 工程助理。",
    messages=[{"role": "user", "content": "用一句话解释过拟合。"}],
)
print(resp.content[0].text)
```

流式输出（Python）：

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": "写一段产品文案"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

TypeScript 流式：

```ts
const stream = await client.messages.stream({
  model: "claude-sonnet-4-5",
  max_tokens: 2048,
  messages: [{ role: "user", content: "写一段产品文案" }],
});
for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

## 4. 工具调用（tool use）

定义工具 → 模型返回 `tool_use` → 你执行 → 用 `tool_result` 回传 → 继续。

```python
tools = [{
    "name": "get_weather",
    "description": "查询某城市当前天气",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}]

messages = [{"role": "user", "content": "北京今天天气怎么样？"}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-4-5", max_tokens=1024,
        tools=tools, messages=messages,
    )
    # 若没有工具调用，说明模型已给出最终答案
    if resp.stop_reason != "tool_use":
        print(resp.content[0].text)
        break
    # 取出 tool_use 块并执行
    tool_use = next(b for b in resp.content if b.type == "tool_use")
    result = call_get_weather(tool_use.input["city"])  # 你的本地/远程函数
    # 把助手输出与工具结果追加回消息，继续下一轮
    messages.append({"role": "assistant", "content": resp.content})
    messages.append({
        "role": "user",
        "content": [{"type": "tool_result",
                     "tool_use_id": tool_use.id,
                     "content": result}],
    })
```

要点：
- `input_schema` 用 JSON Schema，`description` 写清用途，模型靠它决定是否调用。
- `tool_result.content` 可以是字符串，也可是结构化文本；出错要回传错误信息而非抛异常中断循环。
- 用 `tool_choice: {"type": "any"}` 可强制模型先调工具；默认自动决定。

## 5. Agent 模式（循环 / 子 Agent 编排）

**自管工具循环**（上面 §4 的 while 循环即最小 Agent）：适合任务明确、工具固定的场景。
关键护栏：
- 设**最大迭代步数**（如 10 步），到顶强制收尾，防无限循环。
- 每步记录轨迹，便于调试与回放。
- 高风险动作（写文件、发请求、执行命令）加人工确认或白名单。

**Agent SDK 程序化构建**（适合把 Agent 嵌入后端服务、做子 Agent 编排）：
- Python：`from claude_agent_sdk import Agent, tool` 装饰器声明工具，框架负责循环与上下文。
- 子 Agent 编排：主 Agent 拆解任务 → 派发子 Agent 并行/串行执行 → 汇总。
  注意上下文隔离（子 Agent 不应无脑继承全部历史，避免 token 爆炸）。

## 6. 降本与可靠性

- **提示缓存（prompt caching）**：把不变的 system / 长背景加
  `cache_control: {"type": "ephemeral"}`，命中缓存的 token 计费大幅降低。
  适合多轮对话、固定系统提示、大段参考资料。
- **速率限制**：遇 `429` 用指数退避重试（含 jitter）；不要在循环里裸调不重试。
- **token / 成本护栏**：给 `max_tokens` 设合理上限；长任务预估月成本，必要时截断。
- **延长思考（extended thinking）**：复杂推理任务可开启，但思考 token 也计费且延长时延。

## 7. 踩坑清单（W6 增量信息）

1. **漏填 max_tokens** → 直接 400 报错；每次 create 必带。
2. **API Key 硬编码** → 提交到仓库泄露；一律走环境变量 / 密钥管理。
3. **Agent 无限循环** → 不设最大步数，token 与费用失控；必须设上限 + 退出条件。
4. **工具结果不带 tool_use_id** → 模型无法对齐调用，报错；回传时务必带原 id。
5. **把超长历史全量塞进每轮** → token 暴涨、成本飙升；做摘要/截断/子 Agent 隔离。
6. **忽略 rate limit** → 突发流量 429 打断任务；加退避重试。
7. **信任模型生成的 JSON** → 可能不合法；解析前校验，必要时要求结构化输出并捕获异常。
8. **让 Agent 执行高风险操作不确认** → 删库/外发/转账；高风险动作加确认或白名单。
9. **模型 ID 写死旧版本** → 能力与价格漂移；集中配置并定期核对官方最新。
10. **敏感数据进提示** → 隐私/合规风险；明确数据边界，必要时脱敏。

## 8. 上线前检查清单

- [ ] API Key 来自环境变量，无硬编码、无提交
- [ ] 每次 `create` 都带 `max_tokens`
- [ ] 工具 `input_schema` 完整、描述清晰
- [ ] Agent 设了最大迭代步数与退出条件
- [ ] 工具循环带 `tool_use_id` 回传、错误不中断
- [ ] 长/固定上下文用了提示缓存
- [ ] 429 有指数退避重试
- [ ] 高风险动作有确认 / 白名单
- [ ] 模型 ID 集中管理、核对最新
- [ ] 成本与 token 预算已预估并设置护栏

## 相关子技能与层次边界（L2→L3）

- [claude-agent-sdk 子技能](../skills/claude-agent-sdk/SKILL.md) — 用 Claude API / Agent SDK 构建 AI 应用与 Agent：Messages API、流式、工具调用、Agent 编排（本 playbook 是其专属代码骨架与踩坑集）
