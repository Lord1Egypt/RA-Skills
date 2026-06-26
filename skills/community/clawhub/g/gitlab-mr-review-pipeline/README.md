---
name: gitlab-mr-review-pipeline
description: 自动化 GitLab MR 代码审核流水线。使用 AI 对 MR 进行代码审查，生成报告并邮件发送给提交人。
version: 1.0.1
---

# GitLab MR Review Pipeline

快速开始指南。

## 快速开始

### 1. 安装依赖技能

```bash
npx clawhub install glab-cli
npx clawhub install code-review
npx clawhub install md-to-pdf-advanced
npx clawhub install email-mail-master
```

### 2. 初始化配置

```bash
python3 skills/gitlab-mr-review-pipeline/scripts/init-config.py
```

### 3. 使用 OpenClaw 执行

直接告诉 OpenClaw：

```
帮我审核 GitLab 仓库的 MR
```

OpenClaw 会按照 SKILL.md 的流程自动执行：
1. 查询待处理 MR
2. 获取代码 diff
3. 使用 code-review 技能进行 AI 审核
4. 生成 Markdown 报告
5. 转换为 PDF
6. 邮件发送给提交人

## 文件结构

```
skills/gitlab-mr-review-pipeline/
├── SKILL.md              # 主要技能说明（AI 执行参考）
├── README.md             # 快速开始指南
├── references/           # 参考文档
│   └── review-report-template.md
└── scripts/              # 工具脚本
    ├── init-config.py    # 配置初始化
    ├── gitlab-api.py     # GitLab API 工具
    ├── mr-records.py     # MR 处理记录
    └── cleanup.py        # 清理工具
```

## 工具脚本

### gitlab-api.py

```bash
# 查询 MR 列表
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-list --repo owner/repo

# 获取 MR diff
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-diff --repo owner/repo --mr-id 2

# 获取提交人邮箱
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-commits --repo owner/repo --mr-id 2
```

## 配置

配置文件：`~/.config/gitlab-mr-review-pipeline/config.json`

```json
{
  "gitlab": {
    "host": "http://your-gitlab.com",
    "access_token": "your-token"
  },
  "email": {
    "provider": "163",
    "address": "your-email@163.com",
    "auth_code": "your-auth-code"
  },
  "repositories": ["owner/repo"]
}
```

## 输出

- **Markdown 报告**: `file/mr-code-review-report.md`
- **PDF 报告**: `mr-reports/{repo}_MR{id}_{author}_review.pdf`
- **邮件**: 发送至 MR 提交人（专业审核通知）

### 邮件示例

**主题**: `[MR Review - AI 代码审核] !2 Feature volcengine 20260302`

**正文**:
```
尊敬的开发者，您好！

您的 Merge Request 已完成 AI 代码审核。

📋 审核概览
- MR: !2 Feature volcengine 20260302
- 仓库：owner/repo
- 综合评分：61/100
- 发现问题：2 个严重，3 个主要

📎 请查收附件中的详细审核报告（PDF 格式）。

💡 建议
请优先修复标记为 [CRITICAL] 和 [MAJOR] 的问题。
修复完成后，可以重新提交审核。

祝编码愉快！

---
GitLab MR Review Pipeline
AI 代码审核系统
```

## 更多信息

参考 `SKILL.md` 了解完整的执行流程和故障排除。
