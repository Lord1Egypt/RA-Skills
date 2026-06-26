# 🌙 Memory-Dream — 记忆整理 Skill

> 像人类 REM 睡眠一样，定期扫描日记、整合记忆、清理过时信息。让你的 AI Agent 拥有持续进化的长期记忆。

---

## 中文说明

### 这是什么？

你的 OpenClaw Agent 每天对话会产生日记文件（`memory/YYYY-MM-DD.md`），时间一长：

- 📈 **日记越堆越多**（轻松 20+ 个文件，几千行）
- 🧊 **长期记忆过时**（`MEMORY.md` 只在压缩时被动更新，跟不上变化）
- 🔄 **信息被埋没**（重要事实散落在旧日记里，Agent 再也不会回头看）
- 🤔 **新会话懵圈**（带着过时的记忆上岗，重复问同样的问题）

**Memory-Dream 就像人类的"做梦"** —— 模拟 REM 睡眠期间的记忆整合机制，定期扫描近期日记，把重要的新信息合并到长期记忆里，过时的信息修正掉。

### 安装方法

**方式一（推荐）：通过 ClawHub**

```bash
clawhub install memory-dream
```

**方式二：从 GitHub 克隆**

```bash
git clone https://github.com/wavmson/openclaw-skill-memory-dream.git \
  ~/.openclaw/skills/memory-dream
```

**方式三：只复制核心文件**

```bash
mkdir -p ~/.openclaw/skills/memory-dream
curl -o ~/.openclaw/skills/memory-dream/SKILL.md \
  https://raw.githubusercontent.com/wavmson/openclaw-skill-memory-dream/main/SKILL.md
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 使用方法

**手动触发** — 直接跟 Agent 说：

| 触发词 | 说明 |
|--------|------|
| `做梦` | 中文触发 |
| `dream` | 英文触发 |
| `整理记忆` | 中文触发 |
| `记忆整合` | 中文触发 |
| `consolidate memory` | 英文触发 |

**自动执行（推荐）** — 设定每天凌晨 3 点自动做梦：

```
/cron add --schedule "0 3 * * *" --task "Execute dream skill: consolidate memory" --label dream-nightly
```

**Heartbeat 集成** — 在 `HEARTBEAT.md` 中添加：

```markdown
- [ ] 如果 memory/ 文件数 >20 或总行数 >3000，执行 dream skill
```

### 五阶段执行流程

```
阶段一「盘点」 → 阶段二「扫描」 → 阶段三「合并」 → 阶段四「标记」 → 阶段五「报告」
```

#### 阶段一：盘点（Orient）

清点家底：
- 列出所有 `memory/*.md` 文件
- 读取当前 `MEMORY.md` 的结构和内容
- 统计：总文件数、总行数、最近 7 天的文件

#### 阶段二：扫描（Scan）

读取**最近 7 天**的 `memory/YYYY-MM-DD.md` 文件，提取：
- 🔵 **新事实**：`MEMORY.md` 中还没有的信息
- 🔴 **矛盾信息**：与 `MEMORY.md` 现有内容冲突的（需要修正）
- 🟡 **重复主题**：多次出现说明很重要，需要强化

**节省 Token**：只读 7 天以内的文件，大文件截取前 200 行。

#### 阶段三：合并（Merge）

精准编辑 `MEMORY.md`：
- ➕ **新增**：添加新发现的事实、偏好、配置
- ✏️ **修正**：更新过时或矛盾的信息
- 🔀 **去重**：合并重复的条目
- 🧹 **清理**：移除已确认无效的旧信息

**关键原则**：使用 `edit`（精准编辑），**绝不整体覆盖** `MEMORY.md`。

#### 阶段四：标记（Mark）

给 30 天以上的旧日记打上"已整合"标签：
- 在文件顶部添加 `<!-- dream-consolidated: YYYY-MM-DD -->`
- **绝不删除任何文件**——只标记，不销毁

#### 阶段五：报告（Report）

输出结构化的整合报告：

```
🌙 Dream complete
━━━━━━━━━━━━━━━━

📊 扫描统计：
- 扫描日记：19 个文件（共 2877 行）
- 新发现事实：8 条
- 矛盾需修正：1 条
- 重复主题：3 个

💾 MEMORY.md 更新：
- [+] 新增 8 个章节
- [~] 修正 1 条过时信息
- [-] 清理 0 条无效条目

📝 标记归档：
- 标记 12 个超过 30 天的旧日记

💡 建议：
- 考虑归档 2026-03-01 之前的文件
```

### 设计原则

| 原则 | 说明 |
|------|------|
| 🛡️ 保守策略 | 拿不准就保留，宁多勿删 |
| ✏️ 精准编辑 | 用 edit 逐条修改，绝不 overwrite 整个文件 |
| 💰 省 Token | 只读最近 7 天，大文件截取前 200 行 |
| 🔒 安全 | 绝不删除文件，绝不在报告里暴露密钥 |
| ♻️ 幂等 | 跑两次结果一样，不会产生副作用 |
| 📊 透明 | 每次执行都输出详细报告 |

### 与 Smart Compact 搭配使用

Memory-Dream 和 [Smart Compact](https://github.com/wavmson/openclaw-skill-smart-compact) 是互补的两个 Skill：

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

- ⚠️ 建议使用 128k+ context 的模型以获得最佳效果
- ⚠️ 推荐每天凌晨自动执行一次（避免白天占用对话 token）
- ⚠️ 首次运行如果积累了大量日记文件，执行时间会较长
- ⚠️ 不会修改日记文件内容，只读取并提取信息
- ⚠️ `MEMORY.md` 文件建议控制在 500 行以内

### 常见问题

**Q: 多久跑一次比较好？**
A: 推荐每天一次。如果对话很频繁，可以每 12 小时一次。

**Q: 会不会把重要信息删掉？**
A: 不会。设计原则是"宁多勿删"，拿不准的信息一定保留。

**Q: 支持什么模型？**
A: 所有模型都支持，但推荐 128k+ context 窗口的模型效果最佳。

**Q: 能和 Smart Compact 一起用吗？**
A: 强烈推荐！Smart Compact 负责实时保护，Memory-Dream 负责定期整合，形成完整的记忆保护链。

---

## English

### The Problem

OpenClaw agents accumulate daily memory files (`memory/YYYY-MM-DD.md`) through conversations. Over time:

- 📈 **Daily files pile up** — easily 20+ files with thousands of lines
- 🧊 **Long-term memory stales** — `MEMORY.md` only updates during compaction flushes
- 🔄 **Information gets buried** — important facts lost in old daily logs the agent never re-reads
- 🤔 **New sessions start confused** — agent works with outdated context, asks the same questions again

### The Solution

Memory-Dream simulates the brain's REM sleep memory consolidation process. It runs a structured 5-phase process to keep your agent's long-term memory fresh and accurate:

```
Daily journals ──▶ Memory-Dream ──▶ Updated MEMORY.md
(raw, verbose)     (scan + merge)   (curated, compact)
```

It scans recent daily files, extracts what matters, and surgically updates `MEMORY.md` — adding new facts, correcting outdated ones, and removing obsolete entries.

### Install

**Option A (recommended): Via ClawHub**

```bash
clawhub install memory-dream
```

**Option B: Clone from GitHub**

```bash
git clone https://github.com/wavmson/openclaw-skill-memory-dream.git \
  ~/.openclaw/skills/memory-dream
```

**Option C: Copy core file only**

```bash
mkdir -p ~/.openclaw/skills/memory-dream
curl -o ~/.openclaw/skills/memory-dream/SKILL.md \
  https://raw.githubusercontent.com/wavmson/openclaw-skill-memory-dream/main/SKILL.md
```

Then restart Gateway:

```bash
openclaw gateway restart
```

### Usage

**Manual trigger** — Tell your agent:

| Trigger | Description |
|---------|-------------|
| `dream` | Run full consolidation |
| `做梦` | Chinese trigger |
| `consolidate memory` | Explicit trigger |
| `整理记忆` | Chinese explicit trigger |
| `memory consolidation` | English trigger |

**Automatic (recommended)** — Set up a nightly cron:

```
/cron add --schedule "0 3 * * *" --task "Execute dream skill: consolidate memory" --label dream-nightly
```

**Heartbeat integration** — Add to your `HEARTBEAT.md`:

```markdown
- [ ] If memory/ has >20 files or >3000 total lines, run dream skill
```

### The 5 Phases

```
Phase 1: Orient → Phase 2: Scan → Phase 3: Merge → Phase 4: Mark → Phase 5: Report
```

#### Phase 1: Orient

Take inventory:
- List all `memory/*.md` files
- Read current `MEMORY.md` structure and content
- Stats: total files, total lines, files from last 7 days

#### Phase 2: Scan

Read the **last 7 days** of `memory/YYYY-MM-DD.md` files, extract:
- 🔵 **New facts**: Information not yet in `MEMORY.md`
- 🔴 **Contradictions**: Conflicts with existing long-term memory (needs correction)
- 🟡 **Recurring themes**: Appeared multiple times = important, needs emphasis

**Token-efficient**: Only reads 7-day window, caps large files at 200 lines.

#### Phase 3: Merge

Surgically edit `MEMORY.md`:
- ➕ **Add**: New facts, preferences, configurations
- ✏️ **Correct**: Outdated or contradicting information
- 🔀 **Deduplicate**: Merge repeated entries
- 🧹 **Prune**: Remove confirmed-invalid old entries

**Key principle**: Uses precise `edit` operations, **never overwrites** the entire file.

#### Phase 4: Mark

Tag old daily logs (>30 days) as consolidated:
- Adds `<!-- dream-consolidated: YYYY-MM-DD -->` at file top
- **Never deletes any file** — mark only, never destroy

#### Phase 5: Report

Outputs a structured consolidation report:

```
🌙 Dream complete
━━━━━━━━━━━━━━━━

📊 Scan Stats:
- Scanned: 19 daily files (2877 lines total)
- New discoveries: 8
- Contradictions fixed: 1
- Recurring themes: 3

💾 MEMORY.md Updates:
- [+] 8 sections added
- [~] 1 outdated entry corrected
- [-] 0 invalid entries pruned

📝 Archives:
- Marked 12 daily files older than 30 days

💡 Suggestions:
- Consider archiving files before 2026-03-01
```

### Design Principles

| Principle | Description |
|-----------|-------------|
| 🛡️ Conservative | When unsure, keeps info rather than removing |
| ✏️ Surgical edits | Precise line-by-line edits, never full-file overwrite |
| 💰 Token-efficient | Only reads last 7 days, caps large files at 200 lines |
| 🔒 Safe | Never deletes files, never exposes secrets in reports |
| ♻️ Idempotent | Running twice produces the same result |
| 📊 Transparent | Detailed report output after every run |

### Works with Smart Compact

Memory-Dream and [Smart Compact](https://github.com/wavmson/openclaw-skill-smart-compact) are complementary skills:

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

### FAQ

**Q: How often should I run it?**
A: Once daily is recommended. If you have very active conversations, every 12 hours works too.

**Q: Will it delete important information?**
A: No. The core design principle is "when in doubt, keep it." Uncertain information is always preserved.

**Q: What models are supported?**
A: All models work, but 128k+ context window models give the best results.

**Q: Can I use it with Smart Compact?**
A: Strongly recommended! Smart Compact handles real-time protection, Memory-Dream handles periodic consolidation — a complete memory safety net.

### Notes

- ⚠️ Recommended: 128k+ context window model for best results
- ⚠️ Best run during off-hours (e.g. 3 AM) to avoid using conversation tokens
- ⚠️ First run may take longer if many daily files have accumulated
- ⚠️ Read-only on daily files — only reads and extracts, never modifies source
- ⚠️ Keep `MEMORY.md` under 500 lines for optimal performance

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) (any version with Skill support)
- A workspace with `MEMORY.md` and `memory/` directory (standard OpenClaw layout)
- Works with any model (no model-specific features)

## File Structure

```
memory-dream/
├── SKILL.md          # Skill definition (required by OpenClaw)
├── README.md         # This file
└── LICENSE           # MIT License
```

## License

MIT — Use it, fork it, improve it.

## Contributing

PRs welcome! Ideas for improvement:

- [ ] Memory health dashboard script
- [ ] Topic-based memory files (not just chronological)
- [ ] Conflict resolution strategies for contradicting memories
- [ ] Integration with OpenClaw's upcoming persistent memory features

---

*"We are such stuff as dreams are made on, and our little life is rounded with a sleep."* — Shakespeare

## Author

[@wavmson](https://github.com/wavmson)
