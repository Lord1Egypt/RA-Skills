# OpenClaw 自救系统 Skill v2.3.0

> 适配 OpenClaw 2026.4.x | 更新于 2026-04-10
> 
> ## 更新日志
> - v2.3.0: 跨平台自动适配（macOS/Linux/Windows）、端口动态读取、密钥脱敏、卸载脚本
> - v2.2.0: 真正的健康检查（检查服务响应，不仅仅是进程存在）
> - v2.1.0: 适配 OpenClaw 2026.4.x，auth 文件路径更新
>
> ## 跨平台支持
>
> 安装时自动检测操作系统，生成适配版本：
> - **macOS** → cron 定时任务 + osascript 通知
> - **Linux** → cron 定时任务 + notify-send 通知
> - **Windows** → 提供 Task Scheduler 命令 + PowerShell 通知

自动备份配置、监控运行状态、崩溃时自动回滚恢复。

## 功能特性

- **智能备份**: 文件变化自动备份 + 每日自动备份
- **健康监控**: 每5分钟检查运行状态、磁盘空间、内存使用
- **自动回滚**: 崩溃时自动恢复到最近的有效备份
- **系统通知**: macOS 弹窗通知恢复状态
- **一键回滚**: 手动选择备份时间点恢复
- **保底配置**: 所有备份失败时使用安全模式启动
- **配置验证**: 备份前自动验证 JSON 格式

## 安装

```bash
# 运行安装脚本
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/install-v2.sh
```

## 手动操作

```bash
# 立即备份
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/smart-backup.sh

# 手动检查并恢复
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/recover-v2.sh

# 一键回滚（选择备份）
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/rollback.sh

# 查看日志
cat ~/.openclaw/logs/recovery.log
cat ~/.openclaw/logs/backup.log

# 卸载
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/uninstall.sh
```

## 文件说明

- `smart-backup.sh` - 智能备份（监控变化 + 定时备份）
- `recover-v2.sh` - 恢复脚本（含健康检查、系统通知）
- `rollback.sh` - 一键回滚工具
- `install-v2.sh` - 安装脚本
- `safe-mode.json` - 保底配置文件

## 备份策略

- **实时监控**: 配置文件变化立即自动备份
- **每日备份**: 每天凌晨2点自动备份
- **保留策略**: 
  - 最近20个备份
  - 7天历史备份（每天保留最新）
- **备份文件**: `openclaw.json.bak.YYYYMMDD_HHMMSS`
- **备份位置**: `~/.openclaw/backups/`

## 恢复流程

1. 检测 OpenClaw 运行状态
2. 检查磁盘空间、内存使用
3. 如停止，验证配置文件有效性
4. 无效则尝试回滚（最多10个备份）
5. 所有备份失败则使用保底配置
6. 发送系统通知告知恢复结果

## 注意事项

- 回滚只影响系统配置（API、端口等）
- 不影响人格设定（SOUL.md）和记忆
- macOS/Linux 需要 cron（系统自带）
- Windows 需要手动设置 Task Scheduler（安装脚本会提示命令）
- fswatch 为可选，用于实时监控配置变化
