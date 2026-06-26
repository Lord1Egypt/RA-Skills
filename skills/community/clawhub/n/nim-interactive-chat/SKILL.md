# NIM Interactive Chat

为 NVIDIA NIM 格式大模型一键创建交互式对话启动脚本，自动等待服务就绪，一键启动直接进入对话，使用体验和本地聊天程序一样流畅。

## 功能特点

- ✅ 一键创建全套脚本：启动 + 停止 + 交互式对话客户端
- ✅ 自动删除旧容器避免冲突
- ✅ 自动等待健康检查通过，就绪后自动打开对话
- ✅ OpenAI 兼容 API，支持流式输出
- ✅ 保持对话上下文
- ✅ 输入 `exit` 退出，容器继续后台运行
- ✅ 支持自定义 GPU 显存利用率

## 使用方法

```bash
create-nim-interactive <image-name> <container-name> <port> <model-name> [gpu-memory-utilization]
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `image-name` | ✅ | Docker 镜像名称 |
| `container-name` | ✅ | 容器名称 |
| `port` | ✅  | 本地端口映射 |
| `model-name` | ✅ | 模型名称（API 用）|
| `gpu-memory-utilization` | ⭕ | GPU 显存利用率，默认 `0.9` |

## 示例

为 Qwen3.5-4B 创建：

```bash
create-nim-interactive \
  tgcr.turing-agi.com/public/qwen/qwen3.5-4b-spark-nim:latest \
  qwen3.5-4b-nim \
  18000 \
  Qwen/Qwen3.5-4B \
  0.88
```

创建完成后：

```bash
# 一键启动（自动等待服务就绪 + 进入交互式对话）
./start-qwen3.5-4b-nim.sh

# 一键停止容器
./stop-qwen3.5-4b-nim.sh
```

## 生成文件

- `~/start-<container-name>.sh` - 一键启动脚本
- `~/stop-<container-name>.sh` - 一键停止脚本
- `~/<container-name>-chat.py` - Python 交互式对话客户端（OpenAI 兼容）

##  requirements

- Docker
- Python 3
- `openai` Python package

## 适用场景

- 本地部署 NVIDIA NIM 格式模型（NGC / TGC 等）
- 想要一键启动直接对话的便捷体验
- 和 Gemma 一样友好的使用方式
