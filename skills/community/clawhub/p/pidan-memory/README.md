# 🧠 Pidan Memory

本地持久化向量记忆系统，为 AI Assistant 提供长期记忆能力。

[简体中文](./README.md) | [English](./README_EN.md)

## ✨ 特性

- 📦 **向量存储** - 基于 LanceDB + Ollama，本地向量语义搜索
- 🔄 **自动记忆** - 每次对话自动评估存储（需安装 Hook）
- 👥 **多用户/共享模式** - 支持私有隔离和共享模式切换
- 🧹 **自动去重** - 每 20 条自动触发去重
- 🔐 **安全删除** - 只有创建人可删除，需二次确认
- 🔍 **语义搜索** - 支持自然语言查询

## 快速开始

### 1. 安装

```bash
# 方式一：ClawHub 安装（推荐）
clawhub install pidan-memory

# 方式二：手动安装
cd ~/.openclaw/workspace/skills
git clone https://github.com/your-repo/pidan-memory.git
```

### 2. 启动 Ollama

```bash
# 启动 Ollama 服务
ollama serve

# 下载 embedding 模型（首次）
ollama pull nomic-embed-text
```

### 3. 安装 Hook（启用自动记忆）

```bash
# 复制 Hook 文件
mkdir -p ~/.openclaw/hooks/pidan-memory
cp HOOK.md handler.ts ~/.openclaw/hooks/pidan-memory/
cp auto_memory.py ~/.openclaw/workspace/memory/

# 启用 Hook
openclaw hooks enable pidan-memory

# 重启 Gateway
openclaw gateway restart
```

## 使用方法

### 自动记忆（推荐）

安装 Hook 后，每次对话自动评估并存储。覆盖 16 大类场景。

### 模式管理

```bash
# 获取当前模式
echo '{"command": "get_mode", "parameters": {}}' | python3 run.py

# 切换到共享模式
echo '{"command": "set_mode", "parameters": {"mode": "shared"}}' | python3 run.py

# 切换回私有模式
echo '{"command": "set_mode", "parameters": {"mode": "private"}}' | python3 run.py
```

**模式说明：**
- `private` (默认): 多用户模式，记忆隔离
- `shared`: 共享模式，所有用户可互相查询

### 其他命令

```bash
# 记住信息
echo '{"command": "remember", "parameters": {"content": "用户最喜欢吃火锅", "importance": 4}}' | python3 run.py

# 搜索记忆
echo '{"command": "recall", "parameters": {"query": "饮食偏好"}}' | python3 run.py

# 查看最近记忆
echo '{"command": "recent_memories", "parameters": {"limit": 10}}' | python3 run.py

# 删除记忆（首次请求，确认）
echo '{"command": "delete_memory", "parameters": {"memory_id": "xxx", "confirm": true}}' | python3 run.py

# 手动去重
echo '{"command": "deduplicate", "parameters": {}}' | python3 run.py

# 查看统计
echo '{"command": "stats", "parameters": {}}' | python3 run.py
```

## 配置

配置文件：`~/.openclaw/workspace/memory/config.yaml`

```yaml
memory:
  mode: private              # private | shared
  deduplicate_after: 20     # 每N条自动去重
```

或环境变量：
```bash
MEMORY_MODE=private
MEMORY_DEDUP_AFTER=20
```

## 文件说明

```
pidan-memory/
├── SKILL.md           # Skill 定义
├── skill.json         # 元数据 v2.0.0
├── run.py             # CLI 入口
├── memory_lance.py    # 向量存储核心
├── auto_memory.py     # 自动记忆脚本
├── handler.ts         # Hook 处理器
├── HOOK.md            # Hook 元数据
├── _meta.json         # ClawHub 元数据
├── requirements.txt    # Python 依赖
└── scripts/          # 辅助脚本
```

## 更新日志

### v2.0.0
- ✨ 多用户/共享模式支持
- 🧹 自动去重功能
- 🔐 安全删除（权限校验 + 二次确认）
- 📝 完善文档
