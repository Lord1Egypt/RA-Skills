# 🚑 OpenClaw Recovery

> **自动监控、检测、修复 OpenClaw 崩溃的自救系统**

[![Version](https://img.shields.io/badge/version-2.3.0-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.4.x-orange)](https://docs.openclaw.ai)

---

## 🎯 解决什么问题？

你有没有遇到过：

- ❌ 改了配置文件，Gateway 启动失败
- ❌ 半夜服务挂了，第二天才发现
- ❌ 不知道怎么恢复到之前的正常配置

**OpenClaw Recovery** 就是你的 24 小时运维小助手 🤖

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 **智能健康检查** | 检查 HTTP 端口 + WebSocket + 进程，不是简单看进程在不在 |
| 🔧 **配置值验证** | 自动检测无效配置值（如 `compaction.mode: "aggressive"`） |
| 🔄 **自动修复** | 配置值错误时自动修复，不需要人工干预 |
| ⏪ **自动回滚** | 修复失败？自动回滚到最近的备份 |
| 📱 **多渠道通知** | macOS 弹窗 + 飞书通知 |
| 📝 **恢复历史** | 记录每次恢复操作，方便事后分析 |
| 🔄 **日志轮转** | 自动清理旧日志，不会撑爆磁盘 |
| 🧹 **一键卸载** | 干净卸载，可选择保留备份 |

---

## 🚀 一键安装

```bash
# 解压到 skill 目录
unzip openclaw-recovery-v2.3.0.zip -d ~/.openclaw/workspace/skills/openclaw-recovery

# 运行安装脚本
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/install-v2.sh
```

安装脚本会：
1. ✅ 创建备份目录和日志目录
2. ✅ 安装保底配置（如已存在则跳过）
3. ✅ 创建首次备份
4. ✅ 配置 cron 定时任务（每 5 分钟健康检查 + 每日凌晨 2 点备份）
5. ✅ 可选：启动文件监控（需 fswatch）

---

## 📋 使用方法

### 自动运行

安装后，系统会自动：
- ⏰ **每 5 分钟**检查一次健康状态
- 🔄 **每天凌晨 2 点**创建配置备份
- 🚨 **检测到异常**自动恢复并通知你

### 手动运行

```bash
# 手动执行健康检查
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/recover-v2.sh

# 手动创建备份
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/smart-backup.sh

# 一键回滚
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/rollback.sh

# 卸载
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/uninstall.sh
```

---

## 📊 恢复流程

```
┌─────────────────┐
│  健康检查开始   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ✅ 健康     ┌─────────────┐
│ HTTP 端口检查   │────────────────▶│   正常退出   │
└────────┬────────┘                 └─────────────┘
         │ ❌ 失败
         ▼
┌─────────────────┐     ✅ 健康     ┌─────────────┐
│ WebSocket 检查  │────────────────▶│   正常退出   │
└────────┬────────┘                 └─────────────┘
         │ ❌ 失败
         ▼
┌─────────────────┐     ✅ 存在     ┌─────────────┐
│   进程检查      │────────────────▶│   正常退出   │
└────────┬────────┘                 └─────────────┘
         │ ❌ 失败
         ▼
┌─────────────────┐
│  验证配置文件   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ✅ 有效     ┌─────────────┐
│ 配置值自动修复  │────────────────▶│   重启服务   │
└────────┬────────┘                 └──────┬──────┘
         │ 修复失败                        │
         ▼                                 ▼
┌─────────────────┐                 ┌─────────────┐
│  回滚到备份     │────────────────▶│  验证恢复   │
└────────┬────────┘                 └──────┬──────┘
         │ 全部失败                        │
         ▼                                 ▼
┌─────────────────┐                 ┌─────────────┐
│  保底配置启动   │────────────────▶│ 发送通知 ✅ │
└─────────────────┘                 └─────────────┘
```

---

## 📁 文件结构

```
~/.openclaw/workspace/skills/openclaw-recovery/
├── _meta.json         # 元数据
├── SKILL.md           # Skill 说明文档
├── README.md          # 本文件
├── LICENSE            # MIT 许可证
├── safe-mode.json     # 保底配置（已脱敏，不含真实密钥）
└── scripts/
    ├── install-v2.sh      # 安装脚本
    ├── uninstall.sh       # 卸载脚本
    ├── recover-v2.sh      # 健康监控与自动恢复
    ├── smart-backup.sh    # 智能备份脚本
    └── rollback.sh        # 一键回滚工具
```

---

## 📝 恢复历史示例

```
[Fri Apr 10 00:49:39 CST 2026] | auto-fix | compaction.mode 无效: 'aggressive' | success
[Fri Apr 10 01:15:22 CST 2026] | rollback | 回滚到 openclaw.json.bak.20260410_020000 | success
[Fri Apr 10 03:22:11 CST 2026] | restart | 正常重启 | success
```

---

## ⚙️ 配置说明

### 健康检查频率

编辑 crontab 修改检查频率：

```bash
crontab -e

# 默认：每 5 分钟检查一次
*/5 * * * * /path/to/recover-v2.sh

# 更频繁：每 1 分钟
* * * * * /path/to/recover-v2.sh
```

### 通知方式

脚本支持：
- ✅ macOS 系统通知（自动）
- ✅ 飞书通知（通过 OpenClaw）
- 🔄 可扩展：Slack / Telegram / Discord

---

## 🔧 故障排查

### 健康检查不工作？

```bash
# 检查 cron 是否运行
crontab -l

# 检查日志
tail -f ~/.openclaw/logs/recovery.log

# 手动运行测试
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/recover-v2.sh
```

### 备份在哪里？

```bash
ls -la ~/.openclaw/backups/
```

---

## 📄 许可证

MIT License - 自由使用和修改

---

## 🙏 致谢

为 OpenClaw 社区打造，让每个人都能轻松运维自己的 AI 助手。

---

**Made with ❤️ for OpenClaw**
