---
name: github-issue-auto-triage
description: 自动分类 GitHub Issue，AI 打标签、分配负责人、检测重复、回复 FAQ
version: 1.0.0
tags: [github, automation, issue, triage, ai, developer]
user-invocable: true
---

# GitHub Issue Auto Triage Skill

自动分类 GitHub Issue，AI 智能打标签、分配负责人、检测重复 Issue、自动回复 FAQ。

## 触发条件

- **定时触发**: 每 30 分钟检查新 Issue
- **手动触发**: `/triage-issues` 或 "处理 GitHub Issue"
- **Webhook 触发**: GitHub webhook 推送

## 核心功能

### 1. AI 智能分类
- 读取 Issue 标题和描述
- 使用 LLM 分析内容
- 自动分配合适的标签（bug/enhancement/question 等）
- 识别严重程度（critical/major/minor）

### 2. 自动分配负责人
- 根据 Issue 类型分配
- 考虑团队成员负载
- 支持轮询分配
- 可配置分配规则

### 3. 重复 Issue 检测
- 语义相似度分析
- 检测相似标题
- 自动关联重复 Issue
- 建议关闭重复

### 4. FAQ 自动回复
- 识别常见问题
- 自动回复标准答案
- 提供文档链接
- 标记为已解决

### 5. 智能通知
- Slack/Discord 通知
- @mention 相关负责人
- 优先级告警
- 日报/周报生成

## 配置参数

```yaml
github:
  owner: "your-org"
  repo: "your-repo"
  token: "${GITHUB_TOKEN}"
  
triage:
  enabled: true
  interval_minutes: 30
  auto_label: true
  auto_assign: true
  detect_duplicates: true
  auto_reply_faq: true
  
labels:
  bug:
    keywords: ["bug", "error", "crash", "fail", "broken"]
    priority: high
  enhancement:
    keywords: ["feature", "enhancement", "improve", "add"]
    priority: medium
  question:
    keywords: ["question", "help", "how to", "confused"]
    priority: low
  
assignees:
  bug: ["@dev1", "@dev2"]
  enhancement: ["@pm1"]
  question: ["@support1"]
  
faq:
  - question: "how to install"
    answer: "See installation guide: https://docs.example.com/install"
  - question: "license"
    answer: "We use MIT license. See LICENSE file."
```

## 使用示例

### 手动触发
```bash
# 处理所有未分类 Issue
/triage-issues

# 处理特定 Issue
/triage-issues #123

# 检查重复
/triage-issues --check-duplicates
```

### 定时任务
```yaml
# crontab
*/30 * * * * github-issue-triage --run
```

### API 调用
```bash
curl -X POST http://localhost:8080/api/triage \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"repo": "owner/repo", "issue_number": 123}'
```

## 输出示例

### Issue #123 处理结果
```
✅ Issue #123: "App crashes on startup"

分类结果:
  - 类型：bug
  - 严重程度：critical
  - 标签：["bug", "critical", "startup"]
  - 负责人：@dev1
  - 状态：已分配

操作记录:
  ✅ 添加标签：bug
  ✅ 添加标签：critical
  ✅ 分配给：@dev1
  ✅ 发送 Slack 通知
  ✅ 记录到日志

耗时：2.3 秒
```

## 依赖

- GitHub API
- LLM (Qwen/DashScope)
- Slack API (可选)

## 安全

- GitHub Token 安全存储
- 最小权限原则
- 操作日志记录
- 支持 dry-run 模式

## 扩展

- 支持 GitLab
- 支持 Jira
- 自定义分类规则
- 多仓库管理
