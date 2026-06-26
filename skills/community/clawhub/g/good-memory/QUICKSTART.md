# Good Memory 快速开始

## 功能
Session重置后自动恢复对话上下文，解决系统自动重置导致的"失忆"问题。

## 安装方式

### 🚀 快速安装（单Agent，推荐普通用户）
```bash
# 下载并解压到skills目录
mkdir -p ~/.openclaw/workspace/skills/good-memory
cd ~/.openclaw/workspace/skills/good-memory
curl -L https://wry-manatee-359.convex.site/api/v1/download?slug=good-memory | unzip -

# 执行单Agent安装（默认main）
INSTALL_MODE=single TARGET_AGENT=main bash scripts/install.sh
```

### 🔧 完整安装（多Agent，管理员使用）
```bash
# 下载并解压到skills目录
mkdir -p ~/.openclaw/workspace/skills/good-memory
cd ~/.openclaw/workspace/skills/good-memory
curl -L https://wry-manatee-359.convex.site/api/v1/download?slug=good-memory | unzip -

# 执行全Agent安装
bash scripts/install.sh
```

## 环境变量（可选）
如果你的OpenClaw安装在非默认路径，可以设置：
```bash
export OPENCLAW_BASE="/path/to/your/openclaw"
export TRACKER_FILE="/path/to/your/session-tracker.json"
```

## 使用说明
安装后无需额外操作，每次session启动时会自动：
1. 检测是否发生了重置
2. 如果检测到重置，自动恢复上一段对话的最后20-30条记录
3. 首条回复会提示：`已自动恢复 X月X日 XX:XX 之后说的话 📜 如果想要回忆更早的请对我说`

## 手动恢复
如果需要手动恢复更早的历史：
```bash
# 查看某Agent的所有重置历史
bash ~/.openclaw/workspace/skills/good-memory/scripts/recovery.sh list main

# 读取最新重置的100条记录
bash ~/.openclaw/workspace/skills/good-memory/scripts/recovery.sh read main --lines 100
```

## 支持平台
- ✅ 飞书
- ✅ Discord
- ✅ Telegram
- ✅ Signal
- ✅ 所有OpenClaw支持的聊天平台
