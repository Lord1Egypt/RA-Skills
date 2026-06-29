---
name: china-api-gateway
version: 1.5.0
description: |
  想用国内免费/低价大模型，结果每家API格式都不一样？一个网关聚合MiMo/DeepSeek/Qwen/GLM等主流模型，OpenAI兼容接口直接替换，自动负载均衡+故障切换。省钱又省心，薅遍国内AI免费额度。
  触发词：
  - 基础词：国内免费AI、免费API、薅羊毛AI、换模型、切换AI、负载均衡
  - 平台词：MiMo API、DeepSeek API、Qwen API、GLM API、阿里百炼、智谱AI、火山引擎
  - 配置词：怎么调用大模型、API怎么用、接口配置、API Key获取
  - 网关词：OpenAI兼容、API网关、聚合AI、免费调用额度、模型切换
  排除：海外模型直连、模型训练/Fine-tuning、私有化部署咨询
---

# 中国AI API统一网关

## 触发条件判定

### ✅ 触发场景
| 场景 | 触发词示例 |
|------|-----------|
| 找免费API | "有什么免费AI API"、"国内免费模型"、"薅羊毛" |
| 平台咨询 | "MiMo怎么用"、"DeepSeek API"、"阿里百炼申请" |
| 配置问题 | "API怎么配置"、"接口怎么调"、"OpenAI兼容" |
| 切换模型 | "换个AI"、"切换模型"、"负载均衡" |
| 网关搭建 | "API网关"、"聚合接口"、"统一入口" |

### ❌ 排除场景
| 场景 | 排除原因 | 建议替代 |
|------|---------|---------|
| 海外模型直连 | 只支持国内平台 | 使用OpenRouter |
| 模型训练/微调 | 不支持Fine-tuning | 专业ML平台 |
| 私有化部署 | 不涉及API调用 | 技术方案技能 |
| 模型量化压缩 | 不涉及API调用 | 模型优化工具 |

## 核心流程 (5步)

### Step 1: 需求分析
```
必问项：
□ 用途类型：chat（对话）/ embedding（向量化）/ image（绘图）
□ 预算范围：free（免费）/ low（低成本 <¥10/月）/ any（不限）
□ 调用频率：low（<100次/天）/ medium（100-1000）/ high（>1000）
□ 中文需求：必须 / 最好 / 无所谓
□ 特殊能力：推理强 / 代码强 / 速度快 / 稳定

可选补充：
□ 是否需要多模型聚合
□ 是否需要故障切换
□ 部署环境：本地/VPS/云函数
```

### Step 2: 推荐方案
**推荐决策树**：
```
用途=chat AND 预算=free AND 中文=必须?
  → 是 → MiMo > DeepSeek > 智谱GLM

用途=chat AND 推理=必须?
  → 是 → GLM-5.2（1M上下文+开源最强编码） > DeepSeek-Coder

用途=code AND 长上下文=必须?
  → 是 → GLM-5.2（1M稳定上下文，Coding Arena开源第1）

用途=embedding AND 预算=free?
  → DeepSeek-embedding / 智谱embedding

用途=image AND 预算=free?
  → 智谱 CogView / 阿里通义万相

需要多模型聚合?
  → 硅基流动 / OpenRouter
```

### Step 3: 获取指引
```
每个平台的获取步骤：
1. 注册账号（手机号/邮箱）
2. 完成实名认证（如需）
3. 进入控制台/API密钥页面
4. 创建/复制API Key
5. 验证可用性

注意：部分平台需充值才有API权限
```

### Step 4: 配置模板
```python
# OpenAI兼容方式
from openai import OpenAI

client = OpenAI(
    base_url="平台API地址/v1",
    api_key="your-api-key"
)

response = client.chat.completions.create(
    model="模型名",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

### Step 5: 故障排查
```
常见问题 → 排查步骤 → 解决方案

401 Unauthorized
  → 检查API Key是否正确
  → 检查Key是否过期/被禁用
  → 确认API地址是否正确

429 Rate Limit
  → 降低请求频率
  → 开启指数退避重试
  → 申请更高配额

Connection Error
  → 检查网络连接
  → 确认API地址可访问
  → 尝试更换节点/代理
```

## 国内平台详细对比

### 完全免费平台

| 平台 | 模型 | 免费额度 | 限速 | 中文优化 | 推理能力 | 推荐度 |
|------|------|---------|------|---------|---------|--------|
| **小米MiMo** | mimo-v2.5 | 无限（当前） | 较高 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🥇 |
| **DeepSeek** | deepseek-chat | 500万tokens | 标准 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🥈 |
| **阿里百炼** | qwen-turbo | 100万tokens/月 | 标准 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🥉 |
| **智谱AI** | glm-4-flash | 250万tokens | 标准 | ⭐⭐⭐⭐ | ⭐⭐⭐ |  |
| **零一万物** | yi-lightning | 免费额度 | 限制 | ⭐⭐⭐ | ⭐⭐⭐⭐ |  |
| **商汤SenseNova** | DS-V4-Flash | 500次/5h | 标准 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 双协议兼容 |
| **智谱GLM-5.2** | glm-5.2 | MIT开源/API低价 | 标准 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 744B MoE,1M上下文,Coding Arena第2 |

### 低成本平台

| 平台 | 模型 | 价格 | 免费额度 | 特点 |
|------|------|------|---------|------|
| 硅基流动 | 多模型聚合 | ¥0/部分免费 | 有 | 聚合Qwen/GLM/Llama |
| 火山引擎 | doubao | ¥0.004/千tokens | 无 | 字节跳动，稳定 |
| MiniMax | abab6.5s | ¥0.01/千tokens | 无 | 长文本支持好 |
| 天工AI | skywork | ¥0.002/千tokens | 有 | 昆仑万维 |

### 专业模型平台

| 需求 | 推荐平台 | 推荐模型 | 说明 |
|------|---------|---------|------|
| 代码生成 | 智谱GLM-5.2 | glm-5.2 | Coding Arena开源第1（MIT开源，1M上下文，成本GPT-5.5的1/6）|
| 代码生成(备选) | DeepSeek | deepseek-coder | 代码能力强，免费额度充足 |
| 数学推理 | DeepSeek | deepseek-math | 数学专项 |
| 长文本 | 智谱GLM-5.2 | glm-5.2 | 1M上下文稳定（开源最长可用）|
| 长文本(备选) | Kimi/MiniMax | moonshot/abab | 128K+上下文 |
| 图像生成 | 智谱/阿里 | cogview/qwen-vl | 中文优化好 |
| Embedding | DeepSeek | deepseek-embed | 向量化质量好 |

## API调用示例

### 基础对话（curl）

```bash
# 小米MiMo
curl https://api.xiaomimimo.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MIMO_API_KEY" \
  -d '{
    "model": "mimo-v2.5",
    "messages": [{"role": "user", "content": "你好"}],
    "temperature": 0.7,
    "max_tokens": 1000
  }'

# DeepSeek
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}]
  }'

# 阿里百炼
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ALI_API_KEY" \
  -d '{
    "model": "qwen-turbo",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### Python SDK

```python
from openai import OpenAI

# 小米MiMo
client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key="sk-xxxxx"
)

# DeepSeek
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key="sk-xxxxx"
)

# 阿里百炼
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-xxxxx"
)

response = client.chat.completions.create(
    model="auto",  # 或指定具体模型
    messages=[
        {"role": "system", "content": "你是AI助手"},
        {"role": "user", "content": "你好"}
    ],
    temperature=0.7,
    max_tokens=1000
)
print(response.choices[0].message.content)
```

### 流式输出

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key="sk-xxxxx"
)

stream = client.chat.completions.create(
    model="mimo-v2.5",
    messages=[{"role": "user", "content": "讲个笑话"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 网关配置示例

### 简单负载均衡

```yaml
# gateway.yaml
providers:
  - name: mimo
    base_url: https://api.xiaomimimo.com/v1
    api_key: ${MIMO_API_KEY}
    models: [mimo-v2.5]
    priority: 1
    
  - name: deepseek
    base_url: https://api.deepseek.com/v1
    api_key: ${DEEPSEEK_API_KEY}
    models: [deepseek-chat]
    priority: 2

routing:
  strategy: priority  # priority / round_robin / random
  fallback: true
  timeout: 30
  retry: 2
```

### Python实现简单网关

```python
import os
from openai import OpenAI

PROVIDERS = {
    "mimo": {
        "base_url": "https://api.xiaomimimo.com/v1",
        "api_key": os.getenv("MIMO_API_KEY"),
        "models": ["mimo-v2.5"]
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "models": ["deepseek-chat"]
    }
}

def chat(message, prefer="mimo"):
    """简单负载均衡"""
    for provider_name in [prefer] + list(PROVIDERS.keys()):
        if provider_name == prefer:
            continue
        provider = PROVIDERS.get(provider_name)
        if not provider["api_key"]:
            continue
            
        try:
            client = OpenAI(
                base_url=provider["base_url"],
                api_key=provider["api_key"]
            )
            response = client.chat.completions.create(
                model=provider["models"][0],
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"{provider_name} failed: {e}")
            continue
    
    return "All providers failed"
```

## 边界约束

### 输入校验
| 校验项 | 要求 | 不符处理 |
|--------|------|---------|
| 用途 | chat/embedding/image | 询问具体需求 |
| 预算 | free/low/any | 推荐免费方案 |
| API Key | 有效格式 | 检查Key格式 |
| 网络 | 可访问目标API | 提供网络诊断 |

### 平台限制清单

| 平台 | 限制说明 |
|------|---------|
| MiMo | 免费额度可能调整，注意用量 |
| DeepSeek | 免费额度用完需充值 |
| 阿里百炼 | 需要阿里云账号，实名认证 |
| 智谱AI | 部分模型需充值 |
| 硅基流动 | 免费模型有QPS限制 |

### 不支持场景
1. ❌ 海外模型直连（OpenAI/Claude/Gemini等）
2. ❌ 模型训练/Fine-tuning/微调
3. ❌ 私有化部署/模型下载
4. ❌ 模型量化/压缩/导出

## 完整示例

### 示例1：日常对话Agent
```
用户：我想找个免费的中文AI API，用于我的AI助手

【需求分析】
• 用途：chat（对话）
• 预算：free
• 特点：中文优化、高频调用

【推荐方案】

🥇 小米MiMo（首选）
• API：https://api.xiaomimimo.com/v1/chat/completions
• 模型：mimo-v2.5
• 额度：当前免费无限
• 中文：⭐⭐⭐⭐⭐
• 适合：高频调用、中文对话

🥈 DeepSeek（备选）
• API：https://api.deepseek.com/v1/chat/completions
• 模型：deepseek-chat
• 额度：注册送500万tokens
• 推理：⭐⭐⭐⭐⭐
• 适合：复杂推理、代码

【快速开始】
1. 注册：https://platform.xiaomimimo.com
2. 获取API Key
3. 使用上方Python代码调用
```

### 示例2：代码生成助手
```
用户：需要调用一个代码能力强的免费API

【推荐方案】

🥇 DeepSeek-Coder（代码最强）
• API：https://api.deepseek.com/v1/chat/completions
• 模型：deepseek-coder
• 额度：500万tokens免费
• 代码：⭐⭐⭐⭐⭐

【调用示例】
from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key="sk-xxxxx"
)

response = client.chat.completions.create(
    model="deepseek-coder",
    messages=[{
        "role": "user", 
        "content": "写一个Python快速排序"
    }]
)
print(response.choices[0].message.content)
```

### 示例3：聚合网关搭建
```
用户：我想搭建一个API网关，自动切换不同AI

【推荐架构】

方案A：硅基流动（开箱即用）
• 聚合：Qwen/GLM/Llama等
• 部分模型免费
• 无需自己运维

方案B：自建网关（灵活控制）
• 使用One API / New API开源项目
• 配置多个Provider
• 支持负载均衡/故障切换

【New API部署】
# Docker部署
docker run -d \
  --name new-api \
  -p 3000:3000 \
  -v ./data:/data \
  calm业务的/new-api

# 然后在Web界面配置各平台渠道
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 401错误 | Key无效/过期 | 检查API Key，重新获取 |
| 429错误 | 请求超限 | 降频、重试、使用备用平台 |
| 响应慢 | 网络/负载高 | 换节点、异步调用 |
| 额度用完 | 免费额度耗尽 | 充值、换平台、申请新账号 |
| 间歇失败 | 服务不稳定 | 添加重试逻辑、多平台备份 |

## 参考资源

平台注册地址、详细API文档见 references/platforms.md
