# 🦞 MyOpenClaw Backup Restore �?跨平台备份还原工�?
> �?[MyClaw.ai](https://myclaw.ai) 开源技能生态提�?
**一个命令备份，一个命令还原。支�?Windows、macOS、Linux 互相备份还原�?*

�?Mac 上备份的文件，可以直接在 Windows 上还原；�?Linux 上备份的，可以直接在 Mac 上还原——任意组合都行�?
---

## 📖 目录

- [快速开始](#-快速开�?
- [备份了什么](#-备份了什�?
- [跨平台兼容性](#-跨平台兼容�?
- [命令详解](#-命令详解)
- [常用场景](#-常用场景)
- [HTTP 管理服务器](#-http-管理服务�?
- [安全说明](#-安全说明)
- [系统要求](#-系统要求)
- [常见问题](#-常见问题)

---

## 🚀 快速开�?
```bash
# 1. 备份（在任何系统上都一样）
node scripts/backup-restore.js backup

# 2. 查看所有备�?node scripts/backup-restore.js list

# 3. 还原前先预览（不会做任何修改�?node scripts/backup-restore.js restore <备份文件�? --dry-run

# 4. 确认没问题后正式还原
node scripts/backup-restore.js restore <备份文件�?
```

就这么简单。不需要安装任何额外依赖，�?Node.js 就行�?
---

## 📦 备份了什�?
| 组件 | 路径 | 内容说明 |
|------|------|----------|
| **工作空间** | `~/.openclaw/workspace/` | MEMORY.md（记忆）、SOUL.md（人格）、USER.md（用户信息）、自定义文件 |
| **团队工作�?* | `~/.openclaw/workspace-*/` | 多Agent团队的工作区（workspace-team、workspace-dev 等），自动发�?|
| **网关配置** | `openclaw.json` | Bot Token、API Key、渠道配置、模型设�?|
| **技�?* | `~/.openclaw/skills/` | 所有已安装的技�?|
| **扩展插件** | `~/.openclaw/extensions/` | 渠道扩展（飞书等�?|
| **凭证** | `~/.openclaw/credentials/` | 渠道配对状态（Telegram、WhatsApp 等） |
| **渠道状�?* | `~/.openclaw/{telegram,feishu,...}/` | 消息偏移量、会话数据（自动发现所有渠道目录） |
| **Agent 配置** | `~/.openclaw/agents/` | 模型提供商配置、完整对话历�?|
| **设备** | `~/.openclaw/devices/` | 已配对的手机/节点 |
| **身份** | `~/.openclaw/identity/` | 设备身份文件 |
| **定时任务** | `~/.openclaw/cron/` | 所�?Cron 定时任务 |
| **守护脚本** | `guardian.sh` �?| Linux/Mac 自动重启脚本 |
| **ClawHub** | `~/.openclaw/.clawhub/` | ClawHub 技能注册表数据 |
| **消息队列** | `~/.openclaw/delivery-queue/` | 待发送消息队�?|
| **记忆索引** | `~/.openclaw/memory/` | QMD 记忆搜索索引 |

### 不备份的内容（设计如此）

| 内容 | 原因 |
|------|------|
| `logs/` | 运行日志，不需要还�?|
| `media/` | 太大，容易重新生�?|
| `browser/` | 浏览器自动化数据，临时性质 |
| `canvas/` | 系统静态文件，�?OpenClaw 安装 |
| `completions/` | Shell 补全脚本，自动生�?|
| `node_modules/` | 重新 `npm install` 即可 |
| `.git/` | 源码管理独立处理 |
| 二进制媒体文�?| 图片/音频/视频太大 |
| `.lock`、`.deleted.*` | 临时状态文�?|

---

## 🌍 跨平台兼容�?
| 备份系统 �?还原系统 | Windows | macOS | Linux |
|---------------------|---------|-------|-------|
| **Windows** | �?| �?| �?|
| **macOS** | �?| �?| �?|
| **Linux** | �?| �?| �?|

**原理�?* 使用 tar.gz 格式（Windows 10+ / macOS / Linux 原生支持）。在没有 tar 的旧�?Windows 上自动降级为 ZIP 格式。还原时自动检测格式，无需手动处理�?
---

## 📖 命令详解

### 备份 (backup)

```bash
node scripts/backup-restore.js backup [--output-dir <目录>]
```

- 生成文件名格式：`openclaw-backup_{agent名}_{时间戳}.tar.gz`
- 默认保存到：`~/openclaw-backups/`
- 自动清理旧备份（保留最�?7 个）
- 自动排除大文件和不需要的文件
- �?Linux/Mac 上自动设�?`chmod 600`（仅所有者可读写�?- **自动发现**所�?`workspace-*` 目录和渠道目�?
**示例输出�?*
```
🦞 MyOpenClaw Backup Restore
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform:  win32 (x64)
Source:    C:\Users\you\.openclaw
Output:    C:\Users\you\openclaw-backups\openclaw-backup_mybot_20260307.tar.gz

[✓] Backing up workspace...
[✓]   workspace �?28 files (510 KB)
[✓] Backing up 4 extra workspace(s)...
[✓]   workspace-team �?76 files (233 KB)
[✓]   workspace-dev �?9 files (52 KB)
...
�?Backup complete!
   Archive: 8.50 MB  |  Files: 424
   Extra workspaces: workspace-team, workspace-dev, workspace-pm
```

### 还原 (restore)

```bash
# 第一步：一定先 dry-run 预览
node scripts/backup-restore.js restore <备份文件> --dry-run

# 第二步：确认无误后正式还�?node scripts/backup-restore.js restore <备份文件>

# 可选：覆盖 Gateway Token（同机器灾难恢复时使用）
node scripts/backup-restore.js restore <备份文件> --overwrite-gateway-token
```

**安全机制�?*

| 机制 | 说明 |
|------|------|
| **`--dry-run` 预览** | 只展示备份内容，不做任何修改 |
| **还原前自动快�?* | 正式还原前自动保存当前状态，搞砸了可以回�?|
| **Gateway Token 保留** | 默认保留新机器的 Token，防�?Control UI 出现 token 不匹�?|
| **交互确认** | 必须手动输入 `yes` 才会执行还原 |
| **凭证权限加固** | Linux/Mac 上还原后自动 `chmod 700/600` 保护凭证目录 |
| **自动重启网关** | 还原完成后自动重�?OpenClaw Gateway |
| **向后兼容** | 可还�?v1 (bash) �?v2 版本的备份文�?|

**dry-run 输出示例�?*
```
📋 Manifest:
  Backup:     openclaw-backup_mybot_20260307_181031
  Agent:      mybot
  Created:    2026-03-07T10:10:31Z
  From:       MacBookPro (darwin/arm64)
  OC version: 2026.3.2
  Tool ver:   3.0.0
  Extra WS:   workspace-team, workspace-dev
  Channels:   feishu, telegram

Contents:
  📁 workspace/ (28 files)
  📁 workspace-team/ (76 files)
  📁 agents/ (159 files)
  📁 skills/ (67 files)
  ...

Key files:
  �?workspace/MEMORY.md (Agent memory, 5.51 KB)
  �?workspace/SOUL.md (Agent personality, 1.67 KB)
  �?config/openclaw.json (Gateway config, 15.18 KB)

🔑 Gateway Token Strategy:
  Current server token preserved (6a61e7ad...87ff)

🔍 DRY RUN �?no changes made.
```

### 查看备份列表 (list)

```bash
node scripts/backup-restore.js list [--backup-dir <目录>]
```

**输出示例�?*
```
🦞 MyOpenClaw Backup Restores
Directory: ~/openclaw-backups

  📦 openclaw-backup_mybot_20260307_181031.tar.gz  8.50 MB  0m ago
  🔄 pre-restore_20260307_175000.tar.gz  7.80 MB  5m ago    �?还原前自动快�?  📦 openclaw-backup_mybot_20260306_030000.tar.gz  8.10 MB  1d ago
```

---

## 🔄 常用场景

### 场景一：日常手动备�?
```bash
node scripts/backup-restore.js backup
# �?~/openclaw-backups/openclaw-backup_mybot_20260307_180000.tar.gz
```

### 场景二：迁移到新电脑

**旧电脑：**
```bash
node scripts/backup-restore.js backup
# 通过 U�?/ 网盘 / 其他方式�?.tar.gz 拷贝到新电脑
```

**新电脑：**
```bash
# 1. 先安�?OpenClaw
npm i -g openclaw

# 2. 预览备份内容
node backup-restore.js restore openclaw-backup_mybot_20260307.tar.gz --dry-run

# 3. 正式还原
node backup-restore.js restore openclaw-backup_mybot_20260307.tar.gz

# 4. 完成！所有渠道自动重连，不需要重新配�?```

### 场景三：跨系统迁移（�?Mac �?Windows�?
完全一样的操作！在 Mac 上备份的文件，直接在 Windows 上还原：

```bash
# Mac 上：
node scripts/backup-restore.js backup

# �?.tar.gz 拷贝�?Windows，然后：
node scripts\backup-restore.js restore openclaw-backup_mybot_20260307.tar.gz
```

### 场景四：搞砸了，回滚

还原操作执行前会自动创建快照（`pre-restore_xxx.tar.gz`）：

```bash
# 查看所有备份（包括还原前快照）
node scripts/backup-restore.js list

# 用还原前的快照回�?node scripts/backup-restore.js restore pre-restore_20260307_175000.tar.gz
```

### 场景五：OpenClaw Cron 定时自动备份

�?OpenClaw 中创�?Cron 定时任务，每天凌�?3 点自动备份：

```bash
openclaw cron add --name "daily-backup" --schedule "0 3 * * *" --tz "Asia/Shanghai" \
  --agent main --message "运行备份：node ~/.openclaw/skills/openclaw-backup/scripts/backup-restore.js backup" --timeout 120
```

### 场景六：通过 HTTP 传输备份到另一台电�?
见下�?[HTTP 管理服务器](#-http-管理服务�? 部分�?
---

## 🌐 HTTP 管理服务�?
提供浏览器管理界面和远程上传/下载功能�?
### 启动

```bash
# 启动（Token 是必须的！）
node scripts/server.js --token 你的密码 [--port 7373] [--backup-dir <目录>]
```

### 访问

启动后在浏览器打开：`http://localhost:7373/?token=你的密码`

提供完整�?Web UI：创建备份、上传备份、下载备份、预览还原、执行还原�?
### API 端点

| 端点 | 远程访问（需 Token�?| 仅本�?|
|------|---------------------|--------|
| `GET /health` | ✅（无需 Token�?| �?|
| `GET /backups` | �?查看备份列表 | �?|
| `GET /download/:file` | �?下载备份 | �?|
| `POST /upload` | �?上传备份 | �?|
| `POST /backup` | �?| �?创建备份 |
| `POST /restore/:file` | �?| �?执行还原 |

> ⚠️ 创建备份和执行还�?*只能在本�?*操作（localhost），远程客户端只能上�?下载。这是安全设计�?
---

## 🔒 安全说明

备份文件中包�?*敏感信息**�?
- 🔑 Bot Token（Telegram、Discord、钉钉、飞书等�?- 🔑 API Key（模型提供商、各种服务）
- 🔑 渠道配对凭证
- 💬 完整对话历史

**安全建议�?*

1. **不要**�?`.tar.gz` 备份文件上传到公开�?Git 仓库
2. **不要**通过不加密的方式传输（用 scp/sftp 或加密网盘）
3. Linux/Mac 上备份文件自动设�?`chmod 600`（仅所有者可读写�?4. 还原后凭证目录自动加固权�?(`chmod 700/600`)
5. HTTP 服务器强制要�?Token，执行类操作限制本机访问
6. **总是**先用 `--dry-run` 预览，再执行还原

---

## 💻 系统要求

| 要求 | 说明 |
|------|------|
| **Node.js** | 18+（安�?OpenClaw 时已经有了） |
| **tar** | Windows 10+ / macOS / Linux 自带。旧�?Windows 自动降级�?ZIP |
| **磁盘空间** | 通常 5-50 MB（取决于对话历史和团队工作区大小�?|

**不需�?*：bash、rsync、python3。纯 Node.js 实现，零外部依赖�?
---

## �?常见问题

### Q: 还原�?Telegram/钉钉/飞书等渠道需要重新配对吗�?
**不需要�?* 备份包含了所有渠道配对状态，还原后自动重连。如�?Telegram 30 秒后还没响应，给你的 Bot 发一�?`/start` 即可�?
### Q: 还原�?Control UI（网页控制台）报 token mismatch�?
默认情况下，还原�?*保留新机器的 Gateway Token**，不会出现这个问题�?
如果你是在同一台机器上恢复（灾难恢复），可以加 `--overwrite-gateway-token` 使用备份中的 Token�?
### Q: 还原搞砸了怎么办？

还原前会自动创建快照（`pre-restore_xxx.tar.gz`），用它还原回去即可�?
```bash
node scripts/backup-restore.js list                          # 找到 pre-restore 文件
node scripts/backup-restore.js restore pre-restore_xxx.tar.gz  # 回滚
```

### Q: �?Mac 上备份的文件，Windows 上真的能直接还原�?
是的。tar.gz 是跨平台标准格式，Windows 10+ 原生支持。路径分隔符差异在还原时自动处理�?
### Q: 我有多个 Agent 团队（workspace-team），能备份吗�?
**v3.0 新功能：** 自动发现并备份所�?`workspace-*` 目录。无需任何配置，备份时会自动扫描并包含 workspace-team、workspace-dev 等所有额外工作区�?
### Q: 备份文件太大了？

正常情况�?5-50 MB。如果特别大，可能是对话历史太多。可以考虑�?- 清理 `~/.openclaw/agents/main/sessions/` 中的旧会�?- 清理 workspace 中不需要的大文�?
### Q: 怎么自动定期备份�?
推荐使用 OpenClaw 内置 Cron�?
```bash
openclaw cron add --name "daily-backup" --schedule "0 3 * * *" --tz "Asia/Shanghai" \
  --agent main --message "运行备份" --timeout 120
```

### Q: Agent 怎么知道发生了还原？

还原完成后会�?workspace 下写�?`.restore-complete.json` 标记文件，Agent 下次启动时自动读取并发送还原报告，然后删除标记（一次性通知）�?
### Q: 旧版本（v1/v2）的备份文件能用 v3 还原吗？

**可以�?* v3 的还原功能向后兼容，能识�?v1（bash 生成的）�?v2 的备份格式�?
---

## 📁 文件结构

```
openclaw-backup/
├── SKILL.md                    # 技能定义（�?OpenClaw Agent 读的�?├── README.md                   # 本文档（给人读的�?├── _meta.json                  # 技能元信息
├── references/
�?  └── what-gets-saved.md      # 备份内容详细说明
└── scripts/
    ├── backup-restore.js       # �?核心脚本 �?备份/还原/列表，跨平台
    ├── server.js               # HTTP 管理服务器，跨平�?    └── ui.html                 # Web 管理界面
```

---

## 📜 版本历史

- **v3.0.0** �?全面升级。新增：自动发现并备�?workspace-* 多Agent团队工作区、extensions 扩展插件、ClawHub 注册表、delivery-queue 消息队列、memory 记忆索引。自动发现渠道目录（不再硬编码）。改�?multipart 上传解析器。移除冗�?bash 脚本（backup.sh/restore.sh/serve.sh/schedule.sh），统一使用 Node.js 跨平台实现。向后兼�?v1/v2 备份格式�?- **v2.0.0** �?跨平台重写。新�?`backup-restore.js`（Node.js），支持 Windows/Mac/Linux 互相备份还原�?- **v1.x** �?原版。bash 脚本实现，仅支持 Linux/Mac�?
---

## 🤝 贡献

本技能是 [MyClaw.ai](https://myclaw.ai) 开源技能生态的一部分。欢迎提�?Issue �?PR�?
**许可证：** MIT
