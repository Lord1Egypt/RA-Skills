# MiniMax Tools

MiniMax Token Plan 的网络搜索和图片理解工具封装。

## 功能

- **web_search**: 网络搜索，返回搜索结果和相关搜索建议
- **understand_image**: 图片理解，支持 HTTP URL 和本地文件

## 安装

```bash
pip install -r requirements.txt
```

## 配置

### API Key 配置

**方式 1：环境变量（推荐）**

```bash
export MINIMAX_API_KEY="your-api-key"
```

**方式 2：凭据文件**

创建 `~/.openclaw/credentials/minimax_mcp.env`:

```
MINIMAX_API_KEY=your-api-key
```

## 使用方法

### Python API

```python
from minimax_tools import web_search, understand_image

# 网络搜索
result = web_search("Python 教程")
print(result['results'])

# 图片理解
result = understand_image(
    prompt="这张图片里有什么？",
    image_url="https://example.com/image.jpg"
)
print(result)
```

### 命令行

```bash
# 网络搜索
python -m minimax_tools.web_search "搜索词"

# 图片理解
python -m minimax_tools.understand_image "描述这张图" "https://example.com/image.jpg"
```

## 安全说明

- ✅ API Key 从环境变量或凭据文件读取，绝不硬编码
- ✅ 输出时对 API Key 进行脱敏处理
- ✅ 凭据文件权限检查（600）

## 项目结构

```
minimax-tools/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py          # 配置加载
│   ├── web_search.py      # 网络搜索
│   └── understand_image.py # 图片理解
└── tests/
    └── test_api.py        # API 测试
```

## 依赖说明

此工具依赖于 `mcporter` 来调用 MiniMax Token Plan MCP 服务。

安装 mcporter:
```bash
npm install -g mcporter
```

配置 MiniMax MCP:
```bash
mcporter config add MiniMax \
    --command uvx \
    --args "minimax-coding-plan-mcp -y" \
    --env MINIMAX_API_KEY=$MINIMAX_API_KEY \
    --env MINIMAX_API_HOST=https://api.minimaxi.com \
    --scope home
```

## 故障排除

### MCP 服务离线

如果遇到 "MiniMax MCP 服务离线" 错误：

1. 检查 mcporter 配置：
   ```bash
   mcporter config list
   mcporter list
   ```

2. 重启 mcporter daemon：
   ```bash
   mcporter daemon restart
   ```

3. 验证 API Key：
   ```bash
   echo $MINIMAX_API_KEY
   ```

## License

MIT
