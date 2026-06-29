# 中国AI平台注册与API获取指南

## 平台注册地址汇总

| 平台 | 注册地址 | 实名要求 | 充值要求 |
|------|---------|---------|---------|
| 小米MiMo | https://platform.xiaomimimo.com | 手机号 | 无（当前免费） |
| DeepSeek | https://platform.deepseek.com | 邮箱/手机 | 无（注册送额度） |
| 阿里百炼 | https://bailian.congsole.aliyun.com | 阿里云账号+实名 | 无（新用户送额度） |
| 智谱AI | https://open.bigmodel.cn | 手机号 | 无（注册送额度） |
| 零一万物 | https://platform.lingyiwanwu.com | 手机号 | 无（有免费额度） |
| 商汤SenseNova | https://www.sensenova.cn | 手机号 | 无（公测免费） |
| 硅基流动 | https://cloud.siliconflow.cn | 手机号 | 无（部分免费） |
| 火山引擎 | https://console.volcengine.com/ark | 字节账号+实名 | 需充值 |
| MiniMax | https://platform.minimaxi.com | 手机号 | 需充值 |
| 天工AI | https://model-platform.tiangong.cn | 手机号 | 部分免费 |
| Kimi | https://platform.moonshot.cn | 手机号 | 需充值 |

## 完全免费平台详解

### 1. 小米 MiMo ⭐推荐

**平台信息**
```
官网：https://platform.xiaomimimo.com
API地址：https://api.xiaomimimo.com/v1
模型：mimo-v2.5（主力）、mimo-v2.5-pro（更强）
额度：当前免费无限（注意：可能随时调整）
中文优化：⭐⭐⭐⭐⭐（专为中文优化）
```

**注册步骤**
1. 访问 https://platform.xiaomimimo.com
2. 使用手机号注册/登录
3. 进入「API密钥」页面
4. 创建新密钥，复制保存

**API调用**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key="sk-xxxxx"  # 你的API Key
)

response = client.chat.completions.create(
    model="mimo-v2.5",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

**适用场景**
- 日常对话、闲聊
- 高频AI助手调用
- 中文内容创作
- 需要快速响应的场景

**注意事项**
- ⚠️ 免费额度可能调整，建议关注官方公告
- ⚠️ 高频调用时注意用量监控
- ⚠️ 建议同时配置备用平台

---

### 2. DeepSeek ⭐代码推理最强

**平台信息**
```
官网：https://platform.deepseek.com
API地址：https://api.deepseek.com/v1
主力模型：
  - deepseek-chat：通用对话
  - deepseek-coder：代码专用
  - deepseek-math：数学专用
  - deepseek-reasoner：深度推理（思考模型）
额度：注册送500万tokens
中文优化：⭐⭐⭐⭐
```

**注册步骤**
1. 访问 https://platform.deepseek.com
2. 点击「API开放平台」
3. 注册并登录
4. 进入控制台 → API Keys → 创建
5. 复制Key（格式：sk-xxxxx）

**模型选择指南**
| 模型 | 适用场景 | 价格 |
|------|---------|------|
| deepseek-chat | 通用对话、日常任务 | ¥1/百万tokens |
| deepseek-coder | 代码生成/调试 | ¥2/百万tokens |
| deepseek-math | 数学问题、推理 | ¥8/百万tokens |
| deepseek-reasoner | 复杂问题、深度思考 | ¥60/百万tokens |

**免费额度**
```
注册即送：500万tokens
额度用完需充值
```

**API调用**
```python
# 通用对话
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写个快速排序"}]
)

# 代码专用
response = client.chat.completions.create(
    model="deepseek-coder",
    messages=[{"role": "user", "content": "用Python写个爬虫"}]
)

# 深度推理（思考模型）
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[{"role": "user", "content": "分析这道数学题..."}]
)
```

---

### 3. 阿里百炼

**平台信息**
```
官网：https://bailian.console.aliyun.com
API地址：https://dashscope.aliyuncs.com/compatible-mode/v1
模型：
  - qwen-turbo：快速响应（免费100万tokens/月）
  - qwen-plus：更强能力
  - qwen-max：最强能力
额度：新用户送100万tokens
中文优化：⭐⭐⭐⭐⭐
```

**注册步骤**
1. 需要阿里云账号
2. 访问 https://bailian.console.aliyun.com
3. 开通百炼服务
4. 创建API Key（RAM访问密钥）

**API调用**
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")  # 阿里云AccessKey
)

response = client.chat.completions.create(
    model="qwen-turbo",
    messages=[{"role": "user", "content": "你好"}]
)
```

---

### 4. 智谱AI

**平台信息**
```
官网：https://open.bigmodel.cn
API地址：https://open.bigmodel.cn/api/paas/v4
模型：
  - glm-4-flash：免费额度（推荐）
  - glm-4：标准能力
  - glm-4-plus：更强能力
  - glm-4v：视觉理解
额度：新用户送250万tokens
中文优化：⭐⭐⭐⭐
```

**注册步骤**
1. 访问 https://open.bigmodel.cn
2. 手机号注册登录
3. 个人中心 → API密钥 → 创建
4. 复制API Key（格式：xxxxx）

**API调用**
```python
client = OpenAI(
    api_key="your-api-key",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": "你好"}]
)
```

---

### 5. 零一万物

**平台信息**
```
官网：https://platform.lingyiwanwu.com
API地址：https://api.lingyiwanwu.com/v1
模型：
  - yi-lightning：快速模型（免费额度）
  - yi-large：更强模型
额度：有免费额度
英文优化：⭐⭐⭐⭐⭐
```

**特点**
- 对英文场景优化更好
- Yi模型性能不错
- 国内访问速度快

---

## 低成本平台

### 6. 商汤 SenseNova（2026-06-16新增，公测免费）

**平台信息**
```
官网：https://www.sensenova.cn
API地址：https://api.sensenova.cn/v1
模型：DeepSeek V4 Flash / SenseNova 6.7 Flash-Lite / SenseNova U1 Fast
额度：每5小时刷新（DS-V4-Flash 500次, SN-6.7 1500次, SN-U1 1500次）
上下文：256K
协议兼容：OpenAI API + Anthropic Claude 双协议
注册：https://www.sensenova.cn → 手机号验证 → 控制台 → Token Plan → 领取免费Token
```

**核心优势**
- DeepSeek V4 Flash通过商汤中转，百万字长文档+140 token/s推理速度
- 双协议兼容：一套代码切换base_url即可用，无需重写业务逻辑
- 三个模型额度独立刷新，日均可调7200次DS-V4-Flash
- 公测永久免费，无需充值、无需绑卡

**API调用示例**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.sensenova.cn/v1",
    api_key="your-sensenova-api-key"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",  # 或 "sensennova-6.7-flash-lite"
    messages=[{"role": "user", "content": "你好"}]
)
```

**注意事项**
- 额度每5小时自动重置，非一次性总量
- 公测阶段免费，后续可能调整策略
- 适合个人开发者/学生/零成本验证场景

### 7. 硅基流动 SiliconFlow

**平台信息**
```
官网：https://cloud.siliconflow.cn
API地址：https://api.siliconflow.cn/v1
特点：聚合多模型平台
免费模型：Qwen/Llama/GLM等部分模型
```

**免费模型列表**
| 模型 | 类型 | 限制 |
|------|------|------|
| Qwen/Qwen2.5-7B-Instruct | 对话 | 有QPS限制 |
| THUDM/glm-4-9b-chat | 对话 | 有QPS限制 |
| meta-llama/Llama-3-8B-Instruct | 对话 | 有QPS限制 |

**API调用**
```python
client = OpenAI(
    api_key="sk-xxxxx",
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[{"role": "user", "content": "你好"}]
)
```

---

### 7. 火山引擎（字节跳动）

**平台信息**
```
官网：https://console.volcengine.com/ark
API地址：https://ark.cn-beijing.volces.com/api/v3/chat/completions
模型：
  - doubao-pro：主力模型（¥0.004/千tokens）
额度：需要充值
```

**特点**
- 字节跳动背书，稳定可靠
- 价格便宜
- 性能不错

---

### 8. MiniMax

**平台信息**
```
官网：https://platform.minimaxi.com
API地址：https://api.minimaxi.chat/v1
模型：
  - abab6.5s：主力模型（¥0.01/千tokens）
  - abab6.5g：长文本支持
额度：需要充值
```

**特点**
- 长文本支持好
- 128K上下文
- 性价比不错

---

## OpenRouter（海外免费模型）

**官网**：https://openrouter.ai
**免费模型列表**：
| 模型 | 说明 |
|------|------|
| mimo-v2.5:free | MiMo免费通道 |
| deepseek-chat:free | DeepSeek免费 |
| llama-4-maverick:free | Meta最新模型 |

**限制**
- 免费：20请求/分钟，200请求/天
- 充值$10+后：1000请求/天

---

## Google AI Studio

**官网**：https://aistudio.google.com
**API地址**：https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent

**免费额度**
- 15 RPM（每分钟请求）
- 100万TPM（每分钟tokens）
- 模型：gemini-2.0-flash

**API调用**
```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("你好")
print(response.text)
```

---

## 模型选择推荐表

### 按需求推荐

| 需求 | 首选 | 备选 | 说明 |
|------|------|------|------|
| 日常对话 | MiMo | 智谱GLM | 中文优化好，免费 |
| 代码生成 | DeepSeek-Coder | DeepSeek-chat | 专用模型更强 |
| 数学推理 | DeepSeek-math | DeepSeek-reasoner | 数学专项 |
| 图像理解 | Kimi | 智谱GLM-4V | 长上下文 |
| 快速响应 | MiMo | 阿里qwen-turbo | 延迟低 |
| 长文本分析 | Kimi | MiniMax | 128K上下文 |
| 图像生成 | 智谱CogView | 阿里通义万相 | 中文优化 |

### 按预算推荐

| 预算 | 推荐方案 |
|------|---------|
| 完全免费 | MiMo + DeepSeek + 智谱 + 阿里百炼 |
| <¥10/月 | 火山引擎 + 硅基流动 |
| 无限制 | 任意商业模型 |

### 按使用量推荐

| 使用量 | 推荐策略 |
|--------|---------|
| <100次/天 | 任意免费平台轮换 |
| 100-1000次/天 | MiMo主力 + DeepSeek备用 |
| >1000次/天 | MiMo主力 + 多平台备用 + 监控 |

---

## 故障排查手册

### 401 Unauthorized
```
原因：
1. API Key错误或过期
2. Key被禁用
3. API地址错误

排查：
1. 检查Key是否正确复制（无多余空格）
2. 检查Key是否过期
3. 确认API地址是否正确
4. 检查账号是否被封禁

解决：
重新获取API Key
```

### 429 Rate Limit
```
原因：
1. 请求频率超限
2. 并发请求过多
3. 配额用完

排查：
1. 检查请求频率
2. 查看控制台配额
3. 确认是否有其他程序占用

解决：
1. 添加请求间隔（sleep）
2. 实现指数退避重试
3. 轮换多个API Key
4. 申请更高配额或换平台
```

### 500/502/503 Server Error
```
原因：
1. 平台服务端问题
2. 负载过高
3. 维护中

排查：
1. 检查平台状态页
2. 查看官方公告

解决：
1. 等待恢复
2. 切换到备用平台
3. 添加重试逻辑
```

### Connection Error
```
原因：
1. 网络不通
2. 防火墙拦截
3. 代理问题
4. API地址不可达

排查：
1. ping 目标地址
2. curl 测试连通性
3. 检查代理配置

解决：
1. 配置代理
2. 使用国内中转
3. 切换网络环境
```

---

## 安全最佳实践

### API Key保护
```python
# ✅ 正确做法
import os
API_KEY = os.getenv("MIMO_API_KEY")

# ❌ 错误做法
API_KEY = "sk-xxxxx"  # 直接写代码里
```

### 环境变量配置
```bash
# Linux/Mac
export MIMO_API_KEY="sk-xxxxx"
export DEEPSEEK_API_KEY="sk-xxxxx"

# Windows
set MIMO_API_KEY=sk-xxxxx

# Python dotenv
# .env文件
MIMO_API_KEY=sk-xxxxx
DEEPSEEK_API_KEY=sk-xxxxx
```

### 多Key负载均衡
```python
import random
import os

API_KEYS = [
    os.getenv("MIMO_KEY_1"),
    os.getenv("MIMO_KEY_2"),
    os.getenv("MIMO_KEY_3"),
]

def get_random_key():
    return random.choice([k for k in API_KEYS if k])

def chat_with_balance(message):
    for key in random.sample(API_KEYS, len(API_KEYS)):
        try:
            client = OpenAI(
                base_url="https://api.xiaomimimo.com/v1",
                api_key=key
            )
            # 调用...
            return result
        except RateLimitError:
            continue
    raise Exception("All keys rate limited")
```
