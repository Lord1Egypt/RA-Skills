---
name: openclaw-version-monitor
description: |
  监控 OpenClaw GitHub 版本更新，获取最新版本发布说明，翻译成中文，
  并推送到 Telegram 和 Feishu。用于：(1) 定时检查版本更新 (2) 
  推送版本更新通知 (3) 生成中文版发布说明
---

# OpenClaw 版本监控

## 功能

1. **检查版本** - 调用 GitHub API 获取最新版本
2. **对比版本** - 与当前版本比较，判断是否有新版本
3. **获取发布说明** - 获取完整的 changelog
4. **翻译中文** - 将英文发布说明翻译成中文
5. **推送到渠道** - 发送消息到 Telegram 和 Feishu

## 使用方法

### 检查版本

```bash
# 获取最新版本号
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | jq -r '.tag_name'
# 返回: v2026.3.13

# 获取最新版本内容
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | jq -r '.body'
```

### 推送格式

```
🆕 OpenClaw 版本更新 | {版本号}

📅 发布于: {日期}

━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 更新内容:

【新增功能】
• ...

【问题修复】
• ...

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 完整更新日志:
https://github.com/openclaw/openclaw/releases/tag/{版本号}
```

### Telegram 推送

- Chat ID: 8290054457
- 限制: 4096 字符/条

### Feishu 推送

- 需要目标用户或群 ID
- 限制相对宽松

## 定时任务配置

### 工作时段 (9:00-19:00)
- 表达式: `0,30 9-18 * * *`
- 行为: 检测到新版本立即推送

### 非工作时段
- 表达式: `0 9 * * *`
- 行为: 每天早上9点检查并推送

## 当前版本

当前监控版本: 2026.3.13
