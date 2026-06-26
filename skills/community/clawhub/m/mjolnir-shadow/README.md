# 🌑 Mjolnir Shadow (雷神之影)

> *Like a shadow — silent, faithful, always there.*
> *如影随形，默默守护。*

**OpenClaw 智能体的自动备份与一键恢复系统。**

让你的 AI 智能体永远不会失忆——哪怕系统崩了、电脑换了，一条命令就能满血复活。

---

## 🤔 这是什么？为什么需要它？

你的 OpenClaw 智能体会积累记忆、学会你的习惯、记住你的项目进度。但如果系统崩了、换了电脑、或者不小心删了文件——**这些记忆就全没了**。

**雷神之影**就是你的保险：
- ⏰ **自动备份** — 定时把记忆、配置、技能打包上传到你的私有云
- 🔐 **安全加密** — 凭证用 GPG 加密，不怕泄露
- 🔄 **智能轮转** — 自动保留最近 N 个备份，不占满存储
- 🚀 **一键恢复** — 系统挂了？一条命令，5 分钟满血复活

---

## 📦 雷神四件套

雷神之影是「**雷神系列**」开源工具集的一员：

| 工具 | 用途 | 状态 |
|------|------|------|
| 🧠 [雷神之脑](https://github.com/king6381/mjolnir-brain) | AI Agent 自进化记忆系统 | ✅ 已发布 |
| 🌑 **雷神之影** (本项目) | 自动备份与一键恢复 | ✅ 已发布 |
| 🛡️ 雷神之盾 | GPG 加密凭证管理 | 🔧 内部使用 |
| ⚡ 雷神之锤 | A 股智能量化分析 | 🔒 私有 |

装了这四件套，你的 OpenClaw 智能体就有了：**长期记忆 + 数据安全 + 密码管理 + 量化分析**。

---

## 🚀 5 分钟上手指南

> **适合人群**：从没用过 Linux 命令行也没关系，跟着步骤走就行。

### 前提条件

你需要：
- 一台电脑（**Windows 11**、**macOS**、**Ubuntu** 都行）
- 一个 WebDAV 存储（Nextcloud、群晖 NAS、ownCloud 都行）
- OpenClaw 会在恢复过程中自动安装，不用提前装

| 你的系统 | 用哪个脚本 | 怎么运行 |
|---------|-----------|---------|
| 🪟 **Windows 11** | `restore-kit.ps1` | PowerShell 管理员运行（自动装 WSL2 + Ubuntu） |
| 🍎 **macOS** | `restore-kit.sh` | 终端运行 `bash restore-kit.sh` |
| 🐧 **Ubuntu** | `restore-kit.sh` | 终端运行 `bash restore-kit.sh` |

> 💡 **Windows 用户不用怕 Linux！** PowerShell 脚本会自动帮你装好 WSL2 和 Ubuntu，全程中文提示，点点鼠标就行。

### 第 1 步：安装雷神之影

```bash
# 方式 A：如果你有 OpenClaw（推荐）
# 直接复制到技能目录
cp -r mjolnir-shadow ~/.openclaw/workspace/skills/

# 方式 B：从 GitHub 克隆
git clone https://github.com/king6381/mjolnir-shadow.git
cd mjolnir-shadow
```

### 第 2 步：配置你的存储

运行配置向导，跟着提示一步步填：

```bash
python3 scripts/setup_backup.py
```

向导会问你：
1. **WebDAV 地址** — 你的 Nextcloud/NAS 的 WebDAV 地址
2. **用户名和密码** — 登录凭证（会用 GPG 加密保存）
3. **备份频率** — 几天备份一次（默认 3 天）
4. **保留数量** — 保留几个备份（默认 3 个）

> 💡 **小贴士**：如果你用群晖 NAS，WebDAV 地址通常是 `http://你的NAS_IP:5005`
> 如果你用 Nextcloud，地址通常是 `http://你的IP/remote.php/webdav`

### 第 3 步：首次备份

```bash
bash scripts/backup.sh
```

你会看到：
```
🌑 Mjolnir Shadow Backup - 2026-03-23_2200
==========================================
📦 Packing workspace...
📦 Packing config...
📦 Packing skills...
📤 Uploading...
✅ Upload successful! HTTP 201
==========================================
🌑 Mjolnir Shadow - SUCCESS
📦 Size: 2.1M
🔄 Rotation: 1/3 slots used
==========================================
```

**恭喜！你的智能体已经有了第一份保险。** 🎉

### 第 4 步：设置自动备份（可选但强烈推荐）

让它每 3 天自动跑一次，你再也不用操心：

```bash
# 在 OpenClaw 里添加定时任务
openclaw cron add --name "🌑 雷神之影" \
  --schedule "0 3 */3 * *" --tz "Asia/Shanghai" \
  --isolated --timeout 300 \
  --message "bash ~/path/to/scripts/backup.sh"
```

> 💡 这表示每 3 天凌晨 3 点自动备份。你睡觉的时候，雷神之影替你守护数据。

---

## 🆘 灾难恢复 — 系统崩了怎么办？

> **这是最重要的部分。** 收藏这一节，关键时刻救命。

### 场景 1：OpenClaw 还在，只是数据丢了

一条命令搞定：

```bash
bash scripts/restore.sh --auto
```

你会看到进度条一步步走完：

```
🌑 ═══════════════════════════════════════════
   雷神之影 — 一键全自动恢复
🌑 ═══════════════════════════════════════════

  [███░░░░░░░░░░░░░░░░░░░░░░░░░░░]  16%  🔐 解密配置文件...
       ✓ 配置加载成功

  [██████░░░░░░░░░░░░░░░░░░░░░░░░]  33%  🔍 查找最新备份...
       ✓ 找到: backup_2026-03-23_0300.tar.gz (2026-03-23)

  [█████████░░░░░░░░░░░░░░░░░░░░░]  50%  📥 下载备份包...
       ✓ 下载完成 (2.1M)

  [████████████░░░░░░░░░░░░░░░░░░]  66%  📦 解压备份包...
       ✓ 解压完成: workspace.tar.gz, config.tar.gz, skills.tar.gz

  [███████████████░░░░░░░░░░░░░░░]  83%  🔄 恢复文件到系统...
       ✓ workspace → ~/.openclaw/workspace
       ✓ config → ~/.openclaw
       ✓ skills → ~/.openclaw/workspace/skills/
       ✓ 共恢复 3 个组件

  [██████████████████████████████] 100%  🚀 重启 OpenClaw...
       ✓ OpenClaw 已重启

🌑 ═══════════════════════════════════════════
   ✅ 恢复完成！
🌑 ═══════════════════════════════════════════

  📦 备份文件: backup_2026-03-23_0300.tar.gz
  📅 备份日期: 2026-03-23
  🔄 恢复组件: 3 个

  智能体下次醒来就有完整记忆了 🧠
```

### 场景 2：全新电脑，什么都没装

**这才是真正的考验。** 你的电脑炸了，换了一台全新的，什么都没有。

别慌。拿出你提前备份的恢复脚本（U 盘、邮箱、网盘都行），然后根据你的系统：

#### 🪟 Windows 11

```powershell
# 右键 PowerShell → "以管理员身份运行"，然后：
Set-ExecutionPolicy Bypass -Scope Process -Force
.\restore-kit.ps1
```

脚本会自动完成：
1. ✅ 检测 Windows 版本
2. ✅ 安装 WSL2（可能需要重启一次）
3. ✅ 安装 Ubuntu
4. ✅ 在 Ubuntu 里装 Node.js + OpenClaw
5. ✅ 连接你的 WebDAV 备份存储
6. ✅ 下载并恢复所有数据
7. ✅ 启动智能体

> 💡 如果提示需要重启，重启后再运行一次就行，脚本会自动从断点继续。

#### 🍎 macOS / 🐧 Ubuntu

```bash
bash restore-kit.sh
```

脚本会自动完成：
1. ✅ 检测系统 + 安装缺失依赖
2. ✅ 安装 Node.js v22
3. ✅ 安装 OpenClaw
4. ✅ 连接 WebDAV + 下载备份
5. ✅ 恢复数据 + 启动智能体

效果预览：

```
🌑 ════════════════════════════════════════════════════════
   雷神之影 — 一键恢复引导 (Restore Kit v2.0)
   从全新电脑到满血复活，一条命令搞定
🌑 ════════════════════════════════════════════════════════

  [██████████████████████████████] 100%

  ✅ 完美！从裸机到满血，一步到位！

  📦 备份来源:  backup_2026-03-23_0300.tar.gz
  📅 备份日期:  2026-03-23
  🔄 恢复组件:  4 个

  🧠 智能体下次醒来就有完整记忆了！
```

> **重点**：恢复脚本是**完全独立**的——不需要提前装任何东西。
> Windows 只要有 PowerShell，macOS/Ubuntu 只要有 bash。
> 这就是为什么你应该**把它单独备份一份**（U 盘、邮箱、打印出来贴墙上都行 😄）。

### 场景 3：想看看有哪些备份

```bash
bash scripts/restore.sh --list
```

```
🌑 可用备份列表

  1. 📦 backup_2026-03-20_0300.tar.gz  (2026-03-20)
  2. 📦 backup_2026-03-23_0300.tar.gz  (2026-03-23)
```

### 场景 4：想恢复特定版本（不是最新的）

```bash
bash scripts/restore.sh --file backup_2026-03-20_0300.tar.gz
```

---

## 📋 命令速查表

| 我想... | 命令 |
|---------|------|
| 首次配置 | `python3 scripts/setup_backup.py` |
| 手动备份一次 | `bash scripts/backup.sh` |
| 查看备份列表 | `bash scripts/restore.sh --list` |
| **一键恢复（推荐）** | `bash scripts/restore.sh --auto` |
| 🐧🍎 全新系统恢复 | `bash scripts/restore-kit.sh` |
| 🪟 Win11 全新恢复 | `.\restore-kit.ps1`（管理员 PowerShell） |
| 恢复最新（手动模式） | `bash scripts/restore.sh --latest` |
| 恢复指定版本 | `bash scripts/restore.sh --file <名字>` |

---

## 🔒 安全设计

**你的数据安全是第一优先级。**

| 安全措施 | 说明 |
|---------|------|
| 🔐 **GPG 加密** | 你的 WebDAV 密码用 AES-256 加密存储，不是明文 |
| 🔒 **进程隐藏** | 所有 curl 请求用 `--netrc-file`，`ps` 命令看不到密码 |
| ⚠️ **HTTPS 提醒** | 如果你的地址不是 HTTPS，脚本会警告你 |
| 🚫 **敏感排除** | `.gpg`、`.key`、`.secret`、`.env` 文件永远不会被备份 |
| 🧹 **自动清理** | 临时文件（包括 netrc）在脚本结束时自动删除，崩溃也不留 |
| 🔑 **通道保护** | 微信/QQ 等登录 token 默认不备份（防止 token 泄露） |

---

## 📦 备份了什么？没备份什么？

### ✅ 会备份的

| 类型 | 包含内容 |
|------|---------|
| **记忆文件** | MEMORY.md、memory/*.md（你的智能体的全部记忆） |
| **人格文件** | SOUL.md、IDENTITY.md、USER.md（智能体的性格和对你的了解） |
| **配置文件** | openclaw.json、定时任务（cron） |
| **工作文档** | AGENTS.md、TOOLS.md 及 workspace 下所有文件 |
| **技能包** | 已安装的所有技能（包括雷神之影自己） |
| **交易策略** | 策略文件和监控脚本（如果有） |

### ❌ 不会备份的（安全考虑）

| 类型 | 原因 |
|------|------|
| `.git/` 目录 | 太大，可以重新 clone |
| `node_modules/` | 太大，可以重新 npm install |
| `venv/` 虚拟环境 | 太大，可以重新创建 |
| `.env` 环境变量 | 可能包含密钥 |
| `*.gpg` 加密文件 | 已经是加密的凭证 |
| 微信/QQ 登录 token | 安全原因，需要重新扫码 |

---

## 🔄 轮转机制

雷神之影不会无限占用存储空间：

```
第 1 次备份:  [A]
第 2 次备份:  [A] [B]
第 3 次备份:  [A] [B] [C]          ← 存满了（默认保留 3 个）
第 4 次备份:  [B] [C] [D]          ← A 自动删除
第 5 次备份:  [C] [D] [E]          ← B 自动删除
```

始终保留最近 N 个备份（默认 3 个），旧的自动清理。

---

## 🛠️ 高级配置

### 修改备份参数

配置文件在 `config/backup-config.json`（GPG 加密）。重新运行向导即可修改：

```bash
python3 scripts/setup_backup.py
```

可配置项：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `webdav_url` | — | WebDAV 地址（必填） |
| `webdav_user` | — | 用户名（必填） |
| `webdav_pass` | — | 密码（必填，加密存储） |
| `remote_dir` | `openclaw-backups` | 远程备份目录名 |
| `max_backups` | `3` | 最多保留几个备份 |
| `interval_days` | `3` | 自动备份间隔（天） |
| `backup_workspace` | `true` | 是否备份工作空间 |
| `backup_config` | `true` | 是否备份配置 |
| `backup_strategies` | `true` | 是否备份交易策略 |
| `backup_skills` | `true` | 是否备份技能包 |
| `exclude_channel_auth` | `true` | 是否排除通道认证 token |

### 定时备份（Cron）

```bash
# 每 3 天凌晨 3 点自动备份
openclaw cron add --name "🌑 雷神之影" \
  --schedule "0 3 */3 * *" --tz "Asia/Shanghai" \
  --isolated --timeout 300 \
  --message "bash /path/to/scripts/backup.sh"
```

### 非交互式运行（服务器/Cron 场景）

定时任务运行时没人输密码，需要提前设置：

```bash
# 推荐：用 gpg-agent 缓存密码
gpg-connect-agent /bye

# 或者：设置环境变量（通过安全的密钥管理器）
export MJOLNIR_SHADOW_PASS="$(your-secret-manager get mjolnir-shadow-pass)"
```

> ⚠️ **绝对不要**在 cron 命令或明文文件里写密码。

---

## ❓ 常见问题 (FAQ)

### Q: 我的 NAS 重启后备份会失败吗？
**A:** 会。NAS 重启后 WebDAV 服务可能没有自动启动，检查一下 NAS 的 WebDAV 设置。

### Q: 备份文件有多大？
**A:** 取决于你的 workspace 大小。一般 1-5MB，非常小。

### Q: 可以备份到多个地方吗？
**A:** 目前支持一个 WebDAV 目标。如果需要多份备份，可以在 NAS 端设置同步。

### Q: restore-kit.sh 需要 GPG 吗？
**A:** 如果你之前的配置是 GPG 加密的，恢复时需要 GPG + 密码。如果是明文配置，不需要。但在 restore-kit.sh 的交互模式下（手动输入驿站信息），完全不需要 GPG。

### Q: 支持哪些操作系统？
**A:** 三大平台全覆盖：
- 🪟 **Windows 11** — PowerShell 脚本自动装 WSL2（需要 Build 19041+）
- 🍎 **macOS** — 原生 bash 支持（需要 Homebrew）
- 🐧 **Ubuntu/Debian** — 原生支持

### Q: 支持哪些 WebDAV 服务？
**A:** 已测试：✅ Nextcloud、✅ ownCloud、✅ 群晖 NAS、✅ Apache mod_dav

### Q: 换了电脑，恢复脚本怎么拿到？
**A:** 提前备一份！建议：
- 📧 发一份到自己邮箱（Win11 存 `.ps1`，Mac/Ubuntu 存 `.sh`，或者两个都存）
- 💾 U 盘存一份
- ☁️ 网盘存一份
- 🖨️ 打印出来（没开玩笑，关键时刻纸比电子靠谱）

### Q: Windows 用户需要学 Linux 吗？
**A:** 完全不需要！PowerShell 脚本会自动帮你装好 WSL2 和 Ubuntu，全程中文提��。装完后日常使用也只要在开始菜单搜 "Ubuntu" 打开就行。

---

## 📁 项目结构

```
mjolnir-shadow/
├── README.md                   # 你正在看的这个文件
├── SKILL.md                    # OpenClaw 技能清单
├── LICENSE                     # MIT 开源许可证
├── scripts/
│   ├── backup.sh               # 核心备份脚本（带轮转）
│   ├── restore.sh              # 恢复工具（支持 --auto 一键模式）
│   ├── restore-kit.sh          # 🐧🍎 独立恢复引导（Ubuntu/macOS，零依赖）
│   ├── restore-kit.ps1         # 🪟 Windows 11 恢复引导（自动装 WSL2）
│   └── setup_backup.py         # 交互式配置向导
├── references/
│   └── config-reference.md     # 配置详细文档
└── config/                     # 你的配置（git-ignored，不会上传）
    └── backup-config.json.gpg  # GPG 加密的配置文件
```

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) — 让 AI 智能体真正有用的开源平台
- 所有给 Star 的朋友们 ⭐

---

## 📜 法律与知识产权

### 版权

Copyright © 2026 King Lei (雷哥). All rights reserved.

**雷神系列** 品牌名称，包括但不限于 **雷神之脑**、**雷神之影**、**雷神之盾**、**雷神之锤** 及所有相关标识，均为 King Lei 的商标。

### 许可证

本项目采用 **MIT 许可证** — 详见 [LICENSE](LICENSE)。

你可以自由使用、修改和分发本软件。但 **雷神系列** 品牌名称未经书面许可不得用于衍生作品。

### 联系方式

- 📧 **Email**: king6381@hotmail.com
- 🐙 **GitHub**: [@king6381](https://github.com/king6381)
- 📱 **微信公众号**: 雷哥玩AI

商务合作、品牌授权请联系。

---

*Built with ❤️ by a 45-year-old who learned AI and decided to protect everyone's data.*

*一个 45 岁学 AI 的人，决定守护所有人的数据安全。*

**⭐ 觉得有用？给个 Star，让更多人看到！**
