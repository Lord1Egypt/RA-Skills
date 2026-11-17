# 设计决策清单

> 42 个关键设计决策 + trade-off 分析 + 主流 harness 选择对比。每个决策都标注了【谁选了什么】。

---


## 目录

- 一、Loop 层决策
  - D1: max_iterations 设多少？
  - D2: 同步还是异步？
  - D3: 流式还是批量？
- 二、Provider 层决策
  - D4: 支持多 provider 还是深度绑定？
  - D5: Provider 抽象层多厚？
  - D6: 支持 thinking blocks 吗？
- 三、Tools 层决策
  - D7: 单一 shell 还是分型工具集？
  - D8: 工具参数用什么校验？
  - D9: edit 工具是否拒绝模糊匹配？
  - D10: 工具失败重试策略？
  - D11: bash 工具的输出限制？
- 四、Permissions 层决策
  - D12: 权限模型选哪种？
  - D13: 沙箱默认开还是 opt-in？
  - D14: 权限 hook 的粒度？
- 五、Session 层决策
  - D15: 扁平 list 还是树？
  - D16: 存储格式？
  - D17: 是否做 checkpoint（代码快照）？
  - D18: 多 session 管理？
- 六、Compaction 层决策
  - D19: 何时触发 compaction？
  - D20: 摘要格式？
  - D21: 用什么模型做摘要？
  - D22: 压缩后原始数据保留吗？
  - D23: keep_recent 设多少？
  - D24: reserve_tokens 设多少？
- 七、Prompts & Skills 层决策
  - D25: 系统 prompt 多长？
  - D26: Skill 的 catalogue 放哪里？
  - D27: Skill body 何时加载？
  - D28: AGENTS.md vs CLAUDE.md vs .cursorrules？
- 八、Extensions 层决策
  - D29: Extension 用什么 API？
  - D30: Sub-agents 是 runtime feature 还是 extension？
  - D31: MCP 怎么集成？
  - D32: Plan mode 怎么实现？
- 九、Delivery 层决策
  - D33: 支持哪些交付界面？
  - D34: Extension UI 怎么跨 shell？
- 十、安全与运维决策
  - D35: 敏感信息如何处理？
  - D36: 审计日志？
  - D37: 速率限制？
  - D38: 如何防止 prompt 注入？
- 十一、性能决策
  - D39: Prompt caching？
  - D40: 并发工具调用？
  - D41: 预热模型？
  - D42: Token 计算用哪个 tokenizer？

## 一、Loop 层决策

### D1: max_iterations 设多少？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 25-50 | 安全，快速失败 | 复杂任务做不完 | Pi 默认 |
| 50-100 | 平衡 | 大多数场景合适 | Edd Mann, OpenCode |
| 无限 + 超时 | 不限任务复杂度 | 危险，可能死循环 | 不推荐 |

**推荐**：50-100，配合用户取消机制。

### D2: 同步还是异步？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 同步 | 简单 | 无法取消、无法并发 |
| 异步 | 可取消、可并发、可多 agent | 复杂度高 |

**推荐**：异步。取消机制是非谈判项。

### D3: 流式还是批量？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 流式 | 用户体验好、早期错误检测 | 实现复杂 |
| 批量 | 简单 | 用户等待焦虑、无法中途取消 |

**推荐**：必须流式。所有主流 harness 都是流式。

## 二、Provider 层决策

### D4: 支持多 provider 还是深度绑定？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 深度绑定单一 provider | 深度优化、体验一致 | 锁定 | Claude Code (Anthropic), Codex (OpenAI) |
| 多 provider 广覆盖 | 灵活、可选最便宜模型 | 难以深度优化 | Pi, OpenCode, OpenHarness |

**决策依据**：做产品 → 绑定；做平台 → 广覆盖；做轻量 harness → 广覆盖。

### D5: Provider 抽象层多厚？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 薄（直接 passthrough） | 简单、无性能损失 | 代码重复 |
| 厚（统一 StreamEvent + 窄协议） | provider 切换零成本 | adapter 复杂 |

**推荐**：厚。provider 差异大，薄抽象 = 每个 consumer 都要处理差异。

### D6: 支持 thinking blocks 吗？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 支持 | 推理透明、调试方便 | 额外 token 成本 |
| 不支持 | 省钱 | 推理不透明 |

**推荐**：支持，作为 opt-in。Anthropic 的 thinking blocks 对复杂推理显著提升质量。

---

## 三、Tools 层决策

### D7: 单一 shell 还是分型工具集？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 单一 shell | 极简 | 失败不可控 | 早期实验 |
| 7 件套分型 | 窄输出、RL 对齐好 | 工具多 | Claude Code, Codex, Pi, OpenCode |

**推荐**：7 件套。这是行业共识。

### D8: 工具参数用什么校验？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 手动 if-else | 无依赖 | 重复代码、易漏 |
| Pydantic | 一石二鸟（schema + 校验） | 依赖 |
| JSON Schema | 语言无关 | Python 体验差 |

**推荐**：Pydantic。生成给模型的 function schema + 校验模型回传，一套代码两个用途。

### D9: edit 工具是否拒绝模糊匹配？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 替换第一个 | 简单 | 可能改错位置 |
| 拒绝多次匹配 | 强制精确 | 模型可能需要多次尝试 |

**推荐**：拒绝。宁可报错让模型重试，也不要默默改错。失败信息告诉模型"出现了 N 次"→ 模型自然加入更多上下文。

### D10: 工具失败重试策略？

| 失败类型 | 重试？ | 理由 |
|---------|--------|------|
| unknown_tool | ❌ | 模型编造了不存在的工具 |
| validation_error | ❌ | 让模型看到错误自己修正 |
| tool_error（瞬时） | ✅ 一次 | 网络抖动等瞬时错误 |
| unexpected_error | ❌ | 记日志，返回通用错误 |

### D11: bash 工具的输出限制？

**问题**：`bash` 输出可能几千行，直接塞回 context 会爆窗口。

| 选项 | 谁选了 |
|------|--------|
| 截断到 N 行 + 提示"truncated" | Claude Code |
| 分页返回 | OpenCode |
| 不限制 | Pi（依赖用户自己管理） |

**推荐**：截断 + 提示。默认 2000 行。

---

## 四、Permissions 层决策

### D12: 权限模型选哪种？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 审批提示（每次问用户） | 最安全 | 烦人 | Claude Code 首次执行 |
| allow/deny 列表 | 自动化 + 可控 | 需要维护 | Codex, Claude Code |
| Hook 边界 | 最灵活 | 需要编程 | Edd Mann |
| 无（依赖 VCS） | 最简 | 不安全 | Pi |

**推荐**：Hook 边界 + 默认 allow/deny 列表。

### D13: 沙箱默认开还是 opt-in？

| 选项 | 谁选了 | 理由 |
|------|--------|------|
| 默认开 | Codex | 安全第一 |
| opt-in | Claude Code | 平衡便利和安全 |
| 不提供 | Pi, Edd Mann | 留给用户 |

**推荐**：默认开 read-only / workspace-write，danger-full-access 需显式选择。

### D14: 权限 hook 的粒度？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 工具级（拦截整个工具调用） | 简单 | 粒度粗 |
| 参数级（检查具体参数） | 精确 | 复杂 |
| 混合 | 灵活 | 实现难度中 |

**推荐**：混合。工具级快速过滤 + 参数级精确检查。

---

## 五、Session 层决策

### D15: 扁平 list 还是树？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 扁平 list | 简单 | 无法 fork/time-travel | 早期 harness |
| 不可变树 | fork/time-travel/compaction 都自然 | 实现复杂 | Pi, Edd Mann |
| 带祖先主记录 | 折中 | 压缩后原始数据丢 | Codex, Claude Code, OpenCode |

**推荐**：不可变树。"什么都不删"是最安全的设计。

### D16: 存储格式？

| 选项 | 优点 | 缺点 |
|------|------|------|
| JSONL（每行一个 entry） | 追加写入快、可流式读 | 查询需扫描 |
| SQLite | 查询快 | 追加不如 JSONL 直观 |
| JSON 单文件 | 简单 | 并发问题、大文件慢 |

**推荐**：JSONL。append-only 天然适配树结构。

### D17: 是否做 checkpoint（代码快照）？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 做 | rewind 时代码和对话一起回退 | 存储成本 | Codex, Claude Code |
| 不做 | 简单 | rewind 后代码不一致 | Pi, Edd Mann |

**推荐**：如果做产品 → 做；如果做轻量 harness → 不做（留给 git）。

### D18: 多 session 管理？

| 选项 | 谁选了 |
|------|--------|
| 每个目录一个 session | Claude Code |
| 显式 session ID | Pi, Edd Mann |
| 数据库管理 | OpenCode |

---

## 六、Compaction 层决策

### D19: 何时触发 compaction？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 固定阈值（80%） | 简单 | 可能太晚 | Edd Mann |
| 动态（基于剩余预算） | 精确 | 复杂 | OpenCode |
| 手动触发 | 用户控制 | 用户可能忘记 | Pi |

**推荐**：80% 固定阈值 + `keep_recent` 地板。

### D20: 摘要格式？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 自由文本 | 灵活 | 不可控、易漏信息 |
| 8 固定标题结构化 | 可控、可 grep | 可能不匹配所有场景 |

**推荐**：8 固定标题。覆盖了"接下来继续干活"需要的所有信息。

### D21: 用什么模型做摘要？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 主模型 | 质量高 | 贵 |
| 便宜模型（如 Haiku） | 省钱 | 质量可能不够 |
| 主模型 + 缓存 | 省钱且质量好 | 实现复杂 |

**推荐**：便宜模型。摘要不需要深度推理，便宜模型足够。SentinelOne 测评显示 compaction 对质量无显著影响。

### D22: 压缩后原始数据保留吗？

| 选项 | 优点 | 缺点 | 谁选了 |
|------|------|------|--------|
| 保留（追加 CompactionEntry） | 可回溯、可恢复 | 存储成本 | Pi, Edd Mann |
| 丢弃（原地改写） | 省存储 | 不可回溯 | Codex, Claude Code |

**推荐**：保留。"A compaction is a narrowing of view, not a discarding of state."

### D23: keep_recent 设多少？

| 选项 | 效果 |
|------|------|
| 5 | 激进压缩，context 很短但可能丢近期上下文 |
| 10 | 平衡（推荐） |
| 20 | 保守，压缩效果不明显 |

**推荐**：10。约 5 轮对话。

### D24: reserve_tokens 设多少？

**推荐**：4096。一个 bash stderr 可能 4000 token，不给余量就爆窗口。

---

## 七、Prompts & Skills 层决策

### D25: 系统 prompt 多长？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 短（~60 词） | 省 token | 可能不够引导 |
| 长（几百词） | 详细引导 | 每轮都付成本 |

**推荐**：短 base prompt + 动态拼接（tools + guidelines + context files + skills catalogue）。

### D26: Skill 的 catalogue 放哪里？

**推荐**：系统 prompt 尾部，XML 格式。只含 name + description + location，不含 body。

### D27: Skill body 何时加载？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 模型自己 `read` | 按需、省 token | 模型可能忘了读 |
| 自动注入 | 模型一定能看到 | 浪费 token |

**推荐**：模型自己 `read`。catalogue 的 description 要写得好，让模型知道何时该读。

### D28: AGENTS.md vs CLAUDE.md vs .cursorrules？

| 文件 | 谁用 | 作用 |
|------|------|------|
| AGENTS.md | Edd Mann, 通用 | 始终在场的项目级指令 |
| CLAUDE.md | Claude Code | 同上 |
| .cursorrules | Cursor | 同上 |

**推荐**：AGENTS.md。最通用的命名。

---

## 八、Extensions 层决策

### D29: Extension 用什么 API？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 三动词（on/register_tool/register_command） | 简洁、覆盖全 | 需要设计好事件系统 |
| 类继承 | 面向对象 | 过重 |
| 装饰器 | Pythonic | 难以发现 |

**推荐**：三动词。Pi 和 Edd Mann 验证过。

### D30: Sub-agents 是 runtime feature 还是 extension？

| 选项 | 谁选了 | 理由 |
|------|--------|------|
| Runtime 内置 | Codex, Claude Code | 产品化、深度优化 |
| Extension 实现 | Pi, Edd Mann | 简化 runtime、可定制 |

**推荐**：Extension。"不需要 runtime 知道 sub-agent 这个概念"是核心洞察。

### D31: MCP 怎么集成？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 每个 MCP 工具注册为一等工具 | 调用方便 | prompt 膨胀 |
| Proxy tool 模式 | 省 prompt | 多一跳调用 |

**推荐**：Proxy tool。常用工具可选 `directTools` opt-in 提升为一等。

### D32: Plan mode 怎么实现？

**推荐**：会话级状态 + 工具收窄 + 高 thinking level。用 extension 实现。

---

## 九、Delivery 层决策

### D33: 支持哪些交付界面？

| 选项 | 谁选了 |
|------|--------|
| TUI + CLI | Claude Code, Pi |
| TUI + CLI + Web | OpenCode, Edd Mann |
| app-server 协议 | Codex |

**推荐**：TUI + CLI。Web 可后续加。

### D34: Extension UI 怎么跨 shell？

**推荐**：`ctx.ui` callback dataclass。每种 shell 填支持的，其余 `None`。Extension 必须处理 `ctx.ui is None`。

---

## 十、安全与运维决策

### D35: 敏感信息如何处理？

| 策略 | 实现 |
|------|------|
| 工具结果脱敏 | `process_tool_result` hook 正则替换 |
| 环境变量过滤 | bash 执行前检查 |
| 文件路径限制 | workspace scope 限制 |

### D36: 审计日志？

**推荐**：所有工具调用记录到 JSONL（timestamp + tool + params + result + duration）。

### D37: 速率限制？

| 层 | 策略 |
|----|------|
| LLM 调用 | provider 自带速率限制 |
| 工具执行 | 每工具每分钟 N 次 |
| bash | 单次超时 + 总时长限制 |

### D38: 如何防止 prompt 注入？

| 策略 | 效果 |
|------|------|
| 工具结果与系统 prompt 分离 | 中等 |
| Extension 硬护栏 | 强 |
| 输入消毒 | 弱（误杀） |

**推荐**：不依赖 prompt 防注入，用 extension 硬护栏。

---

## 十一、性能决策

### D39: Prompt caching？

**推荐**：启用。不变的前缀走缓存，减少重复计算。OpenAI 和 Anthropic 都支持。

### D40: 并发工具调用？

| 选项 | 优点 | 缺点 |
|------|------|------|
| 串行 | 简单、安全 | 慢 |
| 并发 | 快 | 需要处理竞争 |

**推荐**：串行。工具间可能有依赖（read → edit）。

### D41: 预热模型？

**推荐**：不必要。provider 自带连接池。

### D42: Token 计算用哪个 tokenizer？

**推荐**：用 provider 的官方 tokenizer。估算可用 tiktoken（OpenAI）或 anthropic 的计数 API。
