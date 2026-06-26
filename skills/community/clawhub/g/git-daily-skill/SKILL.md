---
name: gitpulse
description: 今日 Git 提交日报助手 —— 自动扫描当天（含次日凌晨6点前）所有仓库的 commit 记录，生成结构化日报。
---

# ⚡ GitPulse · 生成日报助手

**版本 / Version**: 1.0.0  
**定位**: 每天工作结束后，一键生成当日所有 Git 仓库的提交日报，支持多仓库扫描、跨午夜统计（截止次日 06:00）。

---

## ⚡ 快捷触发 / Quick Triggers

当用户消息匹配以下任意关键词时，**自动激活此技能**：

| 触发词 | 说明 |
| :--- | :--- |
| `今日提交` / `今天提交` | 查今天的 git 记录 |
| `git日报` / `gitpulse` | 直接激活 |
| `提交记录` / `commit记录` | 查提交历史 |
| `今天写了什么` / `今天干了啥` | 口语化触发 |

**示例提示词（用户只需输入）**：
- `今日提交记录`
- `帮我看看今天写了什么代码`
- `gitpulse`
- `生成今天的git日报`

---

## 🤖 AI 执行流程 / Execution Workflow

当技能被触发时，按以下顺序执行：

1. **运行扫描脚本**: 执行 `scripts/gitpulse.py`，脚本自动：
   - 检测用户指定或默认的仓库根目录
   - 扫描所有 `.git` 子目录（支持多仓库）
   - 过滤当日 06:00 ~ 次日 06:00 时间窗口内的 commit
2. **解析脚本输出**: 读取 JSON 格式的结构化结果
3. **生成中文日报**: 综合输出，包含：
   - 📦 各仓库提交数量汇总
   - 📝 每条 commit 的详情（hash、时间、作者、message）
   - 📊 今日编码活跃度统计（总 commit 数、涉及仓库数）
   - 💬 AI 一句话点评（今天是摸鱼之日还是暴肝之夜？）

---

## 🛠️ 工具说明 / Tools Included

### 核心脚本 (`scripts/gitpulse.py`)

- 自动发现多个 Git 仓库（深度优先，最多3层）
- 时间窗口：`今日 06:00:00` ～ `明日 05:59:59`（跨午夜时开发适配）
- 支持通过命令行参数 `--root` 指定扫描根目录
- 支持 `--date` 参数手动指定"哪一天"（格式 `YYYY-MM-DD`）
- 输出格式：JSON + 人类可读两种模式（`--format=json` / `--format=text`）

**用法 / Usage**:

// turbo
```bash
python e:\py\.agent\skills\gitpulse\scripts\gitpulse.py --root e:\py
```

// turbo
```bash
# 指定日期（查昨天）
python e:\py\.agent\skills\gitpulse\scripts\gitpulse.py --root e:\py --date 2026-04-09
```

// turbo
```bash
# 输出 JSON 格式（供 AI 解析）
python e:\py\.agent\skills\gitpulse\scripts\gitpulse.py --root e:\py --format json
```

---

## 📦 依赖 / Dependencies

- Python 3.8+
- 标准库only：`subprocess`, `datetime`, `argparse`, `json`, `os`, `pathlib`（**零额外依赖**）

---

## 📋 输出示例 / Output Example

```
╔══════════════════════════════════════════════╗
║       ⚡ GitPulse · 今日提交日报              ║
║       统计日期: 2026-04-10                    ║
║       时间窗口: 06:00 ~ 次日 05:59           ║
╚══════════════════════════════════════════════╝

📦 仓库: e:\py  (共 3 条提交)
  ├─ [14:23] abc1234  feat: 实现 OTA 价格爬虫并发控制
  ├─ [16:45] def5678  fix: 修复 Django migration 冲突
  └─ [23:10] ghi9012  chore: 更新 start.sh 启动脚本

📊 今日统计:
  · 扫描仓库数: 1
  · 有效提交数: 3
  · 活跃时段: 14:00 ~ 23:10

💬 AI 点评: 晚上11点还在 chore，兄弟今天属于标准暴肝，好好休息！
```
