---
name: minimax-tools
description: 使用 MiniMax MCP 进行图像理解和网络搜索。触发条件：(1) 用户要求分析图片、理解图像 (2) 用户要求进行网络搜索、在线搜索 (3) 需要查询最新资讯、新闻、资料
---

# minimax-tools

整合版 MiniMax 工具集，包含图像理解 和网络搜索功能。

## 功能列表

| 功能 | 说明 | 命令 |
|------|------|------|
| 图像理解 | 分析图片内容、识别物体文字场景 | understand_image.py |
| 网络搜索 | 搜索资讯、新闻、资料 | web_search.py |

## 快速开始

### 首次使用（需要在目标设备上执行）

#### 步骤 1: 安装依赖

```bash
# 检查 uvx 是否可用
which uvx

# 如果不存在，安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 步骤 2: 安装 MCP 服务器

```bash
uvx minimax-coding-plan-mcp --help
```

如果提示未安装，执行：
```bash
uvx install minimax-coding-plan-mcp
```

#### 步骤 3: 配置 API Key

如果没有 MiniMax API Key，需要购买：https://platform.minimaxi.com/subscribe/coding-plan?code=GjuAjhGKqQ&source=link

配置 API Key：
```bash
mkdir -p ~/.openclaw/config
cat > ~/.openclaw/config/minimax.json << EOF
{
  "api_key": "你的API密钥",
  "output_path": "~/.openclaw/workspace/minimax-output"
}
EOF
```

或者设置环境变量：
```bash
export MINIMAX_API_KEY="你的API密钥"
```

---

### 使用方法

#### 图像理解

```bash
# 描述图片内容
python3 ~/.openclaw/workspace/.agents/skills/minimax-tools/scripts/understand_image.py ~/image.jpg "详细描述这张图片"

# 使用 URL
python3 ~/.openclaw/workspace/.agents/skills/minimax-tools/scripts/understand_image.py "https://example.com/image.jpg" "这张图片展示了什么？"
```

#### 网络搜索

```bash
# 搜索内容
python3 ~/.openclaw/workspace/.agents/skills/minimax-tools/scripts/web_search.py "今天的热点新闻"

# 搜索技术问题
python3 ~/.openclaw/workspace/.agents/skills/minimax-tools/scripts/web_search.py "Python 如何处理 JSON"
```

---

## 迁移到其他设备

需要复制到新设备的内容：

1. **脚本目录**：
   ```
   ~/.openclaw/workspace/.agents/skills/minimax-tools/scripts/
   ```

2. **配置文件**：
   - 复制 `~/.openclaw/config/minimax.json`，或
   - 在新设备设置环境变量 `MINIMAX_API_KEY`

3. **依赖安装**（在新设备上执行）：
   ```bash
   # 安装 uv（如需要）
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # 安装 MCP 服务器
   uvx install minimax-coding-plan-mcp
   ```

---

## 脚本说明

### understand_image.py

- 优先从环境变量 `MINIMAX_API_KEY` 读取 API Key
- 如未设置则从 `~/.openclaw/config/minimax.json` 读取
- 支持本地图片路径和 URL

### web_search.py

- 优先从环境变量 `MINIMAX_API_KEY` 读取 API Key
- 如未设置则从 `~/.openclaw/config/minimax.json` 读取
- 返回格式化的搜索结果

---

## 常见问题

**Q: 提示 "uvx: command not found"**
> 需要安装 uv，参见步骤 1

**Q: 提示 "API Key 未配置"**
> 需要配置 MiniMax API Key，参见步骤 3

**Q: MCP 服务器连接失败**
> 检查网络连接，或尝试重新安装：`uvx install minimax-coding-plan-mcp`
