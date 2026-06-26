---
name: macos-launchctl
description: 在 macOS 环境下使用 launchctl 定时启动或停止应用。当用户要求「定时启动/停止某个应用」「设置定时任务」「用 launchctl 管理应用」「每天几点自动打开XX」「定时关闭XX」时应使用本 Skill。支持自然语言时间描述（如「每天9点」「每2小时」「每周一上午8点」）和标准 cron 表达式，自动生成并加载 launchd plist 配置文件，支持查看、启动、停止、删除定时任务。
---

# macOS Launchctl 定时应用管理器

## 概述

本 Skill 提供在 macOS 环境下通过 `launchctl` / `launchd` 机制，定时自动启动或停止应用的能力。用户用自然语言描述时间和应用，Skill 自动解析时间、生成 plist 配置文件并加载到系统。

## 核心脚本

主脚本位于 `scripts/macos_launchctl.sh`，提供以下子命令：

| 命令 | 说明 |
|------|------|
| `create <app> <schedule>` | 创建定时启停任务 |
| `list` | 列出当前用户的 LaunchAgents 任务 |
| `start <label>` | 手动触发启动任务 |
| `stop <label>` | 停止正在运行的任务 |
| `restart <label>` | 重启任务 |
| `remove <label>` | 删除任务（含备份） |
| `info <label>` | 查看任务详情和日志 |
| `status <label>` | 查看任务运行状态 |

## ⚠️ 安全规则（强制执行）

> **在执行任何写入操作前，必须完成以下确认流程，不得跳过。**

1. **预览计划**：向用户清晰展示将要执行的所有操作，包括：
   - 目标应用名称和路径
   - 定时任务的触发时间（人类可读格式）
   - 将要写入的 plist 文件路径
   - 将要执行的 launchctl 命令
2. **等待确认**：以明确的问题询问用户是否继续，如：`"以上计划是否确认执行？输入「确认」继续，或告诉我需要修改的地方。"`
3. **仅在用户明确确认后**执行 `launchctl load` / `launchctl unload` / 写入 plist 文件等操作
4. **删除操作**（`remove`）必须额外展示将被删除的文件完整路径，并再次确认
5. 使用 `--dry-run` 参数可仅预览将要生成的 plist 内容，不实际写入

## 工作流程

### 第 0 步：安全确认（强制）

在任何实际操作之前，先向用户展示计划并等待确认。示例输出格式：

```
📋 定时任务计划
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  应用：Safari（/Applications/Safari.app）
  启动：每工作日 09:00
  停止：每工作日 18:00
  写入路径：
    ~/Library/LaunchAgents/com.user.launch.safari.start.plist
    ~/Library/LaunchAgents/com.user.launch.safari.stop.plist
  执行命令：
    launchctl load ~/Library/LaunchAgents/com.user.launch.safari.start.plist
    launchctl load ~/Library/LaunchAgents/com.user.launch.safari.stop.plist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
是否确认执行？
```

### 第一步：理解用户意图

用户可能的表达方式：
- "帮我设置每天9点自动打开 Safari"
- "定时在晚上10点关闭微信"
- "每周一到周五早上8点启动企业微信，晚上6点关闭"
- "用 launchctl 管理我的 Slack，每2小时启动一次"
- "查看当前所有的定时任务"
- "删除 Safari 的定时任务"

### 第二步：解析应用路径

调用 `scripts/macos_launchctl.sh` 的解析逻辑（或 AI 自行解析），支持的输入格式：
1. **应用名**：`Safari`、`WeChat`、`企业微信`
2. **`.app` 路径**：`/Applications/Safari.app`
3. **Bundle ID**：`com.apple.Safari`

解析优先级：
1. 绝对路径 → 直接验证存在性
2. `/Applications/<name>.app` 和 `~/Applications/<name>.app`
3. `mdfind` 搜索（支持中文应用名）

### 第三步：解析时间调度

支持以下时间格式（均由脚本自动转换为 cron）：

| 用户描述 | 解析结果 |
|---------|---------|
| `每天 9:00` / `daily at 09:00` | `0 9 * * *` |
| `每天 18:30` | `30 18 * * *` |
| `每小时` | `0 */1 * * *` |
| `每2小时` | `0 */2 * * *` |
| `每周一 9:00` | `0 9 * * 1` |
| `周一至周五 8:30` | `30 8 * * 1-5` |
| `周末 10:00` | `0 10 * * 0,6` |
| `* * * * *`（标准 cron）| 原样使用 |

**重要**：launchd 的 `StartCalendarInterval` 不支持 cron 的 `*`（通配），需将 `*` 替换为具体值，或使用多段 dict 配置。对于复杂 cron（含 `*/n`、`,`、`-`），脚本会自动展开为多个 `StartCalendarInterval` 条目。

### 第四步：生成 plist 文件

plist 文件存放在 `~/Library/LaunchAgents/`，命名规范：
- 启动任务：`com.user.launch.<app_name_lower>.start.plist`
- 停止任务：`com.user.launch.<app_name_lower>.stop.plist`

**启动 plist 模板**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.launch.safari.start</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>-a</string>
        <string>/Applications/Safari.app</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/com.user.launch.safari.start.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/com.user.launch.safari.start-error.log</string>
</dict>
</plist>
```

**停止 plist 模板**（使用 `osascript` 发送 quit 指令）：
```xml
<key>ProgramArguments</key>
<array>
    <string>/usr/bin/osascript</string>
    <string>-e</string>
    <string>tell application "Safari" to quit</string>
</array>
```

### 第五步：加载/卸载任务

```bash
# 加载任务
launchctl load ~/Library/LaunchAgents/com.user.launch.safari.start.plist

# 卸载任务
launchctl unload ~/Library/LaunchAgents/com.user.launch.safari.start.plist

# 查看任务状态
launchctl list | grep "com.user.launch"
```

## 快速命令参考

```bash
# 预览将要创建的任务（不会实际写入或加载！推荐先执行此步骤）
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh create Safari "每天 9:00" --stop-at "每天 18:00" --dry-run

# 创建（每天9点启动，18点停止，会弹出交互确认）
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh create Safari "每天 9:00" --stop-at "每天 18:00"

# 创建（跳过确认直接执行——仅限自动化场景）
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh create Slack "每2小时" --start-only --yes

# 创建（仅启动，不自动停止）
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh create Slack "每2小时" --start-only

# 列出所有任务
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh list

# 预览删除计划（不会实际删除！）
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh remove com.user.launch.safari --dry-run

# 查看状态
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh status com.user.launch.safari.start

# 手动触发
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh start com.user.launch.safari.start

# 删除任务（需交互确认）
bash ~/.workbuddy/skills/macos-launchctl/scripts/macos_launchctl.sh remove com.user.launch.safari
```

## 注意事项

1. **安全确认**（强制）：`create` 和 `remove` 命令默认会弹出交互式确认。使用 `--dry-run` 可先预览计划，`--yes` 跳过确认
2. **权限**：launchctl 用户级任务无需 sudo，存放在 `~/Library/LaunchAgents/`
3. **Weekday**：launchd 的 Weekday 从 0（周日）到 6（周六），与 cron 一致
4. **多时间段**：如果 cron 含 `,`（如 `1,3,5`），需生成多个 `StartCalendarInterval` dict
5. **应用名含空格**：plist 中需用 `<string>` 正确包裹，解析时注意转义
6. **删除前备份**：删除任务时脚本会自动备份 `.plist.bak.<timestamp>`
7. **日志路径**：任务执行日志在 `/tmp/<label>.log` 和 `/tmp/<label>-error.log`
8. **AI 使用规范**：调用本 Skill 时，必须先用 `--dry-run` 预览操作计划，向用户展示完整内容并获得明确确认后，再去掉 `--dry-run` 执行实际操作

## 常见问题排查

| 问题 | 排查方法 |
|------|---------|
| 任务未触发 | 检查 `launchctl list \| grep <label>`，确认已加载；检查 `/tmp/<label>-error.log` |
| 应用无法启动 | 确认 plist 中应用路径正确；尝试 `open -a <App名>` 手动测试 |
| 停止任务无效 | 部分应用不支持 AppleScript quit，需 `killall <app>` 替代 |
| 修改后不生效 | 先 `launchctl unload` 再 `launchctl load` 重新加载 |
