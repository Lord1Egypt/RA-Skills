# AI 服务配置指南

## 快速开始

### 1. SiliconFlow（推荐，免费额度）

1. 注册账号：https://siliconflow.cn
2. 获取 API Key
3. 设置环境变量：

```bash
# Linux/Mac
export AI_PROVIDER=siliconflow
export AI_API_KEY=your_api_key_here

# Windows
set AI_PROVIDER=siliconflow
set AI_API_KEY=your_api_key_here
```

### 2. OpenAI GPT

```bash
export AI_PROVIDER=openai
export AI_API_KEY=sk-your_key_here
export AI_MODEL=gpt-3.5-turbo
```

### 3. 智谱 GLM（国产）

```bash
export AI_PROVIDER=zhipu
export AI_API_KEY=your_zhipu_key_here
export AI_MODEL=glm-4
```

### 4. 仅使用规则响应（无需API）

```bash
export AI_PROVIDER=silence
```

---

## 支持的提供商

| 提供商 | 模型 | 免费额度 | 特点 |
|-------|------|---------|------|
| **SiliconFlow** | Qwen, GLM 等 | 100万token/月 | 性价比高，中文支持好 |
| **OpenAI** | GPT-3.5, GPT-4 | $5免费额度 | 能力最强 |
| **智谱** | GLM-4 | 注册送token | 国产，免费额度多 |
| **Silence** | 无 | 无限 | 仅规则响应 |

---

## 环境变量配置

在启动后端前设置：

```bash
cd backend

# 方式1: 直接设置
export AI_PROVIDER=siliconflow
export AI_API_KEY=your_key_here

# 方式2: 创建 .env 文件（推荐）
echo "AI_PROVIDER=siliconflow" > .env
echo "AI_API_KEY=your_key_here" >> .env

# 方式3: 启动时指定
AI_PROVIDER=siliconflow AI_API_KEY=your_key python main.py
```

---

## 代码中配置

也可以在代码中直接修改配置：

```python
# ai_config.py
class AIConfig:
    def __init__(self):
        self.provider = "siliconflow"  # 修改这里
        self.api_key = "your_key_here"  # 修改这里
        self.model = "Qwen/Qwen2.5-7B-Instruct"
```

---

## 验证配置

启动后端后，查看日志：

```
AI Provider: siliconflow
API Key configured: True
```

或者发送一条消息测试：

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

---

## 常见问题

### Q: API 调用失败
A: 检查：
1. API Key 是否正确
2. 网络是否能访问
3. 是否超出配额

### Q: 响应很慢
A: 尝试：
1. 使用 SiliconFlow（国内节点）
2. 减少对话历史长度
3. 使用更小的模型

### Q: 如何切换提供商？
A: 修改 `AI_PROVIDER` 环境变量，重启服务即可。
