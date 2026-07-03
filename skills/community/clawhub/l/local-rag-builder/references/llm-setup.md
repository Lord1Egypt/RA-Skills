# 外部 LLM 服务接入参考

> 本文件适用于 **独立模式**（`rag_standalone.py`）。技能模式（`rag_skill.py`）不需要 LLM。

## 配置方式

所有 LLM 连接参数通过 `data/config/rag_config.json` 的 `llm` section 控制：

```json
{
  "llm": {
    "base_url": "http://localhost:1234/v1",
    "api_key": "not-needed",
    "temperature": 0.1,
    "max_tokens": 512,
    "model_name": ""
  }
}
```

更新方式：
- **Web 面板**：`python scripts/rag_web_ui.py` → LLM 配置卡片
- **CLI**：`/config set llm.base_url http://localhost:11434/v1`

---

## 方案一：LM Studio（图形界面，适合新手）

| 项目 | 说明 |
|:----|:-----|
| 下载 | https://lmstudio.ai |
| 模型搜索 | 左侧 Search → 搜索 Qwen2.5 / DeepSeek-R1 / Gemma 等 GGUF 格式 |
| 模型下载 | 选择一个量化版本（如 Q4_K_M），点击 Download |
| 启动服务 | Local Inference Server → 选择模型 → Start Server |
| API 地址 | `http://localhost:1234/v1` |
| 验证 | 浏览器访问 `http://localhost:1234/v1/models` 应返回模型列表 |
| Python 配置 | `base_url = "http://localhost:1234/v1"` |

**典型流程：**
```
1. 下载 LM Studio 并安装
2. 搜索 qwen2.5-7b-instruct-gguf，选择 Q4_K_M 量化版下载
3. 切换到 Local Inference Server 标签页
4. 下拉框选择刚下载的模型
5. 点击 Start Server
6. 保持 LM Studio 运行，回到终端
7. python scripts/rag_standalone.py    ← 启动问答
```

---

## 方案二：Ollama（命令行，适合开发者）

| 项目 | 说明 |
|:----|:-----|
| 下载 | https://ollama.com |
| 模型市场 | https://ollama.com/library |
| 常用模型 | `qwen2.5:7b`（通义千问）、`deepseek-r1:7b`、`gemma3:7b`、`llama3.1:8b` |
| 启动服务 | `ollama serve`（自动后台运行） |
| API 地址 | `http://localhost:11434/v1` |
| 验证 | `curl http://localhost:11434/v1/models` |
| Python 配置 | `base_url = "http://localhost:11434/v1"` |

**典型流程：**
```bash
# 安装 Ollama 后
ollama pull qwen2.5:7b          # 拉取模型（首次需下载）
ollama serve                    # 启动 API 服务（后台常驻）

# 另一个终端
python scripts/rag_standalone.py
```

**多模型管理：**
```bash
ollama list                     # 列出已下载的模型
ollama pull deepseek-r1:7b      # 拉取另一个模型
ollama run qwen2.5:7b           # 直接交互运行
```

---

## 方案三：vLLM（生产环境高性能推理）

| 项目 | 说明 |
|:----|:-----|
| 安装 | `pip install vllm` |
| GPU 要求 | NVIDIA GPU，建议 ≥8GB 显存 |
| 常用模型 | `Qwen/Qwen2.5-7B-Instruct`、`deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` |
| API 地址 | `http://localhost:8000/v1`（可自定义端口） |
| Python 配置 | `base_url = "http://localhost:8000/v1"` |

**典型流程：**
```bash
pip install vllm

# 单卡启动
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000

# 另一个终端
python scripts/rag_standalone.py
```

**vLLM 参数调优：**
```bash
# 指定 GPU 显存使用比例
--gpu-memory-utilization 0.85

# 使用 AWQ 量化模型（降低显存需求）
--quantization awq

# 最大并发数
--max-num-seqs 32
```

---

## 参数参考

| 参数 | LM Studio 默认 | Ollama 默认 | vLLM 默认 |
|:----|:--------------:|:-----------:|:---------:|
| `base_url` | http://localhost:1234/v1 | http://localhost:11434/v1 | http://localhost:8000/v1 |
| `api_key` | not-needed | not-needed | not-needed |
| `temperature` | 0.1 | 0.1 | 0.1 |
| `max_tokens` | 512 | 512 | 512 |
| 推荐模型 | Qwen2.5-7B-GGUF | qwen2.5:7b | Qwen2.5-7B-Instruct |

---

## 故障排查

| 现象 | 原因 | 解决 |
|:----|:-----|:-----|
| LLM 连接失败 | 服务未启动 | 启动 LM Studio / Ollama / vLLM 服务 |
| 连接失败 | 端口不对 | 确认实际端口，更新 base_url |
| 连接失败 | 地址不对 | 本地服务用 localhost，远程用 IP |
| 回答乱码 | 模型不支持中文 | 换成 Qwen / DeepSeek 等中文模型 |
| 回答太短 | max_tokens 太小 | 调大 max_tokens（如 2048） |
| 显存不足 | 模型太大 | 换更小的量化版或换 3B 模型 |
