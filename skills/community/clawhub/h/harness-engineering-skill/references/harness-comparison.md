# 主流 Agent Harness 横向对比

> 六大 harness 的全维度对比，蒸馏自各项目源码、官方文档和社区评测。

---

## 速查对比表

| 维度 | Claude Code | Codex | Pi | OpenCode | Edd Mann | OpenHarness |
|------|------------|-------|-----|---------|---------|-------------|
| **定位** | Anthropic 闭源产品 | OpenAI 生态 | 最简主义 | 分层最细 | 轻量自建 | 研究导向 |
| **语言** | TypeScript | TypeScript | TypeScript | TypeScript | Python | Python |
| **开源** | ❌ | ❌ | ✅ MIT | ✅ MIT | ✅ MIT | ✅ MIT |
| **Provider** | Anthropic 系 | OpenAI 系 | 广覆盖 | 广覆盖 | OAI+Anthropic | 多 provider |
| **工具集** | 7 件套 | 7 件套 | 4 件套（核心默认） | 7 件套 | 7 件套 | 7 件套+ |
| **权限** | 审批+列表 | 审批+列表 | 轻量 | 审批+列表 | Hook 边界 | 审批+列表 |
| **沙箱** | opt-in | 默认开 | 轻量 | 轻量 | 轻量 | opt-in |
| **Session** | 带祖先主记录 | 带祖先主记录 | 不可变树 | 带祖先主记录 | 不可变树 | 扁平+压缩 |
| **压缩** | 原地改写 | 原地改写 | 追加式 | 原地+pruning | 追加式 | 原地改写 |
| **扩展** | 内置 | 内置 | 全推给扩展 | 双层插件 | Extension API | 内置+插件 |
| **MCP** | 内置 | 内置 | 扩展实现 | 内置 | 扩展实现 | 内置 |
| **Sub-agents** | 内置 | 内置 | 扩展实现 | 内置 | 扩展实现 | 内置 |
| **Plan mode** | 内置 | 内置 | 扩展实现 | 内置 | 扩展实现 | ❌ |
| **Delivery** | TUI+CLI | app-server | TUI+CLI+RPC | TUI+CLI+Web+Electron | TUI+CLI+Web | TUI+CLI |
| **Stars** | N/A | N/A | - | - | - | GitHub 实时 |

---

## 1. Claude Code

**一句话**：Anthropic 的闭源编码代理，深度绑定 Anthropic 模型，产品化程度最高。

### 架构特点
- **Provider**：深度绑定 Anthropic（Claude Sonnet/Opus），不走 OpenAI
- **工具**：7 件套 + 诊断工具（mcp__*, web_search 等）
- **权限**：首次执行危险操作时审批，之后加入 allow 列表
- **Session**：带祖先的主记录，支持 rewind
- **Compaction**：原地改写，Checkpoint 绑定代码快照
- **扩展**：插件系统 + MCP 内置 + Sub-agents 内置
- **沙箱**：opt-in `/sandbox`（macOS Seatbelt / Linux bubblewrap）
- **AGENTS.md**：项目级指令文件，始终在 system prompt 中

### 独特优势
- 产品化最成熟，用户体验最好
- 深度 Anthropic 模型优化（thinking blocks 等）
- 插件生态丰富

### 劣势
- 闭源，无法自定义核心逻辑
- 绑定 Anthropic 模型
- 无法作为快速启动模板（需自己写）

---

## 2. OpenAI Codex

**一句话**：OpenAI 的编码代理，安全优先，默认沙箱。

### 架构特点
- **Provider**：走 ChatGPT 订阅 OAuth（`chatgpt.com/backend-api/codex/responses`）
- **沙箱**：默认开（macOS Seatbelt / Linux bubblewrap），三模式
  - `read-only`：只读
  - `workspace-write`：只能写工作目录
  - `danger-full-access`：完全访问（需显式选择）
- **Session**：带祖先主记录，Checkpoint 绑定代码快照
- **Compaction**：原地改写 + Responses API 原生 compaction（2026.03 新增）
- **扩展**：MCP 内置 + Sub-agents 内置 + Plan mode 内置
- **Delivery**：app-server 协议（可被多种客户端调用）
- **Sub-agents**：可配嵌套深度，结构化返回

### 独特优势
- 安全设计最完善（默认沙箱）
- OpenAI 生态集成（Responses API 原生 compaction）
- app-server 协议让多种客户端可复用

### 劣势
- 绑定 OpenAI 模型
- 闭源

### SentinelOne Compaction 评测

SentinelLABS 用自动化恶意软件分析评测 Codex 的 native compaction：
- **input tokens 减少 ~86%**
- **评测分数无显著变化**
- 结论：compaction 可显著降低成本和噪音，不牺牲任务质量

---

## 3. Pi

**一句话**：最简主义 agent harness，runtime 精简到极致，一切功能推给扩展。

### 架构特点
- **Provider**：广覆盖（OpenAI, Anthropic, OpenAI-compatible）
- **Session**：不可变树（首创），append-only JSONL
  - 四种 Entry：MessageEntry / ModelChangeEntry / CompactionEntry / SessionStateEntry
  - Fork / Time-travel / Compaction 都通过追加实现
- **Compaction**：追加式，原始数据保留
- **扩展**：三动词 API（on / register_tool / register_command）
  - MCP / Sub-agents / Plan mode 全是扩展实现
  - Extension 可访问 `ctx.runtime` / `ctx.session` / `ctx.model` / `ctx.tools` / `ctx.ui`
- **Delivery**：TUI + CLI + RPC

### 设计哲学

> "It is an agent connected to a communication channel of your choosing. Pi is the agent harness that fuels OpenClaw." — Armin Ronacher

核心理念：**runtime 不应该知道 "sub-agent" / "MCP" / "plan-mode" 这些概念**。它们都是 extension 实现的，runtime 只提供足够中性的 hook。

### 独特优势
- Runtime 最精简，可组合性最强
- 不可变树设计最优雅
- 7 Rings 架构的最完整公开剖析
- 第三方扩展空间最大

### 劣势
- 开箱体验差（需要装扩展）
- 扩展质量参差
- 某些深度优化做不到

---

## 4. OpenCode

**一句话**：分层最细的 harness，server/TUI 双插件系统，支持最多交付界面。

### 架构特点
- **Provider**：广覆盖
- **Session**：带祖先主记录 + 原地改写
- **Compaction**：原地改写 + tool-result pruning（更细粒度）
- **扩展**：双层插件
  - Runtime 插件：hooks / tools / commands
  - TUI 插件：UI 组件 / themes / keybindings
- **Delivery**：TUI + CLI + Web + Electron（覆盖最广）
- **MCP**：内置
- **Sub-agents**：内置
- **Plan mode**：内置

### 独特优势
- 交付层最丰富（Web + Electron）
- 双层插件最灵活
- Compaction 粒度最细（tool-result pruning）

### 劣势
- 架构复杂度高
- 产品化程度不如 Claude Code / Codex

---

## 5. Edd Mann / my-own-coding-agent

**一句话**：轻量级 Python harness，Pi 阵营，7 Rings 架构的最完整公开剖析。

### 架构特点
- **Provider**：OpenAI + Anthropic + OpenAI-compatible
- **Session**：不可变树（借鉴 Pi）
- **Compaction**：追加式（借鉴 Pi）
- **扩展**：Extension API（借鉴 Pi 的三动词）
- **Delivery**：TUI (Textual) + CLI + Web (FastAPI + WebSocket)
- **Sub-agents**：Extension 实现，`Agent` 类递归使用
- **MCP**：Extension 实现，proxy tool 模式
- **Plan mode**：Extension 实现

### 独特价值
- **最完整的公开实现剖析**：Edd Mann 的博客文章详细记录了每个设计决策的 why
- **架构最清晰**：每个环独立可理解
- **Hook 边界**：`authorize_tool_call` + `process_tool_result`
- **Extension UI 抽象**：同一份代码跨 TUI/CLI/Web 运行

### 关键洞察

> "Once you see it that way, Claude Code, Codex, Pi, OpenCode (and the rest) stop being distinct products. They are the same rings, drawn differently."

### Session Tree 实现

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
- `fork()` 写新文件，两条路之后可以分叉
- `set_leaf(entry_id)` 追加 `SessionStateEntry` → 时间旅行
- **什么都不删**

### Compaction 实现

8 个固定标题：Summary / Decisions / Files Read / Files Modified / Commands Run / Tools Used / Open TODOs / Risks/Concerns

> "A compaction is a narrowing of view, not a discarding of state."

---

## 6. OpenHarness (HKUDS)

**一句话**：开源 Python harness（星数以 GitHub 实时为准），研究导向，内置个人 agent Ohmo。

### 架构特点
- **Provider**：多 provider 支持
- **Session**：扁平 + 压缩
- **扩展**：内置 + 插件
- **Delivery**：TUI + CLI
- **内置 agent**：Ohmo（个人助手）
- **Stars**：GitHub 实时为准

### 独特优势
- 研究导向，适合学术研究
- 内置 Ohmo agent，开箱即用
- 社区活跃

### 已知问题
- 终端兼容性：旧版本对 macOS Terminal.app 的 Backspace（DEL byte 0x7f）处理不当
- 建议升级到最新版

---

## 选型决策树

```
你的需求是什么？
├── 产品（给最终用户用）
│   ├── 绑定 Anthropic → Claude Code
│   └── 绑定 OpenAI → Codex
├── 平台（给开发者用）
│   ├── Python 生态 → Pi
│   └── TypeScript 生态 → OpenCode
├── 理解原理
│   ├── 深度文章 → Edd Mann（7 Rings 最完整剖析）
│   └── 开源项目 → OpenHarness / Pi
├── 研究
│   └── OpenHarness（学术导向）
└── 自建
    ├── 参考 Pi 的极简哲学
    ├── 参考 Edd Mann 的 7 Rings 架构
    └── 参考 OpenCode 的双层插件
```

---

## 关键设计差异总结

### Session 设计差异

| 设计 | 谁选了 | 压缩后原始数据 | Fork/Time-travel | Checkpoint |
|------|--------|---------------|-----------------|-----------|
| 不可变树 | Pi, Edd Mann | ✅ 保留 | ✅ 自然支持 | ❌ 留给 VCS |
| 带祖先主记录 | Codex, Claude Code, OpenCode | ❌ 原地改写 | ✅ 通过 rewind | ✅ 绑定会话 |
| 扁平+压缩 | OpenHarness | ❌ 原地改写 | ❌ | ❌ |

### 扩展策略差异

| 设计 | 谁选了 | 优点 | 缺点 |
|------|--------|------|------|
| 内置一切 | Codex, Claude Code, OpenCode | 开箱即用 | runtime 膨胀 |
| 全推给扩展 | Pi, Edd Mann | runtime 精简 | 开箱体验差 |
| 内置+插件 | OpenHarness | 平衡 | 复杂度中 |

### Compaction 策略差异

| 设计 | 谁选了 | 原始数据 | 粒度 |
|------|--------|---------|------|
| 追加式 | Pi, Edd Mann | ✅ 保留 | 消息级 |
| 原地改写 | Codex, Claude Code | ❌ 丢弃 | 消息级 |
| 原地+pruning | OpenCode | ❌ 丢弃 | 消息级 + tool-result 级 |
| 原生 API | Codex (Responses API) | ❌ 丢弃 | provider 层 |
