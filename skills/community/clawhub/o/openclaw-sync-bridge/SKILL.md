# OpenClaw Sync Bridge Skill

使用 GitHub Gist 作为中转，安全同步 OpenClaw 配置到多设备。

## 核心特性

### 1. 智能工作目录检测
- 自动扫描常见路径
- 支持环境变量 `OPENCLAW_WORKSPACE`
- 多候选时交互选择

### 2. 安全的双向同步
- **push** - 本地 → 云端（预览 + 确认）
- **pull** - 云端 → 本地（预览 + 确认）
- **diff** - 先对比，再决定

### 3. 自动备份
- 覆盖前自动创建备份
- 保留最近 10 个版本
- 备份位置：`.sync-bridge-backup/`

### 4. Token 检测
- 自动验证 GitHub Token
- 过期时友好提示重新申请

## 安装

### 自动安装

**Mac/Linux:**
```bash
curl -fsSL https://clawhub.ai/JayShna/openclaw-sync-bridge/install.sh | bash
```

**Windows:**
```powershell
irm https://clawhub.ai/JayShna/openclaw-sync-bridge/install.ps1 | iex
```

### 手动安装

1. 下载 skill 文件夹
2. 运行对应平台的 `install.sh` 或 `install.ps1`
3. 按提示完成配置

## 首次配置

运行交互式向导：
```bash
python3 sync_bridge.py setup
```

向导会引导你完成：
1. 选择/确认工作目录
2. 输入 GitHub Token
3. 选择同步方向

## 命令详解

### setup - 配置向导
```bash
python3 sync_bridge.py setup
```
- 检测工作目录
- 验证/输入 Token
- 选择同步方向
- 完成首次同步

### push - 上传到云端
```bash
python3 sync_bridge.py push
```
- 显示文件预览
- 确认后上传
- 自动备份云端旧文件

### pull - 下载到本地
```bash
python3 sync_bridge.py pull
```
- 显示文件预览
- 确认后下载
- 自动备份本地旧文件

### diff - 对比差异
```bash
python3 sync_bridge.py diff
```
- 统计差异文件数
- 预览具体修改内容
- 支持交互式查看

### status - 查看状态
```bash
python3 sync_bridge.py status
```
- Token 有效性
- 云端文件数
- 本地文件数
- 备份历史

### backup - 手动备份
```bash
python3 sync_bridge.py backup
```
- 立即创建备份
- 清理旧备份（保留10个）

## 同步内容

默认同步：
- `SOUL.md` - AI 人格设定
- `AGENTS.md` - 工作区配置
- `USER.md` - 用户信息
- `IDENTITY.md` - 身份设定
- `TOOLS.md` - 工具配置
- `skills/` - 所有技能目录

自动排除：
- 含敏感信息的文件（config.json, .env）
- 密钥文件（*.token, *.key）
- 备份目录

## 安全设计

1. **本地优先** - 不自动同步，每次需确认
2. **备份机制** - 覆盖前自动备份
3. **敏感排除** - 自动识别敏感文件
4. **Token 管理** - 本地存储，不上传

## 多设备同步流程

```
设备 A (Mac)
  ↓ python sync_bridge.py push
GitHub Gist (中转)
  ↓ python sync_bridge.py pull
设备 B (云端/Windows)
```

两边使用相同的 Token 和 Gist ID 即可互通。

## 配置格式

`sync_config.json`:
```json
{
  "token": "ghp_xxxxxxxx",
  "gist_id": "abc123...",
  "workspace": "/path/to/workspace",
  "sync_files": ["SOUL.md", "AGENTS.md", "skills/"]
}
```

## 故障排查

| 问题 | 解决 |
|------|------|
| 未找到工作目录 | 手动输入或设置 `OPENCLAW_WORKSPACE` |
| Token 验证失败 | 重新申请 GitHub Token |
| 没有文件上传 | 确认工作目录有 SOUL.md 等文件 |
| 云端没有文件 | 先在另一设备执行 push |

## GitHub Token 申请

1. 访问 https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾选 `gist` 权限
4. 复制 Token 保存

## 更新日志

### v2.0.0
- 新增智能工作目录检测
- 新增上传/下载确认和预览
- 新增 diff 差异对比
- 新增自动备份机制
- 新增 Token 有效性检测
- 优化安装脚本

### v1.0.0
- 基础 push/pull 功能
- GitHub Gist 中转
- 敏感文件排除
