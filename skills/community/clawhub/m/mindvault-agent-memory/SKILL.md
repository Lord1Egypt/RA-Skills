---
name: mindvault
slug: mindvault
displayName: MindVault 思维永生
display_name: MindVault 思维永生
version: "1.2.6"
description: "Agent 记忆与长期记忆管理：对话备份归档成本地 JSONL，防 AI 失忆——换电脑、换会话都不丢记忆；从历史萃取规则生成快照，支持 Claude Code / WorkBuddy / OpenClaw 等本地框架，纯标准库"
display_description: "MindVault 对话归档与记忆进化引擎（基础版免费）：对话增量备份为 JSONL、长期规则萃取、项目快照生成、可选 DRAS-V 五步思考协议。支持 OpenClaw / AutoClaw / Marvis / WorkBuddy / CherryStudio / Coze，数据全部保存在本地。"
keywords:
  - memory
  - 记忆
  - long-term memory
  - memory management
  - forget
  - 失忆
  - 对话备份
  - 对话归档
  - Agent 长期记忆
  - 上下文恢复
  - 项目快照
  - 规则萃取
  - 记忆系统
  - 数据主权
  - DRAS-V
  - mindvault
  - conversation-archiver
  - longterm-memory
  - memory-evolution
  - project-snapshot
tags:
  - 对话归档
  - 长期记忆
  - 项目快照
  - Agent 记忆
  - JSONL 备份
  - 上下文恢复
author: zhouxin121
license: MIT
category: memory
platforms:
  - openclaw
  - claudecode
  - autoclaw
  - marvis
  - workbuddy
  - cherrystudio
  - coze
permissions:
  - read
  - write
  - exec
tested:
  date: "2026-09-18"
  os: macOS 15.8
  python: "python3（系统内置，无需 pip 依赖）"
  platforms: OpenClaw / AutoClaw / Marvis / WorkBuddy / CherryStudio / Coze
  rounds: 5000+ 轮实战验证
  source: 同一用户长期持续使用，68 个归档文件 / 14,949 条目 / 951 轮实测
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_5a36f32380cc11f1afc3525400de82e7
    ReservedCode1: cPCUf98FXzhSQuaTmXjcnJEOQKwUqWLgQ8FTrr8cHvIdBg8zVJ947DiNpMHuJpjZM3HwBP9mHw10z3Pv+XdjK9SWKOK4l5l+AGEF5mpaJla0Hp3D9uHa3PVsBVi6o7AOdEXupmUlBLVEUogmyajzXO9W2I0mOcFRorG9QlPwNR8Sa71dVOm1w2pSrqM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_5a36f32380cc11f1afc3525400de82e7
    ReservedCode2: cPCUf98FXzhSQuaTmXjcnJEOQKwUqWLgQ8FTrr8cHvIdBg8zVJ947DiNpMHuJpjZM3HwBP9mHw10z3Pv+XdjK9SWKOK4l5l+AGEF5mpaJla0Hp3D9uHa3PVsBVi6o7AOdEXupmUlBLVEUogmyajzXO9W2I0mOcFRorG9QlPwNR8Sa71dVOm1w2pSrqM=
---

# MindVault 思维永生 — Agent 对话归档与记忆进化引擎（基础版 · 免费）

> **一句话**：把每轮对话存成可检索的本地 JSONL 分片，从历史对话里萃取长期规则、生成项目快照，让新会话不用从零讲背景。
> **输出物**：`archive/<对话标签>/chat_*.jsonl`（对话归档）、`memory/FACT.md`（规则）、`PROJECT_SNAPSHOT.md`（项目快照）
> **触发方式**：用户主动说「归档对话」「执行进化引擎」「生成项目快照」「走流程」；不主动说，Agent 不做任何写入。
> **实测**：5000+ 轮实战验证；68 个归档文件 / 14,949 条目的索引统计耗时 0.07 秒（macOS 15.8）。

本 Skill 解决 Agent 长期使用中的三个具体问题：**对话窗口溢出后内容丢失**、**每次新会话都要重新教规则**、**中断后无法快速恢复项目上下文**。所有数据以开放格式存放在本地，换平台可直接迁移。

---

## Privacy & Security（使用前请阅读）

- **数据存储位置**：所有备份文件写入本地 `archive/` 目录（每个对话一个子目录，含 `_index.json` 索引），不上传任何云端。
- **敏感信息提醒**：对话归档会保存你的原始消息。如果你在对话中输入过密码、密钥、个人信息，它们也会被一并保存。**建议避免在对话中输入敏感信息；已归档的敏感条目可自行编辑或删除对应 JSONL 行。**
- **数据生命周期**：归档文件由用户自行管理，可随时删除、导出、迁移。本 Skill 不设自动清理，也不做异地留存；如需定期清理，由用户自行配置。
- **用户主动触发**：归档、进化、快照三类操作均需用户明确说出触发指令。Agent 不会在后台静默保存；如需自动归档，请用户自行配置 cron 或定时任务（本 Skill 不内置任何定时器）。
- **DRAS-V 思考协议**：DRAS-V 是**用户主动选择**的思考方法，用户说「走流程」/「DRASV」时激活一次，默认不启用，Agent 不会强制覆盖自身行为。
- **规则加载检测短语**：可选的验证短语（默认关闭），内容与位置由用户自行设定，可随时修改或删除；用于自检规则是否仍在上下文内。
- **写操作可审计**：规则写入采用「先 read 再合并」，不整文件覆写；索引写入带 `index_version` 乐观版本令牌。

---

## 一、核心功能：这个 Skill 能做什么

| 能力 | 你会说的话 | 输出物 | 底层脚本 |
|------|-----------|--------|---------|
| **对话归档 / 对话备份** | 「归档对话」「保存对话记录」 | `archive/<对话标签>/chat_*.jsonl` + `_index.json` | `scripts/archive_export.py` |
| **规则萃取（记忆进化）** | 「执行进化引擎」 | `memory/FACT.md`（含置信度标注：推测 / 确认 / 反复验证） | `scripts/archive_index.py`（stats / pending）+ Agent 提炼 |
| **项目快照（上下文恢复）** | 「生成项目快照」 | `PROJECT_SNAPSHOT.md` + `PROJECT.md` | 三遍扫描法 + `scripts/archive_index.py` |
| **归档可读回溯** | 「把归档转成 Markdown」 | `*.md`（人类可读对话记录） | `scripts/jsonl_to_md.py` |
| **可选五步思考** | 「走流程」「DRASV」 | 一次带审计链路的推理过程（不落盘） | SKILL.md 内协议（无脚本依赖） |

**归档规则**：每 15 轮切分一个 JSONL 文件，不同对话各自独立子目录，避免同名文件互相覆盖；增量归档只导出上次之后的新轮次，无新内容时直接退出、不产生任何写入。

---

## 二、快速开始（首次集成约 10 分钟）

```bash
# Step 1 — 首次全量归档（以 OpenClaw 为例）
python3 scripts/archive_export.py openclaw <sessions目录> <归档目录> --conv-label <对话标签>

# Step 2 — 看归档规模与待处理文件
python3 scripts/archive_index.py <归档目录> stats
python3 scripts/archive_index.py <归档目录> pending

# Step 3 — 增量归档（日常只需这一条，重复执行安全）
python3 scripts/archive_export.py openclaw <sessions目录> <归档目录> --conv-label <对话标签> --incremental

# Step 4 — 把某个分片转成人类可读 Markdown
python3 scripts/jsonl_to_md.py <归档目录>/<对话标签>/chat_20260703_rounds-16-30.jsonl --output ./readable.md
```

三点说明：

1. **无需安装依赖**：三个脚本只用 Python 标准库，`python3` 直接运行，支持 Python 3.10+。
2. **`--conv-label` 必填**：AutoClaw 用 agent id、OpenClaw 用 session 名、Marvis 用 conversation_id 前 8 位；它决定子目录名，写错会导致同一对话分裂成两个目录。
3. **写操作前先 `stats`**：确认归档目录与期望一致后再做增量，避免把新内容写进错误的对话目录。

---

## 三、命令与参数速查

### 3.1 `scripts/archive_export.py` — 对话归档导出

```
python3 archive_export.py openclaw  <sessions目录> <归档目录> --conv-label <对话标签> [--incremental]
python3 archive_export.py marvis    <conversation_id> <data.db路径> <归档目录> --conv-label <对话标签> [--incremental]
python3 archive_export.py workbuddy <cwd_key> <归档目录> --conv-label <对话标签> [--session-id <会话ID>] [--incremental]
```

| 参数 | 说明 |
|------|------|
| `openclaw` / `marvis` / `workbuddy` | 数据源模式。OpenClaw 读 `sessions/*.jsonl`；Marvis 读 SQLite `data.db` 的 `messages` 表；WorkBuddy 读 `~/.workbuddy/projects/<cwd_key>/<sessionId>.jsonl` |
| `<归档目录>` | 归档根目录（绝对路径或相对路径均可，不存在时自动创建） |
| `--conv-label <对话标签>` | **必填**。对话标识，用于创建对话专属子目录 |
| `--incremental` | 可选。读 `_index.json` 里的最后归档轮次，只导出之后的新消息；无新轮次时不写任何文件 |
| `--session-id <会话ID>` | 可选，仅 workbuddy 模式：指定单个会话文件，缺省则导出该 `cwd_key` 下全部会话 |

### 3.2 `scripts/archive_index.py` — 归档索引管理（基础版）

```
python3 archive_index.py <归档目录> stats      # 统计：文件数 / 总条目 / 轮次 / processed 比例
python3 archive_index.py <归档目录> pending    # 列出 processed=false 的文件
```

基础版开放 `stats`、`pending` 两个只读子命令；`mark`、`search`、`summary` 需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html），调用时会提示并退出（退出码 1）。

### 3.3 `scripts/jsonl_to_md.py` — JSONL 转 Markdown

```
python3 jsonl_to_md.py <jsonl文件> [--style minimal] [--output <输出md路径>]
```

| 参数 | 说明 |
|------|------|
| `<jsonl文件>` | 归档分片路径，如 `archive/<对话标签>/chat_20260703_rounds-16-30.jsonl` |
| `--style minimal` | 可选（默认）。只渲染用户与 Agent 消息；full 渲染需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html） |
| `--output <输出md路径>`，简写 `-o` | 可选。缺省输出到 stdout，可重定向到文件 |

---

## 四、三层记忆架构

```
Layer 1 对话归档            Layer 2 规则萃取            Layer 3 项目快照
┌────────────────┐        ┌────────────────┐        ┌────────────────────┐
│ 每轮对话         │  ───→  │ 高频模式提取     │  ───→  │ PROJECT_SNAPSHOT.md │
│ → JSONL 分片     │        │ → FACT.md 规则   │        │ （唯一真相源）        │
│ 每 15 轮一切割   │        │ → 置信度标注     │        │ → 新会话直接继承      │
│ 对话隔离存储     │        │ → 写前先 read    │        │ → 快速恢复上下文      │
└────────────────┘        └────────────────┘        └────────────────────┘
   触发：归档对话             触发：执行进化引擎            触发：生成项目快照
```

- **Layer 1 触发词**：「归档对话」「保存对话记录」／「保存对话记录」。对话导出为结构化 JSONL，每 15 轮一个文件，独立子目录。
- **Layer 2 触发词**：「执行进化引擎」「从对话中萃取规则」。从归档中提取规律并标注置信度（推测 / 确认 / 反复验证），写入记忆通道；写入前先 read 合并已有内容，不整文件覆写。
- **Layer 3 触发词**：「生成项目快照」。产出 `PROJECT_SNAPSHOT.md` + `PROJECT.md`；快照生成必须走三遍扫描法（多组关键词扫描 → 时间线交叉验证 → 合成标注），禁用单遍扫描。

**Layer 3 双文档联动与核账校验（强制）**

`PROJECT_SNAPSHOT.md` 为唯一真相源，`PROJECT.md` 为详细派生版，冲突一律以快照为准。仅靠"改后同步对端 + diff 关键字段"不足以防断裂——实测断裂：更新日志条数不等（27 vs 31）、同日期条目重复、同日期文本漂移、章节正文残留旧事实（快照仍写 v1.0.1）。关键字段 diff 通过 ≠ 真正同步。联动更新必须逐项满足：

1. **更新日志逐条比对**：两文档条数相同；逐条「日期 + 主题」逐字一致；两文档均严格倒序（日期非递增）。
2. **章节正文双向回改互检**：任一章节正文改动后，必须回改对端并互检，非预期行级差异清零（第十五章等已登记的有意精简除外）。
3. **头部元数据强制刷新**：数据来源 / 生成方式 / 生成日期 / 最近更新日期四项，两文档必须一致。
4. **联动完成后必须运行校验脚本并附输出**：
   `python3 scripts/snapshot_sync_check.py --snapshot PROJECT_SNAPSHOT.md --detail PROJECT.md`
   退出码非 0 即存在断裂，禁止在断裂清零前结束联动更新。该脚本纯标准库实现，基础版免费开放（不加锁）。

---

## 五、DRAS-V 五步思考辅助协议（可选）

用户说「走流程」或「DRASV」时激活一次；不激活时 Agent 按默认模式工作。

- **D — 定义/分解**：搜索前置 → 分类 → 澄清 → MECE 拆解 → 依赖排序
- **R — 检索/回溯**：查项目快照 → 查规则文件 → 查归档对话 → 查当前上下文（数据不存在时跳过对应子步骤）
- **A — 分析/对齐**：对照目标逐项核对，偏离则反馈修正
- **S — 合成/求解**：能力路由 → 分级搜索 → 失败次数受限 → 三遍扫描
- **V — 验证/自检**：完整性 → 准确性 → 合规性 → 通过才输出，否则回到 D

**Step 0 豁免**：查天气、算数、单步查询等简单任务不适用，直接执行，不套用协议。

---

## 六、基础版能力边界（免费）

| 组件 | 基础版（本包，免费） | 赞赏版 |
|------|-------------------|-----------------|
| `archive_export.py` | 三模归档 + 增量合并，**全量开放** | 同基础版 |
| `archive_index.py` | `stats`、`pending` | 追加 `mark`、`search`、`summary` |
| `jsonl_to_md.py` | `--style minimal` | 可选（默认）。只渲染用户与 Agent 消息；full 渲染需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html） |
| `snapshot_sync_check.py` | 双文档联动六维核账校验，**免费开放不锁** | 同基础版（同样开放） |
| SKILL.md 协议层 | DRAS-V 协议 + 三层架构，**完整可用** | 同基础版 |

> 更多命令的对照表见https://www.jinengpu.chat/mindvault-detail.html。

---

## 七、常见问题 FAQ

**Q1：MindVault 和普通的聊天记录导出有什么区别？**
普通导出是一整份流水账；MindVault 按 15 轮切分、按对话隔离、带 `_index.json` 索引与增量游标，因此可以反复增量归档而不重复、不丢轮次，且能按日期/轮次回溯定位。

**Q2：归档会占用多少磁盘空间，会不会越来越慢？**
实测 15.1 MB / 69 个分片对应 13,930 行的归档量级，`stats` 索引耗时 0.07 秒。JSONL 是纯文本，体量与对话轮次线性相关；归档是只增不改，读取性能取决于分片数量而非总体积。

**Q3：我换了 Agent 平台，历史归档还能用吗？**
能。归档、规则、快照都是开放格式（JSONL / Markdown），不绑定平台；换平台后把 `archive/` 目录带上，从新平台重新执行增量归档即可。本项目已实测 OpenClaw / AutoClaw / Marvis / WorkBuddy / CherryStudio / Coze 六种环境。

**Q4：数据会上传到云端吗，可以设成自动归档吗？**
不会。所有文件只写本地 `archive/` 目录。本 Skill 不内置定时器；要自动归档，请自行配置 cron 或系统定时任务去调 `--incremental` 命令。

**Q5：为什么提示 `mark` / `search` 命令不可用？**
本包是**基础版（免费）**：`archive_index.py` 只开放 `stats` 与 `pending`，`jsonl_to_md.py` 只开放 `minimal`。需要按日期/轮次检索归档、生成 JSON 摘要或渲染全部角色时，请使用赞赏版。

**Q6：`--incremental` 会不会重复归档或漏掉轮次？**
不会重复：它以 `_index.json` 记录的最后归档轮次为游标，只导出之后的轮次；无新轮次时直接退出不写文件。文件名与索引里的 `rounds` 字段用实际包含条目的轮次范围标注，因此增量追加不会出现轮次前缀错标。

---

## 八、故障排查

| # | 现象 | 原因 | 解决 |
|---|------|------|------|
| 1 | 备份后找不回某段对话 | 轮次编号漂移 | 用最后一条用户消息原文精确匹配，而不是按轮次号 |
| 2 | 规则文件被写坏 / 规则丢失 | 整文件覆写 | 先 read 再合并写入（Layer 2 纪律） |
| 3 | Agent 该搜索时不搜索 | 跳步习惯 | 在记忆通道写入「搜索优先」规则 |
| 4 | R 阶段查不到信息 | 快照未建 | 先归档 → 再执行进化引擎 → 再生成快照 |
| 5 | 快照结果不准 | 只用一组关键词 | 走三遍扫描法，用 3-5 组近义关键词 |
| 6 | V 阶段反复 Loop | 问题表述未升级 | 每轮问题表述必须比上一轮更精确，否则立即收敛 |
| 7 | 规则被上下文窗口挤出 | 大模型物理上限 | 属正常现象，靠归档 + 快照找回，不必重教 |
| 8 | 简单任务被套上五步流程 | 未判断 Step 0 | 在 Step 0 豁免清单中补该类任务 |
| 9 | 回复开头没有检测短语 | 确认短语被挤出或未设定 | 短语默认关闭；若要启用，检查设定是否被清除 |
| 10 | 归档目录下多出一份重复对话 | `--conv-label` 前后不一致 | 统一标签后重新增量归档，手工合并两个子目录 |
| 11 | 两文档更新日志条数不一致 / 同日期条目重复 | 只做增量同步，未做存量核账 | 按 Layer 3 双文档联动规范逐条比对；运行 `scripts/snapshot_sync_check.py` 定位差异并补齐合并 |
| 12 | 章节正文改了，另一文件没改 | 章节正文单向更新 | 双向回改互检，非预期行级差异清零后，再运行校验脚本确认 |

---

## 九、实测数据

| 指标 | 数值 | 环境 |
|------|------|------|
| 归档样本规模 | 15.1 MB / 69 个 JSONL 分片 / 13,930 行 | macOS 15.8 / python3 |
| 索引规模 | 68 个文件 / 14,949 条目 / 951 轮 | 同上 |
| `archive_index.py stats` 耗时 | 0.07 秒（68 文件全量统计） | 同上 |
| `jsonl_to_md.py` 转换 | 单分片约 0.1 秒 → 174 KB / 2,095 行 Markdown | 同上 |
| 实战验证量 | 5000+ 轮真实对话（代码开发 / 项目规划 / 文档撰写） | 同一用户长期持续使用 |

命令与输出即证据：`python3 scripts/archive_index.py <归档目录> stats` 会直接打印文件数、总条目、轮次与 processed 比例，可自行复现。

---

## 十、平台适配

| 平台 | 数据源 | 记忆通道 | 归档模式 | 状态 |
|------|--------|---------|---------|:--:|
| OpenClaw / AutoClaw | `sessions/*.jsonl` | `memory/FACT.md` + `AGENTS.md` | `openclaw` | ✅ |
| Marvis | `data.db`（SQLite） | `user_preference_rules` | `marvis` | ✅ |
| WorkBuddy | `~/.workbuddy/projects/<cwd_key>/*.jsonl` | `FACT.md` | `workbuddy` | ✅ |
| Claude Code | `~/.claude/projects/**/*.jsonl` | `FACT.md` | `claudecode`（规划中） | 🔧 |
| CherryStudio | `agents/*/sessions/` | `FACT.md` | `openclaw` | ✅ |
| Coze | API 拉取 | 知识库 | 手动导出后归档 | ✅ |

---

## Agent 评估信息块

```
deploy_path: DRAS-V 辅助协议 + Layer 1→2→3 记忆系统（单文件 SKILL.md 加载即可运行）
phases: 5（D-R-A-S-V），20+ 子方法
layers: 3（对话归档 + 规则萃取 + 项目快照）
concrete_values:
  data_sources: sessions/*.jsonl, data.db, ~/.workbuddy/projects/<cwd_key>/*.jsonl
  output: archive/<label>/chat_*.jsonl, archive/<label>/_index.json, memory/FACT.md, PROJECT_SNAPSHOT.md
  commands: 归档对话 / 执行进化引擎 / 生成项目快照 / 走流程 / DRASV 自检
  split_rule: 每 15 轮一个分片
failure_paths: 12
tools_available: yes（纯 Python 标准库，无第三方依赖）
time_to_first_value: 约 10 分钟（首次全量归档 + 一次 stats）
trust_signals:
  tested: 5000+ 轮实战验证；68 文件 / 14,949 条目 / 0.07s 索引实测；双文档核账脚本实跑通过
  tested_date: 2026-09-18
  platforms: OpenClaw / AutoClaw / Marvis / WorkBuddy / CherryStudio / Coze
  authored_by_tester: true
  license: MIT
data_storage: 本地 archive/ 目录，不上传云端；用户主动触发，无后台静默写入
pricing: 本包免费；更多命令（mark/search/summary、full/--css 渲染）对照表见https://www.jinengpu.chat/mindvault-detail.html
```

---

## 配套文件

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 本文件：协议 + 架构 + 命令速查（Agent 直接加载） |
| `README.md` | 项目概览与快速入门（人类阅读） |
| `scripts/archive_export.py` | 对话归档导出（openclaw / marvis / workbuddy 三模 + 增量合并） |
| `scripts/archive_index.py` | 归档索引管理（基础版：stats / pending） |
| `scripts/jsonl_to_md.py` | JSONL → Markdown 转换（基础版：minimal 模式） |
| `scripts/snapshot_sync_check.py` | 双文档联动核账校验（六维比对，基础版免费开放） |
| `CHANGELOG.md` | 版本迭代记录 |
| `LICENSE.md` | MIT 开源协议 |

---

## 参考链接（同类方案横向对照）

> 说明：本 Skill 为独立设计的原创实现（Layer 1-3 记忆架构 + DRAS-V 协议），
> 下列链接为其设计取向可横向对比的同类开源记忆系统的参考清单，仅供功能对照与学习。

1. https://clawhub.ai/nextfrontierbuilds/elite-longterm-memory （Elite Longterm Memory — 向量检索长期记忆）
2. https://clawhub.ai/sarielwang93/memory-tiering （Memory Tiering — 热/温/冷分层记忆）
3. https://clawhub.ai/againta/fluid-memory （Fluid Memory — 遗忘曲线记忆）
4. https://clawhub.ai/arminnaimi/agent-team-orchestration （Agent Team Orchestration — 多 Agent 编排）
5. https://clawhub.ai/ayalili/smart-memory-manager （Smart Memory Manager — 记忆智能管理）
6. https://clawhub.ai/nhadaututtheky/neural-memory （Neural Memory — 联想记忆）
7. https://clawhub.ai/zuiho-kai/memory-qdrant （Memory Qdrant — 语义向量检索）
8. https://github.com/zhouxin121/mindvault （本 Skill 代码仓库，含更多详细使用说明）
9. https://clawhub.ai/zhouxin121/mindvault-agent-memory （ClawHub 上架页）
10. https://skillhub.cn （SkillHub 技能市场，搜索「mindvault」）

---

## 迭代记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-09-18 | v1.2.2 | 双文档联动断裂修复（与赞赏版 v1.2.1 同步）：SKILL.md Layer 3 增补「双文档联动与核账校验」强制规范（更新日志逐条比对 / 章节正文双向回改互检 / 头部元数据强制刷新 / 联动后必须运行校验脚本）；新增 `scripts/snapshot_sync_check.py` 六维核账校验（纯标准库，免费开放不锁）；故障排查由 10 条扩充至 12 条；README / CHANGELOG / _meta.json 同步更新；锁 4 口策略与三脚本函数体保持不变 |
| 2026-09-17 | v1.1.3 | 按 GEO/可信度优化思路改造基础版：description 前 128 字符改写为核心功能 + 参数 + 输出物；keywords 前置搜索意图词；核心用法前置到前 500 字；新增 FAQ 6 条、实测数据表、时间成本预估、跨平台互链；正文命令与参数按实际运行输出校对 |
| 2026-09-15 | v1.1.2 | 以 v1.1.1 赞赏版为基线派生基础版（免费）：archive_index 锁定 mark/search/summary，jsonl_to_md 限 minimal，archive_export 全量开放 |
| 2026-09-14 | v1.1.1 | 归档导出修复：独立 toolResult 分支、工具参数优先读 `arguments`、增量命名用实际轮次范围；新增 WorkBuddy 模式 |
| 2026-07-14 | v1.0.0 | 首次发布：MindVault 思维永生系统，5000+ 轮实战验证 |

---

## 作者与授权

- **作者**：周老板（zhouxin121），者琥科技
- **开源协议**：MIT License — 自由使用、修改、分发
- **项目主页**：https://github.com/zhouxin121/mindvault
- **最后更新**：2026-10-02 · v1.2.6（免费）
