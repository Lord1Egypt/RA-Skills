---
name: gitea-routine-report
version: 1.2.0
description: 获取 Gitea 各仓库提交记录，调用 AI 生成进度报告，并发送 HTML 邮件给仓库管理员
author: mayidan, zhangyiwen
license: MIT
required_environment_variables:
  - GITEA_URL
  - GITEA_TOKEN
primary_credential: GITEA_TOKEN
credentials:
  - name: GITEA_TOKEN
    type: personal_access_token
    provider: gitea
environment_file: ~/.config/gitea-routine-report/.env
---

# Gitea Routine Report

## 功能描述
对每个 Gitea 可见仓库分别生成一份 HTML 格式进度报告，内容包括：
- 情况总览（统计周期、提交次数、参与成员）
- AI 综合评估（现状评估 + 下一步建议）
- 成员贡献排行
- 每位成员的工作摘要、文件类型分布、详细提交记录
- 本期无提交成员名单（含连续未提交天数和最后提交日期）
- 风险提示

每个仓库单独发送一封 HTML 邮件给该仓库的管理员。

## 使用场景
- 当用户说"帮我生成进度报告"且未给出仓库与时间时触发（默认：全部可见仓库 + 最近 7 天）
- 当用户说"帮我生成某个仓库的进度报告"并给出 `owner/repo` 时触发单仓库模式（默认：最近 7 天）
- 当用户明确给出 `since` + `until`（或等价的起止日期）时触发绝对时间段模式（仓库可指定或不指定）
- 当用户说"最近 N 小时 / 最近一天 / 最近三天"时触发相对时间语义解析，并先换算为绝对时间段后执行
- 当用户需要按固定节奏推送团队进展（日报/周报）或临时排查某时间段风险时触发

## 使用方法

```bash
# 默认：全部可见仓库 + 最近7天
python scripts/generate_report.py

# 指定仓库 + 绝对时间段（UTC+8，北京时间）
python scripts/generate_report.py --repo mayidan/project-test --since 2026-04-01 --until 2026-04-07

# 只指定仓库、不指定时间时，默认最近7天
python scripts/generate_report.py --repo mayidan/project-test

# 全部可见仓库 + 绝对时间段（UTC+8，北京时间）
python scripts/generate_report.py --since 2026-04-01T00:00:00 --until 2026-04-07T23:59:59

# 用户说"最近 N 小时"时，内部先换算为绝对时间段后执行
# 例如：最近8小时 => until=当前时刻，since=当前时刻-8小时
```

## 执行流程

**重要：必须严格按照以下四个步骤顺序执行，不得跳过任何步骤。**

---

### 第一步：运行脚本获取数据（必须执行）

无论何时触发此 skill，必须首先根据用户输入选择以下命令之一获取最新数据，不得使用记忆中的历史数据：

- 用户给出绝对时间段（`since` + `until`）且明确指定仓库时：
```bash
python scripts/generate_report.py --repo owner/repo --since 2026-04-01 --until 2026-04-07
```

- 用户给出绝对时间段（`since` + `until`）但未指定仓库时：
```bash
python scripts/generate_report.py --since 2026-04-01T00:00:00 --until 2026-04-07T23:59:59
```

- 用户只指定仓库（未给出绝对时间段）时：
```bash
python scripts/generate_report.py --repo owner/repo
```

- 用户既未指定仓库，也未给出绝对时间段时（默认最近 7 天）：
```bash
python scripts/generate_report.py
```

时间参数规则：
- 统一使用绝对时间段：脚本参数为 `--since` 和 `--until`。
- 当用户说"最近 N 小时"时，按当前时刻换算：`until = now`，`since = now - N 小时`，再调用脚本。
- 未提供时间参数时，默认统计最近 7 天（即 `since = now - 168h`，`until = now`）。
- 日期格式支持：`YYYY-MM-DD` 或 `YYYY-MM-DDTHH:MM:SS`（按 UTC+8/北京时间解释）。

---

### 第二步：从脚本输出中读取数据

脚本输出是一个 JSON 数组，每个元素包含：
- `repo`：仓库名称
- `admin_email`：仓库创建者邮箱
- `has_commits`：本期是否有提交记录
- `time_range`：统计周期简述
- `time_range_detail`：统计周期详细时间范围
- `generated_at`：生成时间
- `overview`：总览数据（total_commits, total_members, total_deletions）
- `members`：各成员数据（含 commit_details, file_type_summary, branches）
- `inactive_members`：本期无提交成员列表（含 name, last_commit_date, inactive_days）
- `vague_commits`：模糊提交列表

---

### 第三步：对每个仓库，用 AI 生成纯文字内容（must output JSON only）

**此步骤 AI 只负责生成文字内容，不得输出任何 HTML。**

对 JSON 数组中 `has_commits` 为 true 的每一个仓库，根据该仓库的数据，生成如下结构的 JSON：

```json
{
  "ai_overview": "根据提交内容和成员活跃度，用2-3句话评估本期项目整体进展和主要推进了哪些工作",
  "ai_suggestion": "根据现状和风险，给项目负责人1-2条具体可执行的建议，帮助推进后续工作",
  "member_summaries": {
    "成员名1": "根据该成员所有 commit message 提炼的一句话工作总结",
    "成员名2": "根据该成员所有 commit message 提炼的一句话工作总结"
  },
  "risk_notes": "风险提示内容，多条风险用换行分隔，每条以⚠️或ℹ️开头；若无风险则填空字符串"
}
```

**输出要求（严格遵守）：**
- 只输出上述 JSON，不得在 JSON 前后添加任何说明文字、代码块标记（```）或 HTML
- `member_summaries` 中的键名必须与数据中的成员用户名完全一致
- `risk_notes` 示例（多条换行）：
  ```
  ⚠️ ZhangYiwen 已连续 6 天未提交，上次提交日期：2026-04-04
  ⚠️ 发现 1 条模糊提交，建议规范提交信息
  ```
- `risk_notes` 若本期无风险，填入空字符串 `""`

---

### 第四步：调用脚本将数据 + AI 文字内容拼装为 HTML，并发邮件

**❌ 禁止由 AI 直接拼写 HTML 正文，HTML 必须全部由脚本生成。**

对每个仓库分别执行：

**情况一：`has_commits` 为 false（本期无提交）**

运行以下命令生成 HTML：

```bash
python -c "
import json, sys, os
sys.path.insert(0, 'scripts')
from render_email import render
data = json.loads(open('/tmp/report_data.json').read())
# 找到对应仓库
repo_data = next(d for d in data if d['repo'] == 'REPO_NAME')
html = render(repo_data)
open('/tmp/email_body.html', 'w').write(html)
print('HTML 已生成，长度：', len(html))
"
```

然后调用 imap-smtp-email skill 发送邮件：
- 收件人：`admin_email`（除非用户指定了其他收件人）
- 邮件主题：`【项目进度报告】{repo} · {time_range}`（time_range 取数据中的 time_range 字段，如"过去 7 天"）
- 邮件格式：HTML
- 邮件正文：读取 `/tmp/email_body.html` 的内容

**情况二：`has_commits` 为 true（本期有提交）**

首先将第三步输出的 AI JSON 保存到 `/tmp/ai_content_{repo_safe}.json`（repo_safe 为仓库名中 `/` 替换为 `_`），然后运行：

```bash
python -c "
import json, sys, os
sys.path.insert(0, 'scripts')
from render_email import render
data = json.loads(open('/tmp/report_data.json').read())
ai_content = json.loads(open('/tmp/ai_content_REPO_SAFE.json').read())
repo_data = next(d for d in data if d['repo'] == 'REPO_NAME')
html = render(repo_data, ai_content)
open('/tmp/email_body.html', 'w').write(html)
print('HTML 已生成，长度：', len(html))
"
```

然后调用 imap-smtp-email skill 发送邮件：
- 收件人：默认使用 `admin_email`，用户指定了收件人则以用户指定为准
- 邮件主题：`【项目进度报告】{repo} · {time_range}`（time_range 取数据中的 time_range 字段）
- 邮件格式：HTML
- 邮件正文：读取 `/tmp/email_body.html` 的内容

---

## 依赖 skill
- imap-smtp-email：发送邮件，请确保该 skill 已安装并配置好 SMTP 信息
