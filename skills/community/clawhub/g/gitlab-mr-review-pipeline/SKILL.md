---
name: gitlab-mr-review-pipeline
description: 自动化 GitLab MR 代码审核流水线。使用 AI 对 MR 进行代码审查，生成报告并邮件发送给提交人。
version: 1.0.0
author: milet_suki
dependencies:
  - code-review
  - md-to-pdf-advanced
  - email-mail-master
---

# GitLab MR Review Pipeline

自动化 GitLab Merge Request 代码审核流水线。使用 AI 对 MR 进行代码审查，生成报告并邮件发送给提交人。

---

## 依赖技能

执行前确保已安装：
- **glab-cli** - GitLab CLI（可选，脚本会使用 API 直接调用）
- **code-review** - AI 代码审核
- **md-to-pdf-advanced** - Markdown 转 PDF
- **email-mail-master** - 邮件发送

### 安装命令

```bash
npx clawhub install glab-cli
npx clawhub install code-review
npx clawhub install md-to-pdf-advanced
npx clawhub install email-mail-master
```

---

## 配置文件

**路径**: `~/.config/gitlab-mr-review-pipeline/config.json`

```json
{
  "gitlab": {
    "host": "http://your-gitlab.com",
    "access_token": "your-access-token"
  },
  "email": {
    "provider": "163",
    "address": "your-email@163.com",
    "auth_code": "your-auth-code"
  },
  "repositories": ["owner/repo1", "owner/repo2"]
}
```

### 配置说明

| 字段 | 说明 | 必需 |
|------|------|------|
| `gitlab.host` | GitLab 地址 | 是 |
| `gitlab.access_token` | Access Token（需 api 权限） | 是 |
| `email.provider` | 邮箱服务商（163/qq/126） | 是 |
| `email.address` | 邮箱地址 | 是 |
| `email.auth_code` | 邮箱授权码（非登录密码） | 是 |
| `repositories` | 监控的仓库列表 | 是 |

---

## 使用方式

### 方式 1：直接告诉 OpenClaw

```
帮我审核 GitLab 仓库的 MR
```

OpenClaw 会按照以下流程执行：

### 方式 2：使用脚本初始化配置

```bash
python3 skills/gitlab-mr-review-pipeline/scripts/init-config.py
```

---

## 执行流程

### 步骤 1：检查配置

读取 `~/.config/gitlab-mr-review-pipeline/config.json`

如果配置不存在，提示用户运行初始化脚本。

### 步骤 2：查询待处理 MR

使用 GitLab API 查询每个仓库的待处理 MR：

```bash
# 使用工具脚本
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-list --repo owner/repo
```

**API 端点**: `{host}/api/v4/projects/{repo}/merge_requests?state=opened`

如果没有待处理 MR，提示用户并终止。

### 步骤 2.5：检查 MR 是否已处理（避免重复）

对于每个待处理 MR，检查是否已处理过：

```bash
python3 skills/gitlab-mr-review-pipeline/scripts/mr-records.py check --repo owner/repo --mr-id 2
```

如果输出包含 "已处理过"，跳过该 MR。

### 步骤 3：获取 MR 详情

对于每个待处理 MR：

1. **获取 diff**
   ```bash
   python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-diff --repo owner/repo --mr-id 2
   ```
   **API**: `{host}/api/v4/projects/{repo}/merge_requests/{id}/changes`

2. **获取提交人邮箱**
   ```bash
   python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-commits --repo owner/repo --mr-id 2
   ```
   **API**: `{host}/api/v4/projects/{repo}/merge_requests/{id}/commits`

### 步骤 4：AI 代码审核

使用 **code-review** 技能对 diff 内容进行审查。

**审核提示模板**:

```
使用 code-review 技能对以下代码变更进行详细审查。

## MR 信息
- 仓库：{repo}
- MR ID: !{id}
- 标题：{title}
- 作者：{author}

## 代码变更
```diff
{diff_content}
```

## 审核要求
请按照 code-review 技能的 checklist 进行审查，**只列出发现的问题项**。

输出格式参考：references/review-report-template.md
```

**输出**: `file/mr-code-review-report.md`

### 步骤 5：生成 PDF

使用 **md-to-pdf-advanced** 技能：

```bash
python3 skills/md-to-pdf-advanced/scripts/md_to_pdf.py \
  file/mr-code-review-report.md \
  mr-reports/{repo}_MR{id}_{author}_review.pdf
```

### 步骤 6：发送邮件

使用 **email-mail-master** 技能发送审核报告。

**邮件主题**: `[MR Review - AI 代码审核] !{id} {title}`

**邮件正文模板**:
```
尊敬的开发者，您好！

您的 Merge Request 已完成 AI 代码审核。

📋 审核概览
- MR: !{id} {title}
- 仓库：{repo}
- 综合评分：{score}/100
- 发现问题：{critical} 个严重，{major} 个主要

📎 请查收附件中的详细审核报告（PDF 格式）。

💡 建议
请优先修复标记为 [CRITICAL] 和 [MAJOR] 的问题。
修复完成后，可以重新提交审核。

祝编码愉快！

---
GitLab MR Review Pipeline
AI 代码审核系统
```

### 步骤 7：标记 MR 已处理

```bash
python3 skills/gitlab-mr-review-pipeline/scripts/mr-records.py mark \
  --repo owner/repo \
  --mr-id 2 \
  --author author@example.com \
  --score 61 \
  --issues 5
```

记录已处理的 MR，避免下次重复审核。

### 步骤 8：清理临时文件（可选）

```bash
python3 skills/gitlab-mr-review-pipeline/scripts/cleanup.py --days 7
```

清理临时 markdown 文件和 7 天前的 PDF 报告。

---

## 工具脚本

### gitlab-api.py

GitLab API 调用工具。

```bash
# 查询 MR 列表
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-list --repo owner/repo

# 获取 MR diff
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-diff --repo owner/repo --mr-id 2

# 获取 MR commits
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py mr-commits --repo owner/repo --mr-id 2

# 验证仓库
python3 skills/gitlab-mr-review-pipeline/scripts/gitlab-api.py repo-check --repo owner/repo
```

### mr-records.py

MR 处理记录管理（避免重复审核）。

```bash
# 检查 MR 是否已处理
python3 skills/gitlab-mr-review-pipeline/scripts/mr-records.py check --repo owner/repo --mr-id 2

# 标记 MR 已处理
python3 skills/gitlab-mr-review-pipeline/scripts/mr-records.py mark \
  --repo owner/repo --mr-id 2 --author user@example.com --score 61 --issues 5

# 列出最近处理的 MR
python3 skills/gitlab-mr-review-pipeline/scripts/mr-records.py list --days 7

# 清理旧记录
python3 skills/gitlab-mr-review-pipeline/scripts/mr-records.py cleanup --days 30
```

**记录文件位置**: `~/.config/gitlab-mr-review-pipeline/processed-mrs.json`

### cleanup.py

清理临时文件和旧报告。

```bash
# 清理临时文件和 7 天前的 PDF
python3 skills/gitlab-mr-review-pipeline/scripts/cleanup.py --days 7

# 显示存储统计
python3 skills/gitlab-mr-review-pipeline/scripts/cleanup.py --stats

# 清理所有临时文件
python3 skills/gitlab-mr-review-pipeline/scripts/cleanup.py --all
```

### init-config.py

配置初始化脚本。

```bash
python3 skills/gitlab-mr-review-pipeline/scripts/init-config.py
```

会引导用户输入：
- GitLab 地址和 Token
- 邮箱配置
- 监控仓库列表

并验证配置是否有效。

---

## 输出文件

### Markdown 报告
- **路径**: `file/mr-code-review-report.md`
- **格式**: 参考 `review-report-template.md`

### PDF 报告
- **路径**: `mr-reports/{repo}_MR{id}_{author}_review.pdf`

### 邮件
- **收件人**: MR 提交人邮箱
- **主题**: `[MR Review - AI 审核] !{id} {title}`
- **附件**: PDF 审核报告

---

## 报告格式示例

```markdown
# Code Review Report

## 基本信息
| 项目 | 内容 |
|------|------|
| 仓库 | owner/repo |
| MR ID | !2 |
| 标题 | Feature xxx |

## ❌ 发现问题

### [CRITICAL] 问题标题
- **文件**: `path/to/file.java`
- **代码**:
```java
// 问题代码
```
- **风险**: 描述风险
- **建议**: 修改建议

## 📊 评分
| 维度 | 得分 |
|------|------|
| 安全性 | 60/100 |
| 代码质量 | 75/100 |

**综合评分**: 61/100

## 🎯 结论
**建议**: 需要修复后重新审查
```

---

## 故障排除

### GitLab API 调用失败

**错误**: `401 Unauthorized`

**原因**: Token 无效或过期

**解决**: 重新生成 Access Token

### 仓库不存在

**错误**: `404 Not Found`

**原因**: 仓库名称错误或无访问权限

**解决**: 检查仓库名称格式（`owner/repo`）

### 邮件发送失败

**错误**: `Authentication failed`

**原因**: 使用了登录密码而非授权码

**解决**: 在邮箱设置中获取授权码（SMTP 授权码）

### PDF 中文乱码

**解决**: 安装中文字体

```bash
sudo apt-get install fonts-noto-color-emoji fonts-wqy-zenhei
fc-cache -fv
```

---

## 安全注意事项

1. **配置文件权限**: 设置为 600
   ```bash
   chmod 600 ~/.config/gitlab-mr-review-pipeline/config.json
   ```

2. **Token 安全**: 不要将 Token 提交到版本控制

3. **定期轮换**: 建议每 3 个月更换一次 Token

---

## 示例会话

```
用户：帮我审核 GitLab 仓库的 MR

AI: 好的，让我先检查配置...

[检查配置]
✓ 配置文件已找到

[查询 MR]
✓ owner/repo: 发现 1 个待处理 MR (!2)

[获取 MR 详情]
✓ 获取 diff 成功（223KB）
✓ 提交人邮箱：author@example.com

[AI 代码审核]
✓ 使用 code-review 技能
✓ 发现 2 个 CRITICAL 问题
✓ 发现 3 个 MAJOR 问题
✓ 综合评分：61/100

[生成 PDF]
✓ PDF 已生成

[发送邮件]
✓ 邮件已发送至 author@example.com

✅ 处理完成！
```

---

## 版本

- **版本**: 2.0
- **最后更新**: 2026-03-29
- **变更**: 简化脚本逻辑，主要流程由 AI 执行

---

## 社区

- **技能市场**: https://clawhub.com
- **问题反馈**: 提交 Issue
