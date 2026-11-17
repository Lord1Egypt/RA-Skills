# MindVault 思维永生
> 📦 **一键安装**：[ClawHub 页面](https://clawhub.ai/zhouxin121/skills/mindvault-agent-memory) · OpenClaw 用户搜索 `mindvault-agent-memory` 直接装
 — Agent 对话归档与记忆进化引擎

> **把你的 Agent 对话存成可检索的本地 JSONL，从历史里萃取规则，新会话不用再从零讲背景。**
> 5000+ 轮实战验证 · 纯本地存储 · 输出 `archive/*.jsonl` + `memory/FACT.md` + `PROJECT_SNAPSHOT.md` · MIT 开源
> 跨平台：OpenClaw / AutoClaw / Marvis / WorkBuddy / CherryStudio / Coze

MindVault 是一套**Agent 对话归档与长期记忆基础设施**，解决 AI Agent 长期使用中的三个具体问题：**对话窗口溢出后内容丢失**、**每次新会话都要重新教规则**、**中断后无法快速恢复项目上下文**。它用三层架构（对话归档 → 规则萃取 → 项目快照）让 Agent 拥有可检索的长期记忆与结构化思考能力，所有数据以开放格式存在本地，换平台可无缝迁移。

---

## 快速开始（3 条命令）

```bash
# 1) 全量归档对话（以 OpenClaw 为例；Marvis 走 data.db，WorkBuddy 走 ~/.workbuddy）
python3 scripts/archive_export.py openclaw <sessions目录> <归档目录> --conv-label <对话标签>

# 2) 查看归档规模与待处理文件
python3 scripts/archive_index.py <归档目录> stats

# 3) 日常增量归档（可反复执行，只导出新轮次）
python3 scripts/archive_export.py openclaw <sessions目录> <归档目录> --conv-label <对话标签> --incremental
```

无第三方依赖，`python3` 标准库即可运行（Python 3.10+）。完整参数与故障排查见 [SKILL.md](SKILL.md)。

---

## 它能做什么

| 能力 | 说明 | 输出物 | 实现 |
|------|------|--------|------|
| **对话归档 / 对话备份** | 每 15 轮切分一个 JSONL，按对话隔离存储，增量归档不重复不丢轮次 | `archive/<标签>/chat_*.jsonl` + `_index.json` | `archive_export.py`（openclaw / marvis / workbuddy 三模） |
| **规则萃取（记忆进化）** | 从历史对话提取偏好规则与项目模式，标注置信度（推测 / 确认 / 反复验证） | `memory/FACT.md` | `archive_index.py` + Agent 提炼 |
| **项目快照（上下文恢复）** | 用三遍扫描法生成项目快照，下次对话直接继承全部背景 | `PROJECT_SNAPSHOT.md` | 三遍扫描法 |
| **归档可读回溯** | JSONL 一键转人类可读 Markdown | `*.md` | `jsonl_to_md.py`（minimal 模式） |
| **可选五步思考** | 说「走流程」/「DRASV」时激活一次完整推理链路，不跳步、可审计 | 推理过程（不落盘） | DRAS-V 协议 |

---

## 技术架构

```
Layer 1 对话归档            Layer 2 规则萃取            Layer 3 项目快照
┌────────────────┐        ┌────────────────┐        ┌────────────────────┐
│ 每轮对话         │  ───→  │ 高频模式提取     │  ───→  │ PROJECT_SNAPSHOT.md │
│ → JSONL 分片     │        │ → FACT.md 规则   │        │ （唯一真相源）        │
│ 每 15 轮一切割   │        │ → 置信度标注     │        │ → 新会话直接继承      │
│ 对话隔离存储     │        │ → 写前先 read    │        │ → 快速恢复上下文      │
└────────────────┘        └────────────────┘        └────────────────────┘
```

---

## 为什么选择 MindVault

- **数据主权**：JSONL / Markdown 开放格式，不绑定任何平台，换平台无缝迁移。
- **可审计**：DRAS-V 协议下每一步工具调用与推理过程可回溯；写操作「先 read 再合并」，不整文件覆写。
- **增量安全**：以 `_index.json` 的轮次游标为界，只导出新内容；无新轮次时不产生任何写入。
- **轻量部署**：单文件 `SKILL.md` 加载即可运行，无需数据库、无需服务器、无需 pip 依赖。
- **实战验证**：5000+ 轮真实对话验证，覆盖代码开发、项目规划、文档撰写等场景。

---

## 实测数据

| 指标 | 数值 | 环境 |
|------|------|------|
| 归档样本规模 | 15.1 MB / 69 个 JSONL 分片 / 13,930 行 | macOS 15.8 / python3 |
| 索引规模 | 68 个文件 / 14,949 条目 / 951 轮 | 同上 |
| `archive_index.py stats` | 0.07 秒（68 文件全量统计） | 同上 |
| `jsonl_to_md.py` 转换 | 单分片约 0.1 秒 → 174 KB / 2,095 行 Markdown | 同上 |

---

## 文件结构

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 核心指令集（DRAS-V 协议 + 三层架构 + 命令参数速查），Agent 直接加载执行 |
| `README.md` | 本文档，项目概览与快速入门 |
| `scripts/archive_export.py` | 对话归档导出引擎（OpenClaw / Marvis / WorkBuddy 三模 + 增量合并） |
| `scripts/archive_index.py` | 归档索引管理（基础版：stats / pending） |
| `scripts/jsonl_to_md.py` | JSONL → Markdown 转换（基础版：minimal 模式） |
| `scripts/snapshot_sync_check.py` | 双文档联动核账校验（PROJECT_SNAPSHOT.md / PROJECT.md 六维比对，基础版免费开放） |
| `LICENSE.md` | MIT 开源协议 |
| `CHANGELOG.md` | 版本更新记录 |

---

## 常见问题

- **会上传云端吗？** 不会，所有文件只写本地 `archive/` 目录；归档/进化/快照均需你主动说触发词，无后台静默保存。
- **会越来越慢吗？** 归档是只增不改，读取性能取决于分片数量；68 文件规模下索引统计 0.07 秒。
- **能按日期或轮次检索归档吗？** `mark` / `search` / `summary` 与 `--style full`、`--css` 需按版本核对（对照表见https://www.jinengpu.chat/mindvault-detail.html）；本包开放 `stats`、`pending` 与 `minimal` 渲染。
- **换平台后历史还能用吗？** 能，带上 `archive/` 目录即可继续增量归档。
- **快照双文档（PROJECT_SNAPSHOT.md / PROJECT.md）会不会写着写着不同步？** 已内置防断裂规范：更新日志逐条比对、章节正文双向回改互检、头部元数据强制刷新，并要求联动完成后运行 `scripts/snapshot_sync_check.py` 做六维核账（退出码非 0 即存在断裂）。

---

## 数据与隐私

- 备份文件写入本地 `archive/` 目录（每对话独立子目录 + `_index.json` 索引），不上传云端。
- 归档会保存你的原始消息，**建议避免在对话中输入密码、密钥等敏感信息**；已归档内容可自行编辑或删除。
- 归档数据由用户自行管理生命周期，可随时导出、迁移、删除；本 Skill 不设自动清理，也不内置定时器。

---

## 相关链接

- GitHub 仓库：https://github.com/zhouxin121/mindvault
- ClawHub 上架页：https://clawhub.ai/zhouxin121/mindvault-agent-memory
- SkillHub 技能市场：https://skillhub.cn （搜索「mindvault」）
- 同类方案横向对照（长期记忆 / 分层记忆 / 遗忘曲线 / 多 Agent 编排）见 [SKILL.md](SKILL.md) 参考链接章节

---

> 本包免费：`archive_index` 开放 `stats` / `pending`，`jsonl_to_md` 开放 `minimal` 渲染。更多命令的对照表见https://www.jinengpu.chat/mindvault-detail.html。

---

*MindVault v1.2.6 · 免费 · 5000+ 轮实战验证 · 跨平台 Agent 对话归档与记忆基础设施*
