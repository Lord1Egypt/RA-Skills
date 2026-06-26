# 🔍 Smart Compact — 智能压缩增强

> 让 OpenClaw 的 /compact 不再丢失重要信息。先救后压，四阶段智能上下文管理。

---

## 中文说明

### 这是什么？

AI Agent 对话越长，上下文越大，token 消耗越快。压缩上下文是必须的，但 OpenClaw 原生的 `/compact` 是一步到位的压缩——整个对话被浓缩成一段摘要，过程中**大量细节会丢失**。

你有没有遇到过这些情况？
- Agent 压缩后忘了刚才调试好的 API 端点
- 配置文件的路径、IP、端口信息全部丢失
- 之前踩过的坑，压缩后又要重新踩一遍
- 做了某个决策，压缩后连原因都想不起来了

**Smart Compact** 在 `/compact` 之前插入一个"预处理"阶段：**先把重要信息救出来，写入记忆文件，确认安全后再压缩**。

### 核心理念：先救后压

传统压缩是一刀切，Smart Compact 采用**四阶段渐进式**策略：

```
阶段一「扫描」 → 阶段二「提取」 → 阶段三「检查」 → 阶段四「压缩」
```

每个阶段都有明确的职责，确保信息不会在压缩中意外丢失。

### 安装

**方式一（推荐）：通过 ClawHub**

```bash
clawhub install smart-compact
```

**方式二：从 GitHub 克隆**

```bash
git clone https://github.com/wavmson/openclaw-skill-smart-compact.git \
  ~/.openclaw/skills/smart-compact
```

**方式三：只复制核心文件**

```bash
mkdir -p ~/.openclaw/skills/smart-compact
curl -o ~/.openclaw/skills/smart-compact/SKILL.md \
  https://raw.githubusercontent.com/wavmson/openclaw-skill-smart-compact/main/SKILL.md
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 使用方法

对你的 Agent 说以下任意一种触发词：

| 触发词 | 说明 |
|--------|------|
| `智能压缩` | 中文触发 |
| `smart-compact` | 英文触发 |
| `压缩检查` | 只做检查不压缩 |
| `pre-compact` | 压缩前预处理 |
| `compact check` | 同"压缩检查" |

### 四阶段详解

#### 阶段一：扫描（Scan）

回顾当前对话中所有的工具调用结果（`exec`、`read`、`web_fetch`、`web_search` 等），识别：

- **大块输出**：超过 50 行或 2000 字符的工具结果
- **关键信息**：配置值、IP 地址、API 端点、文件路径、认证信息
- **引用状态**：该信息是否已被后续对话引用或总结过
- **冗余判断**：是否是重复的 `ls`、`git status` 等输出

#### 阶段二：提取（Extract）

从工具输出和对话中提取值得持久化的信息，分类写入 `memory/YYYY-MM-DD.md`：

- 🔵 **新事实**：IP 地址、端口号、文件路径、API 端点
- 🟡 **决策记录**：为什么选了方案 A 而不是 B，以及原因
- 🔴 **踩坑记录**：错误信息和对应的解决方案
- 🟢 **用户偏好**：用户明确表达的喜好或要求
- 🟣 **任务进度**：哪些做完了，哪些还在进行中

写入规则：
- 只使用**追加模式**，绝不覆盖已有内容
- 每条记忆附带简短的来源说明
- 敏感信息（如 认证令牌）会脱敏处理

#### 阶段三：检查（Check）

生成一份结构化的压缩前检查清单：

```
📋 Smart Compact 检查清单
━━━━━━━━━━━━━━━━━━━━━━

📊 扫描统计：
- 工具调用总数：23 次
- 大块输出（>50行）：5 个
- 已引用/总结过的：3 个
- 可安全压缩的：4 个

💾 已提取到记忆：
- [+] Docker 容器端口配置 18060
- [+] GitHub 推送权限已配置
- [+] 小红书发布正文限制 1000 字
（共 3 条写入 memory/2026-04-02.md）

⚠️ 需要注意：
- [!] exec 输出包含 API 响应但尚未被引用

✅ 建议：可以安全执行 /compact
```

#### 阶段四：压缩（Compact）

- 如果检查清单显示 ✅，提示用户确认
- 用户确认后才执行 `/compact`
- 如果有 ⚠️ 警告项，建议先处理再压缩
- **绝不自动压缩**——必须用户明确同意

### 设计原则

| 原则 | 说明 |
|------|------|
| 🛡️ 先救后压 | 宁可多存也不能漏存 |
| 📝 追加写入 | 只追加记忆文件，绝不覆盖已有内容 |
| 🔒 不自动压缩 | 必须用户确认才执行压缩操作 |
| 👁️ 透明可控 | 每一步操作都有详细报告和统计 |
| 🔑 安全优先 | 敏感信息脱敏，绝不泄露认证信息 |
| ♻️ 幂等设计 | 重复执行不会产生副作用 |

### 信息分类标准

| 类别 | 处理方式 | 示例 |
|------|----------|------|
| 🔴 必须保存 | 写入记忆 | 认证令牌、IP 地址、配置值、错误解决方案 |
| 🟡 建议保存 | 写入记忆 | 决策原因、用户偏好、任务进度 |
| 🟢 可以丢弃 | 标记安全 | 重复的 ls 输出、已被总结的搜索结果 |

### 与 Memory-Dream 搭配使用

Smart Compact 和 [Memory-Dream](https://github.com/wavmson/openclaw-skill-memory-dream) 是互补的两个 Skill：

| Skill | 时机 | 职责 |
|-------|------|------|
| **Smart Compact** | 实时（压缩前） | 从对话中抢救信息 → 写入日记文件 |
| **Memory-Dream** | 定期（每天凌晨） | 把日记整合到长期记忆 → 更新 MEMORY.md |

两者组成完整的**记忆保护链条**：

```
对话进行中 ──→ Smart Compact 保护信息 ──→ 写入日记
                                            ↓
长期记忆 ←── Memory-Dream 整合 ←────── 日记积累
```

推荐配置：
- Smart Compact：每次 `/compact` 前手动触发
- Memory-Dream：每天凌晨 3 点 Cron 自动执行

### 注意事项

- ⚠️ 对话中工具调用越多，扫描阶段越耗时
- ⚠️ 建议使用 128k+ context 的模型以获得最佳效果
- ⚠️ 首次使用时建议先用"压缩检查"模式熟悉流程
- ⚠️ 不会修改对话历史本身，只读取并提取信息

---

## English

### What is this?

As AI Agent conversations grow longer, context windows fill up and token costs skyrocket. Context compaction is essential, but OpenClaw's native `/compact` compresses everything at once — **valuable details get lost** in the process.

Have you ever experienced these frustrations?
- Agent forgot the API endpoint you just debugged after compaction
- Config file paths, IPs, and port numbers all vanished
- A bug you already solved? Agent hits the same wall again
- Made a decision for good reasons? After compaction, the reasons are gone

**Smart Compact** inserts a "pre-processing" phase before `/compact`: **rescue important information first, write it to memory files, confirm safety, then compress**.

### Core Philosophy: Rescue Before Compress

Traditional compaction is a blunt instrument. Smart Compact uses a **4-phase progressive strategy**:

```
Phase 1: Scan → Phase 2: Extract → Phase 3: Check → Phase 4: Compact
```

Each phase has a clear responsibility, ensuring no information is accidentally lost during compression.

### Install

**Option A (recommended): Via ClawHub**

```bash
clawhub install smart-compact
```

**Option B: Clone from GitHub**

```bash
git clone https://github.com/wavmson/openclaw-skill-smart-compact.git \
  ~/.openclaw/skills/smart-compact
```

**Option C: Copy core file only**

```bash
mkdir -p ~/.openclaw/skills/smart-compact
curl -o ~/.openclaw/skills/smart-compact/SKILL.md \
  https://raw.githubusercontent.com/wavmson/openclaw-skill-smart-compact/main/SKILL.md
```

Then restart Gateway:

```bash
openclaw gateway restart
```

### Usage

Say any of these trigger phrases to your agent:

| Trigger | Description |
|---------|-------------|
| `smart-compact` | Run full 4-phase flow |
| `pre-compact` | Same as smart-compact |
| `compact check` | Check only, don't compress |
| `智能压缩` | Chinese trigger |
| `压缩检查` | Chinese check-only trigger |

### The 4 Phases Explained

#### Phase 1: Scan

Reviews all tool call results in the current conversation (`exec`, `read`, `web_fetch`, `web_search`, etc.) and identifies:

- **Large outputs**: Tool results exceeding 50 lines or 2000 characters
- **Key information**: Config values, IP addresses, API endpoints, file paths, auth tokens
- **Reference status**: Whether the info has been referenced or summarized later in conversation
- **Redundancy**: Repeated `ls`, `git status`, or similar outputs

#### Phase 2: Extract

Extracts durable information from tool outputs and conversation, categorized and written to `memory/YYYY-MM-DD.md`:

- 🔵 **New facts**: IP addresses, ports, file paths, API endpoints
- 🟡 **Decision records**: Why option A was chosen over B, with reasoning
- 🔴 **Error solutions**: Error messages and their fixes
- 🟢 **User preferences**: Explicitly stated likes or requirements
- 🟣 **Task progress**: What's done, what's in progress

Writing rules:
- **Append-only** — never overwrites existing content
- Each memory includes a brief source note
- Sensitive info (认证令牌s) is redacted

#### Phase 3: Check

Generates a structured pre-compact checklist:

```
📋 Smart Compact Checklist
━━━━━━━━━━━━━━━━━━━━━━

📊 Scan Statistics:
- Total tool calls: 23
- Large outputs (>50 lines): 5
- Already referenced/summarized: 3
- Safe to compress: 4

💾 Extracted to Memory:
- [+] Docker container port config 18060
- [+] GitHub push access configured
- [+] XiaoHongShu post content limit 1000 chars
(3 items written to memory/2026-04-02.md)

⚠️ Attention:
- [!] exec output contains API response not yet referenced

✅ Recommendation: Safe to execute /compact
```

#### Phase 4: Compact

- If checklist shows ✅, prompts user for confirmation
- Only executes `/compact` after explicit user approval
- If ⚠️ warnings exist, suggests resolving them first
- **Never auto-compacts** — requires explicit user consent

### Design Principles

| Principle | Description |
|-----------|-------------|
| 🛡️ Rescue first | Better to over-save than to miss something |
| 📝 Append-only | Never overwrites existing memory content |
| 🔒 No auto-compact | Requires explicit user confirmation |
| 👁️ Full transparency | Detailed reports and stats at every step |
| 🔑 Security first | Sensitive info is redacted, auth info never leaked |
| ♻️ Idempotent | Running twice produces no side effects |

### Information Classification

| Category | Action | Examples |
|----------|--------|----------|
| 🔴 Must save | Write to memory | 认证令牌s, IPs, config values, error solutions |
| 🟡 Should save | Write to memory | Decision reasons, user preferences, task progress |
| 🟢 Safe to discard | Mark as safe | Repeated ls output, already-summarized search results |

### Works with Memory-Dream

Smart Compact and [Memory-Dream](https://github.com/wavmson/openclaw-skill-memory-dream) are complementary skills:

| Skill | Timing | Role |
|-------|--------|------|
| **Smart Compact** | Real-time (before compaction) | Rescue info from conversation → write to daily logs |
| **Memory-Dream** | Periodic (daily, e.g. 3 AM) | Consolidate daily logs → update MEMORY.md |

Together they form a complete **memory protection chain**:

```
Active conversation ──→ Smart Compact rescues info ──→ daily logs
                                                          ↓
Long-term memory ←── Memory-Dream consolidates ←── accumulated logs
```

Recommended setup:
- Smart Compact: Trigger manually before each `/compact`
- Memory-Dream: Run via Cron daily at 3 AM

### Notes

- ⚠️ More tool calls = longer scan phase
- ⚠️ Best results with 128k+ context window models
- ⚠️ Try "compact check" mode first to get familiar
- ⚠️ Read-only — does not modify conversation history, only reads and extracts

---

## License

MIT — See [LICENSE](LICENSE)

## Author

[@wavmson](https://github.com/wavmson)
