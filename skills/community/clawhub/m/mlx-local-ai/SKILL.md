# MLX Local AI 技能

一键部署本地 AI 服务，支持 Apple Silicon (M1/M2/M3/M4)。

## 功能

- 🤖 **本地 LLM 服务**：Qwen3.5-4B-OptiQ-4bit (通过 MLX-LM)
- 📊 **Embedding 服务**：bge-base-zh-v1.5 (中文向量模型)
- 🔄 **OpenClaw Gateway**：统一 API 网关
- 🎯 **一键安装/启动/停止**

## 系统要求

- macOS 14.0+ (Sonoma 或更高)
- Apple Silicon (M1/M2/M3/M4)
- Python 3.10+
- 8GB+ 内存

## 快速开始

### 安装

```bash
./install.sh
```

### 启动服务

```bash
./start_ai.sh start
```

### 检查状态

```bash
./start_ai.sh status
```

### 停止服务

```bash
./start_ai.sh stop
```

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Chat API | 8080 | OpenAI 兼容 API |
| Embedding API | 8081 | 向量嵌入 API |
| OpenClaw Gateway | 18789 | 管理界面 |

## API 使用

### Chat API

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Qwen3.5-4B-OptiQ-4bit",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'
```

### Embedding API

```bash
curl http://localhost:8081/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["你好", "世界"]}'
```

## 文件结构

```
mlx-local-ai/
├── SKILL.md           # 本文件
├── install.sh         # 安装脚本
├── start_ai.sh        # 启动脚本
├── uninstall.sh       # 卸载脚本
├── config/            # 配置文件
│   ├── openclaw.json  # OpenClaw 配置
│   └── env.example    # 环境变量示例
└── scripts/           # 工具脚本
    ├── check_deps.py  # 依赖检查
    └── test_api.py    # API 测试
```

## 配置

### 环境变量

复制 `config/env.example` 到 `~/.zshrc`：

```bash
cp config/env.example ~/.zshrc.local
echo 'source ~/.zshrc.local' >> ~/.zshrc
```

### 模型配置

默认使用 `mlx-community/Qwen3.5-4B-OptiQ-4bit`，可在 `start_ai.sh` 中修改。

## 故障排查

### 服务无法启动

```bash
# 检查依赖
python3 scripts/check_deps.py

# 查看日志
./start_ai.sh logs
```

### 模型加载失败

```bash
# 手动下载模型
source ~/mlx-env/bin/activate
HF_ENDPOINT=https://hf-mirror.com python3 -c "from mlx_lm import load; load('mlx-community/Qwen3.5-4B-OptiQ-4bit')"
```

## 更新

```bash
./install.sh --update
```

## 卸载

```bash
./uninstall.sh
```

## 许可证

MIT License
