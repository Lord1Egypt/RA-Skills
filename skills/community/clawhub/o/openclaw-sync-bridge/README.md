# OpenClaw Sync Bridge Skill v2.0

一键同步 OpenClaw 配置到云端，**智能检测工作目录**，**上传/下载确认**，**自动备份**，安全可靠。

## ✨ 特性

- 🎯 **智能检测** - 自动寻找 OpenClaw 工作目录（支持自定义路径）
- 🔄 **双向确认** - push/pull 前显示文件预览，支持差异对比
- 💾 **自动备份** - 覆盖前自动备份，保留最近 10 个版本
- 🔐 **Token 检测** - 自动验证 GitHub Token 有效性
- 📊 **差异对比** - `diff` 命令查看本地与云端文件差异
- 🖥️ **跨平台** - Mac / Windows / Linux 全支持

## 🚀 快速开始

### 安装

**Mac/Linux:**
```bash
curl -fsSL https://clawhub.ai/JayShna/openclaw-sync-bridge/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://clawhub.ai/JayShna/openclaw-sync-bridge/install.ps1 | iex
```

**或手动安装:**
```bash
# 1. 安装 skill
openclaw skills install openclaw-sync-bridge

# 2. 进入目录
cd ~/.openclaw/workspace/skills/openclaw-sync-bridge

# 3. 运行安装脚本
bash install.sh      # Mac/Linux
# 或
.\install.ps1        # Windows
```

### 首次配置

```bash
python3 sync_bridge.py setup
```

安装向导会：
1. 🔍 自动寻找工作目录
2. 🔑 验证 GitHub Token
3. 🆕 创建 Gist（如需）
4. 🎯 选择同步方向

## 📖 使用指南

### 命令列表

| 命令 | 说明 |
|------|------|
| `setup` | 交互式配置向导（推荐首次使用） |
| `push` | 上传本地 → 云端（带预览和确认） |
| `pull` | 下载云端 → 本地（带预览和确认） |
| `diff` | 对比本地与云端文件差异 |
| `status` | 查看同步状态和统计 |
| `backup` | 手动创建备份 |

### 典型工作流

```
Mac 本地修改 SOUL.md
        ↓
python3 sync_bridge.py push
  📋 显示预览：
     🆕 新增: 0 个
     📝 修改: 1 个 (SOUL.md)
  确认上传? [y/N/diff]: y
        ↓
✅ 上传成功！
        ↓
云端 OpenClaw
  python3 sync_bridge.py pull
    📋 显示预览：
       📝 覆盖: 1 个 (SOUL.md)
    确认下载? [y/N/diff]: y
          ↓
  ✅ 下载成功！（自动备份旧文件）
```

## 🔐 GitHub Token 申请

1. 访问 https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 勾选 `gist` 权限
4. 复制生成的 Token

## 📁 同步内容

默认同步以下文件/目录：
- `SOUL.md` - 人格设定
- `AGENTS.md` - 工作区配置
- `USER.md` - 用户信息
- `IDENTITY.md` - 身份设定
- `TOOLS.md` - 工具配置
- `skills/` - 所有技能

**自动排除**（不上传）：
- `config.json` - 敏感配置
- `.env` - 环境变量
- `*.token`, `*.key` - 密钥文件
- `.sync-bridge-backup/` - 备份目录

## 🛡️ 安全特性

- **备份机制** - 每次覆盖前自动备份到 `.sync-bridge-backup/YYYYmmdd_HHMMSS/`
- **Token 检测** - 自动验证 GitHub Token，过期时提醒重新申请
- **敏感文件排除** - 自动识别并跳过含敏感信息的文件
- **差异预览** - 上传/下载前可查看具体差异

## 🔧 高级配置

### 环境变量

```bash
export OPENCLAW_WORKSPACE=/path/to/workspace  # 指定工作目录
```

### 自定义同步列表

编辑 `sync_config.json`：
```json
{
  "sync_files": ["SOUL.md", "AGENTS.md", "my-custom-skill/"]
}
```

## ❓ 故障排查

### "未找到工作目录"
- 手动输入工作目录路径
- 或设置环境变量 `export OPENCLAW_WORKSPACE=/path`

### "Token 无效或已过期"
- 重新申请 GitHub Token
- 运行 `python3 sync_bridge.py setup` 更新

### "没有找到文件"
- 确认工作目录下有 `SOUL.md` 或 `AGENTS.md`
- 或运行 `setup` 重新配置

## 📄 License

MIT
