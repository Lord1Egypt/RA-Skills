# OpenClaw 更新检查技能

## 概述

每日检查 OpenClaw 是否有新版本，获取 Release Note，分析是否需要更新，并推送建议给用户（不主动更新）。

## 功能

### 1. 检查更新状态

使用 `openclaw update status` 或 `openclaw version` 获取当前版本和最新版本信息。

### 2. 获取 Release Note

从 GitHub releases 页面获取最新的 Release Note：
- URL: https://github.com/openclaw/openclaw/releases
- 使用 `web_fetch` 工具获取内容

### 3. 分析是否需要更新

根据 Release Note 分析：
- **重要功能更新**：新功能对用户有帮助
- **安全更新**：涉及安全性
- **Breaking Changes**：可能导致配置不兼容
- **Bug 修复**：修复重要问题

### 4. 推送建议

通过飞书向用户推送更新建议，包含：
- 当前版本 vs 最新版本
- Release Note 摘要
- 是否建议更新
- 原因说明

## 工具

- `exec`: 执行 openclaw 命令
- `web_fetch`: 获取 GitHub releases 页面
- `feishu_doc` 或 `message`: 推送消息给用户

## 使用方式

### 手动触发

用户发送"检查更新"或类似指令时执行。

### 定时任务（每日）

配置 cron job 每日执行检查。

## 示例输出

```
## OpenClaw 更新检查

### 当前版本
v2026.2.26

### 最新版本
v2026.x.xx

### Release Note 摘要
- 新功能：PDF 分析工具
- 改进：MiniMax M2.5 支持
- Bug 修复：...

### 更新建议
根据 Release Note，建议 [更新/暂不更新]

原因：
1. 有新的重要功能
2. 存在 Breaking Changes，需要检查配置
3. ...
```

## 注意事项

1. 不主动执行更新，只提供建议
2. 分析 Breaking Changes 提醒用户注意
3. 提供更新命令供用户参考（如需更新）
