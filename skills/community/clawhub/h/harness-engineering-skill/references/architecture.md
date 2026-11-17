# Agent Harness 架构总览：The Loop + 7 Rings

> 一个 harness 就是以 agent loop 为中心，向外扩展七层"环"。每层解决一个独立问题，可单独理解和替换。

---


## 目录

- Ring ①：The Loop（Agent 循环）
  - 关键设计决策
  - 失败模式
- Ring ②：Providers（模型适配层）
  - 问题
  - 解法：两层抽象
  - Provider 策略对比
- Ring ③：Tools & Permissions（工具与权限）
  - 工具系统
  - 工具失败四种类别
  - 权限系统
  - 沙箱
- Ring ④：Sessions & State（会话与状态）
  - 为什么不用扁平 list？
  - 树结构（Pi 首创）
  - 四种 Entry 类型
  - Session 策略对比
- Ring ⑤：Context Strategy & Compaction（上下文策略与压缩）
  - 为什么需要
  - 何时触发
  - 压缩做什么
  - 压缩在树里怎么存
  - 更细粒度的上下文管理
  - 实战数据（SentinelOne 测评）
- Ring ⑥：Prompts & Skills（提示词与技能）
  - 系统提示词分层组合
  - Skill 机制
  - Catalogue vs Body 分离
  - 两种调用路径
  - 三兄弟对比
- Ring ⑦：Extensions / Plugins（扩展系统）
  - Extension API
  - Handler ctx sub-APIs
  - 三个杀手级扩展
  - Extension 策略对比
- Delivery Shells（交付层）

## Ring ①：The Loop（Agent 循环）

**这是 harness 的心跳**。所有 harness 不管多复杂，核心就是四步循环：

```python
for turn in range(max_iterations):
    # 1. 把对话历史 + 工具列表发给模型
    messages_for_llm = prepare_context(session.messages)
    stream = provider.stream(messages_for_llm, tools=tools.get_schemas())

    # 2. 接收模型响应（文本 + 可能的 tool_calls）
    assistant_msg = consume_stream(stream)
    session.append(assistant_msg)

    # 3. 检查模型是否要调工具
    if not assistant_msg.tool_calls:
        break  # 模型不再要工具 → 循环结束

    # 4. 执行工具调用，结果回传给模型
    for tool_call in assistant_msg.tool_calls:
        result = execute_tool(tool_call)
        session.append(Message(role="tool", content=result))

# 循环结束条件：模型不再请求工具 / 触达 max_iterations / 用户取消
```

### 关键设计决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| `max_iterations` | 50-100 | 安全阀，防止无限工具调用 |
| 取消机制 | `cancel_event` 必须存在 | 否则用户无法中断长任务 |
| 事件流 | StreamEvent 统一抽象 | UI 实时渲染，不等完整响应 |
| 流式 vs 批量 | 必须流式 | 用户体验 + 早期错误检测 |

### 失败模式

| 失败 | 原因 | 解法 |
|------|------|------|
| 无限工具调用 | 模型陷入循环 | `max_iterations` + 超时 |
| 无法取消 | 同步阻塞 | `cancel_event` + 异步 I/O |
| 静默失败 | 模型不返回也不报错 | 超时 + 心跳检测 |
| 部分输出丢失 | 流中断未保存 | 逐 chunk 追加写入 session |

## Ring ②：Providers（模型适配层）

**解决不同 LLM provider 的 API 格式差异。**

### 问题

| Provider | 流式格式 | 认证 | 特殊性 |
|----------|---------|------|--------|
| OpenAI | `[0].function.arguments` raw JSON 累积 | API key | Responses API 又一套 schema |
| Anthropic | `content_block_delta` 需重组装 | API key | Thinking blocks 需特殊处理 |
| OpenAI Codex | 走 `chatgpt.com/backend-api/codex/responses` | OAuth | 订阅制，非 API key |
| Google Gemini | 又一套流式 schema | API key | 工具格式不同 |

### 解法：两层抽象

**1. 统一事件流（StreamEvent）**

```python
StreamEvent = (
    StartEvent | TextStartEvent | TextDeltaEvent | TextEndEvent |
    ThinkingStartEvent | ThinkingDeltaEvent | ThinkingEndEvent |
    ToolCallStartEvent | ToolCallDeltaEvent | ToolCallEndEvent |
    AssistantMetadataEvent | DoneEvent | ErrorEvent
)
```

所有 provider 的流式输出都转成同一种事件类型。

**2. 窄协议（LLMProvider Protocol）**

```python
class LLMProvider(Protocol):
    name: str
    model: str
    def set_model(self, model: str) -> None: ...
    def stream(self, messages, tools, options) -> AssistantMessageEventStream: ...
    def supports_thinking(self) -> bool: ...
    async def list_models(self) -> list[str]: ...
    async def close(self) -> None: ...
```

Agent loop 只依赖这个最小接口。翻译逻辑全在 adapter 内部。

### Provider 策略对比

| Harness | Provider 覆盖 | 策略 |
|---------|-------------|------|
| Claude Code | Anthropic 系 | 深度绑定 |
| Codex | OpenAI 系 | ChatGPT 订阅 OAuth |
| Pi / OpenCode | 广覆盖 | 多 adapter |
| Edd Mann | OpenAI + Anthropic + 兼容 | 兼顾前沿和长尾 |
| OpenHarness | 广覆盖 | 研究导向 |

---

## Ring ③：Tools & Permissions（工具与权限）

### 工具系统

**两种路线**：

| 路线 | 代表 | 优点 | 缺点 |
|------|------|------|------|
| 单一 shell 工具 | 早期实验性 harness | 极简，模型已知如何组合 ls/cat/grep | 失败模式不可控，输出冗长 |
| 分型工具集 | Claude Code, Codex, OpenCode（Pi 内核默认 4 件套，其余经扩展） | 窄输出、低 token、RL 对齐好 | 工具数量多 |

**主流收敛到 7 件套**（Claude Code 普及）：

| 工具 | 作用 | 设计要点 |
|------|------|---------|
| `read` | 读文件 | 返回带行号的内容，让后续 `edit` 可精确引用 |
| `write` | 写文件 | 整体写入 |
| `edit` | 编辑文件 | **拒绝模糊匹配**——`old_string` 出现多次时报错 |
| `bash` | 执行 shell | 最大权限但最需权限控制 |
| `grep` | 搜索内容 | 输出比 raw shell 更窄 |
| `find` | 查找文件 | 同上 |
| `ls` | 列目录 | 同上 |

**工具即 Schema**——每个工具先是一个 Pydantic model（生成 schema + 校验参数），然后才是 callable：

```python
class EditParams(BaseModel):
    path: str = Field(description="The file path to edit")
    old_string: str = Field(description="The exact string to find and replace")
    new_string: str = Field(description="The string to replace with")
    replace_all: bool = Field(default=False, description="Replace all occurrences")

class EditTool(BaseTool[EditParams]):
    name = "edit"
    description = "Edit a file by finding and replacing text..."
    parameters = EditParams

    async def execute(self, params: EditParams) -> str: ...
```

Pydantic **一石二鸟**：给模型生成 function schema + 给 harness 校验模型回传的参数。

### 工具失败四种类别

| 类别 | 处理 |
|------|------|
| `unknown_tool` | 返回错误，不重试 |
| `validation_error` | 返回参数校验错误，模型可修正 |
| `tool_error` | 瞬时错误自动重试一次 |
| `unexpected_error` | 记录日志，返回通用错误 |

### 权限系统

**权限决定"模型想做"和"harness 允许做"之间的边界。**

三种成熟度：

| 级别 | 代表 | 机制 |
|------|------|------|
| 重度 | Claude Code, Codex, OpenCode | 审批提示、allow/deny 列表、scope 绑定 |
| 中度 | Edd Mann | Hook 边界（`authorize_tool_call` + `process_tool_result`） |
| 轻度 | Pi | 依赖用户自己的版本控制 |

**Hook 机制**（最灵活）：

```python
# authorize_tool_call: 工具执行前拦截
async def block_rm(event, ctx):
    if "rm -rf" in str(event.input):
        return ToolCallResult(block=True, reason="dangerous command")

# process_tool_result: 工具执行后改写
async def redact_secrets(event, ctx):
    return event.result.replace("AKIA****", "[REDACTED]")
```

### 沙箱

**权限决定"是否运行"，沙箱决定"运行时爆炸半径多大"**：

| Harness | 沙箱方案 | 默认开 |
|---------|---------|--------|
| Codex | macOS Seatbelt / Linux bubblewrap | ✅ 默认开 |
| Claude Code | 同上但 opt-in `/sandbox` | ❌ opt-in |
| Pi / OpenCode / Edd Mann | 留给用户 | ❌ |

Codex 三种模式：`read-only` / `workspace-write` / `danger-full-access`

---

## Ring ④：Sessions & State（会话与状态）

**解决跨时间记忆——关掉终端明天回来还能接着干。**

### 为什么不用扁平 list？

扁平 message list 只能"恢复到上次"。但真实使用有三个需求：

1. **Fork**——在第 40 条消息处分叉，试另一条路，不丢当前分支
2. **Time-travel**——回到第 20 条，假装后面的没发生过
3. **Compaction**——压缩旧消息但原始数据不能丢

### 树结构（Pi 首创）

**核心思想：append-only，不原地改写。**

```
msg#a (system)
└── msg#b (user)
    └── msg#c (assistant)
        └── mc#d (model_change → Opus)
            └── msg#e (user)
                └── ... 
                    └── msg#n ← leaf (当前)
```

- `leaf_id` 指向当前分支顶端
- 从 leaf 沿 `parent_id` 回溯到根 = 当前活跃分支
- `fork()` 写新文件，复制到 fork 点
- `set_leaf(entry_id)` 追加 `SessionStateEntry` → 时间旅行
- **什么都不删**

### 四种 Entry 类型

| Entry 类型 | 作用 |
|-----------|------|
| `MessageEntry` | 一条消息（user/assistant/tool） |
| `ModelChangeEntry` | 记录中途换模型 |
| `CompactionEntry` | 记录压缩点（摘要 + 指向第一条保留的消息） |
| `SessionStateEntry` | 记录 leaf 移动（time-travel） |

每条 entry 有 `id` + `parent_id` + `timestamp`。整个 session 是一个 JSONL 文件。

### Session 策略对比

| Harness | 结构 | 压缩后原始数据 | Checkpoint |
|---------|------|---------------|-----------|
| Codex / Claude Code / OpenCode | 带祖先主记录 | ❌ 原地改写 | ✅ 绑定会话状态 |
| Pi / Edd Mann | 不可变树 | ✅ 保留 | ❌ 留给用户 VCS |

---

## Ring ⑤：Context Strategy & Compaction（上下文策略与压缩）

**这是 harness 工程最核心的技术难点之一。**

### 为什么需要

即使 1M token 窗口：
- 长上下文**稀释注意力**——模型越长越"蠢"
- 解码速度随上下文线性下降
- 每轮都发全量历史 → 成本飙升

### 何时触发

```python
def needs_compaction(self, messages: list[Message]) -> bool:
    if len(messages) <= self.keep_recent + 1:
        return False  # 太短不压
    available = self.max_tokens - self.reserve_tokens
    return self.current_tokens(messages) > available * 0.8  # 80% 阈值
```

**两个关键参数**：
- `keep_recent + 1`：地板——短会话永远不压缩
- `reserve_tokens`：预留——不给工具输出留余量 → 一个 4000 token 的 stderr 就爆窗口

### 压缩做什么

把旧消息交给 summariser，用**结构化 prompt** 生成摘要：

```
Summarize the following conversation concisely.
Output markdown with these headings in order:
1) Summary
2) Decisions
3) Files Read
4) Files Modified
5) Commands Run
6) Tools Used
7) Open TODOs
8) Risks/Concerns

Rules:
- Do NOT include system prompt text or policies.
- Keep bullets short and actionable.
```

**为什么 8 个固定标题？**——自由摘要经常漏掉下一轮最需要的信息。固定标题 = 给模型的 checklist，输出可 grep。

### 压缩在树里怎么存

**不原地改写，而是追加 `CompactionEntry`**：

```
[old msg #1] ... [old msg #20] [CompactionEntry] [msg #21] ... [msg #30 ← leaf]
```

`_rebuild_messages()` 发现 compaction entry 后：
1. system messages 照常
2. 插入一条合成的 system message（携带摘要）
3. 从 `first_kept_entry_id` 开始的 recent messages
4. provider 看到的是短视图，文件里存的是长原始

**"A compaction is a narrowing of view, not a discarding of state."**

### 更细粒度的上下文管理

| 策略 | 作用 | 代表 |
|------|------|------|
| Tool-result pruning | 工具输出太长先单独裁剪 | OpenCode |
| prepare_context hook | 每轮最后一次机会改 prompt | Edd Mann |
| Compaction hook | 扩展决定压缩时返回什么 | Pi |
| Prompt caching | provider 层缓存重复前缀 | OpenAI / Anthropic |

### 实战数据（SentinelOne 测评）

OpenAI 原生 compaction 在自动化恶意软件分析评测中：
- 输入 token 减少 **~86%**
- 评测分数**无显著变化**
- 长任务成本和噪音大幅降低

---

## Ring ⑥：Prompts & Skills（提示词与技能）

### 系统提示词分层组合

```
base prompt（~60 词，声明角色和任务类别）
  → active tool descriptions（当前启用的工具）
    → dynamic guidelines（工具组合提示，如"prefer grep/find over bash"）
      → context files（AGENTS.md / CLAUDE.md）
        → skills XML（技能目录，只含 name + description + location）
          → environment info
            → any appended content
```

### Skill 机制

**Skill = 按需加载的领域知识。**

```markdown
---
name: commit
description: Create git commits using Conventional Commits format
---
# Commit
Create a commit for the current changes using a Conventional Commits subject:
> `<type>(<scope>): <summary>`
- Use `feat` for new features, `fix` for bug fixes.
- Keep the summary imperative and under 72 characters.
- Only commit; do not push.
```

**三路径加载**（优先级高→低）：
1. `.agent/skills/`（项目级）
2. config 指定的额外路径
3. `~/.agent/skills/`（用户级）

### Catalogue vs Body 分离

系统 prompt 里只放**目录**（name + description + location），不放 body：

```xml
<available_skills>
  <skill>
    <name>commit</name>
    <description>Create git commits using Conventional Commits format</description>
    <location>/Users/edd/.agent/skills/commit/SKILL.md</location>
  </skill>
</available_skills>
```

30 个 skill 只花 30 行 description 的 token，不是 30 个 body。模型看到描述匹配任务时，自己调 `read` 工具加载 body。

### 两种调用路径

| 路径 | 机制 | 谁触发 |
|------|------|--------|
| Implicit | 模型看到 catalogue 描述匹配 → 调 `read` 加载 body | 模型自主 |
| Explicit | 用户输入 `$commit` → 预处理器展开成 `<skill>` block + 用户指令 | 用户主动 |

### 三兄弟对比

| 概念 | 谁触发 | 作用域 |
|------|--------|--------|
| Skill | 模型按需 / 用户 `$` 前缀 | 任务级 |
| Prompt Template | 用户 `/` 前缀 | 替换整条用户消息 |
| AGENTS.md | 始终在场 | 全局 |

---

## Ring ⑦：Extensions / Plugins（扩展系统）

**Skills 扩展 prompt（文本），Extensions 扩展 loop（行为）。这是 harness 工程最核心的对称性。**

### Extension API

```python
def setup(api: ExtensionAPI):
    # 三动词
    api.on(event, handler)          # 订阅生命周期事件
    api.register_tool(tool)          # 注册新工具
    api.register_command(name, handler)  # 注册 slash command
```

### Handler ctx sub-APIs

| Sub-API | 能力 |
|---------|------|
| `ctx.runtime` | 查空闲状态、中止运行、排队用户消息、读系统 prompt |
| `ctx.session` | 读消息/entry、fork、移 leaf、新建 session |
| `ctx.model` | 获取/设置活跃模型和 thinking level |
| `ctx.tools` | 列出/收窄/注册工具 |
| `ctx.ui` | 交付层 UI 辅助（仅当 shell 附着时） |

### 三个杀手级扩展

**① Sub-agents（子代理）**

不是新类，是 `Agent` 实例的递归使用：

```python
PROFILES = {
    "researcher": SubagentProfile(
        active_tools=("read", "grep", "find", "ls")),
    "reviewer": SubagentProfile(
        active_tools=("read", "grep", "find", "ls"),
        thinking_level=ThinkingLevel.HIGH),
    "implementer": SubagentProfile(
        active_tools=("read", "grep", "find", "ls", "edit", "write", "bash")),
}
```

`/subagent researcher survey the auth middleware` → 新建子 Agent → 多轮循环 → 返回结构化 JSON → `/subagent-apply` 排回父线程。

**Sub-agent 设计差异**：

| Harness | 继承父上下文 | 循环模式 | 返回格式 |
|---------|------------|---------|---------|
| Codex | 可配嵌套深度 | 多轮 | 结构化 |
| Claude Code | 用户选 inline/fork | fork 模式独立预算 | 自由文本 |
| Edd Mann | 不继承 | 多轮 | 结构化 JSON |

**② Plan Mode（计划模式）**

会话级状态，收窄工具到只读 + 高 thinking level：

```python
async def _plan_command(args, ctx):
    match args.split(maxsplit=1):
        case ["on"]:
            ctx.tools.set_active(["read", "grep", "find", "ls"])
            ctx.model.set_thinking_level("high")
        case ["apply"]:
            plan = _load_plan(ctx.session.id)
            ctx.tools.set_active(DEFAULT_TOOLS)
            await ctx.runtime.send_user_message(plan)
```

**③ MCP Adapter（Model Context Protocol 适配器）**

**不是把所有 MCP 工具塞进系统 prompt，而是注册一个 proxy tool：**

```python
def setup(api: ExtensionAPI):
    api.register_tool(MCPProxyTool())  # 单一代理工具

# 模型通过 proxy 按需发现和调用：
mcp({ search: "echo" })           # 搜工具
mcp({ describe: "echo_echo" })    # 查 schema
mcp({ tool: "echo_echo", args: ... })  # 调用
```

**设计要点**：MCP adapter 是 extension 不是 runtime feature。删掉就移除。

### Extension 策略对比

| Harness | 策略 | MCP | Sub-agents | Plan mode |
|---------|------|-----|-----------|-----------|
| Pi | 最简，全推给扩展 | ❌ 扩展 | ❌ 扩展 | ❌ 扩展 |
| Codex / Claude Code | 产品化，内置 | ✅ 内置 | ✅ 内置 | ✅ 内置 |
| OpenCode | 分层（runtime/TUI 双插件） | ✅ | ✅ | ✅ |
| Edd Mann | Pi 阵营，hook 边界 | 扩展 | 扩展 | 扩展 |

---

## Delivery Shells（交付层）

**Runtime 不关心用户怎么跟它交互。Delivery shell 是用户触达 loop 的通道。**

| Shell | 场景 | 特点 |
|-------|------|------|
| TUI (Textual) | 日常交互 | 最丰富：流式渲染、thinking block、模态框 |
| Headless CLI | 脚本/CI | 最薄：一个 prompt 参数 → 跑一次 → stdout → 退出 |
| Web (FastAPI + WebSocket) | 浏览器 | TUI 的 web 版 |

**Extension UI 抽象**——同一份 extension 代码跨三种 shell 运行：

```python
await ctx.ui.confirm("Apply the current plan?")
await ctx.ui.select("Pick a profile", ["researcher", "reviewer"])
await ctx.ui.input("Task for subagent")
```

`ctx.ui` 底层是 `ExtensionUIBindings`（callback dataclass），每种 shell 填它支持的，其余 `None`。
