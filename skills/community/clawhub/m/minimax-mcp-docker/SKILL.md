# MiniMax MCP Skill

**这是一个自动化技能 - 支持图片理解 + 联网搜索两大功能**

## 简介

这个 Skill 集成了 **图片理解** 和 **联网搜索** 两大功能：
- 🖼️ **图片理解** - 用户发送图片，自动 OCR 识别、图像内容分析
- 🔍 **联网搜索** - 用户要求搜索时，自动搜索互联网信息

## 用户使用方式

**用户只需要：**
1. 安装 skill（一次性）
2. 安装 MCP 包：`npm install -g @ameno/pi-minimax-mcp`
3. 配置 API Key（见下方）
4. **发送图片或搜索请求给我** → 我自动调用 MCP 处理 → 返回结果

**用户无需任何其他操作** - 图片理解和联网搜索我都自动搞定！

## API Key 配置（安全）

API Key 存储在 `~/.openclaw/credentials/minimax.json`，**不在代码中**。

### 配置步骤

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/credentials

# 2. 保存 API Key（替换为你的 key）
echo '{"api_key": "sk-cp-xxx", "api_host": "https://api.minimaxi.com"}' > ~/.openclaw/credentials/minimax.json

# 3. 设置权限
chmod 600 ~/.openclaw/credentials/minimax.json
```

## 我是如何自动调用的

当用户发送图片时，我会：

1. **读取 API Key** - 从 `~/.openclaw/credentials/minimax.json` 自动读取
2. **构建命令** - 自动组装 exec 命令
3. **执行 MCP** - 调用 `node .../pi-minimax-mcp.js understand 图片路径`
4. **返回结果** - 把识别结果发给用户

用户完全无感，就像正常聊天一样！

## 示例对话

**图片理解：**
**用户**：发一张图片给我看看
*(用户发送图片)*
**我**：(自动调用 MCP understand) → 返回识别结果

**联网搜索：**
**用户**：搜索一下 OpenClaw 是什么
**我**：(自动调用 MCP search) → 返回搜索结果

**用户**：帮我搜一下今天的热搜
**我**：(自动调用 MCP search) → 返回搜索结果

## 内部实现（供 AI 参考）

```python
# 自动调用流程
def auto_understand_image(image_path):
    # 1. 读取 credentials
    api_key = read_credentials()  # 从 ~/.openclaw/credentials/minimax.json
    
    # 2. 设置环境
    env = {
        'MINIMAX_API_KEY': api_key,
        'MINIMAX_API_HOST': 'https://api.minimaxi.com'
    }
    
    # 3. 执行 MCP
    cmd = ['node', 'node_modules/@ameno/pi-minimax-mcp/bin/pi-minimax-mcp.js', 
           'understand', image_path]
    
    result = subprocess.run(cmd, env=env, capture_output=True, timeout=120)
    
    # 4. 返回结果
    return result.stdout
```

## 注意事项

- ⚠️ MCP 包必须先安装：`npm install -g @ameno/pi-minimax-mcp`
- ⏱️ 图片理解可能需要 30-60 秒
- 🔐 API Key 永远不会出现在代码中

## ⚠️ API Key 缺失处理（重要）

**如果 `~/.openclaw/credentials/minimax.json` 不存在或无法读取 API Key：**

1. **自动提醒用户**：告诉用户需要配置 MiniMax API Key
2. **引导用户获取 Key**：访问 https://platform.minimaxi.com/ 注册获取
3. **让用户提供 Key 后**：帮用户创建配置文件到正确位置

**示例对话：**
```
**我**：未找到 MiniMax API Key 配置，请提供您的 API Key 以便使用图片理解功能。
**用户**：sk-xxxxxxxxxxxxx
**我**：好的，正在帮您配置 API Key...
（自动写入配置文件）
配置完成！以后发图片给我就能自动识别啦~
```

**重要**：用户只需提供一次 API Key，之后都会从本地配置文件自动读取，无需重复提供。
