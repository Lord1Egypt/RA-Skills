# 魔搭社区 API 参考文档

## API 端点

### 图片生成接口

**正确的 API 端点**（根据官方文档）：

```
POST https://api-inference.modelscope.cn/v1/images/generations
```

**注意**：
- Base URL: `https://api-inference.modelscope.cn/v1`
- 兼容 OpenAI API 格式
- 可以使用 OpenAI SDK 调用

### 模型列表获取接口

```
PUT https://modelscope.cn/api/v1/dolphin/models
```

**请求方法**：PUT（不是 GET）

**请求体格式**：
```json
{
  "PageSize": 30,
  "PageNumber": 1,
  "SortBy": "Default",
  "Target": "",
  "Criterion": [
    {
      "category": "tasks",
      "predicate": "contains",
      "values": ["text-to-image-synthesis"],
      "sub_values": []
    }
  ],
  "SingleCriterion": [
    {
      "category": "inference_type",
      "DateType": "int",
      "predicate": "equal",
      "IntValue": 1
    }
  ]
}
```

## 认证方式

在请求头中包含 API Token：

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## 获取 API Key

1. 访问魔搭社区：https://modelscope.cn
2. 登录/注册账号
3. 访问：https://modelscope.cn/my/myaccesstoken
4. 创建或复制你的 API Token

## 请求参数

### 必需参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型 ID，如 `Kwai-Kolors/Kolors` |
| `prompt` | string | 图片描述文本，支持中英文 |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `n` | integer | 1 | 生成图片数量 |
| `size` | string | "1024x1024" | 图片尺寸，如 "512x512", "1024x1024" |
| `response_format` | string | "url" | 响应格式: "url" 或 "b64_json" |

## 响应格式

### 成功响应

```json
{
  "created": 1234567890,
  "data": [
    {
      "url": "https://...",
      "b64_json": "base64编码的图片数据"
    }
  ]
}
```

### 错误响应

```json
{
  "error": {
    "message": "错误描述",
    "type": "错误类型",
    "code": "错误代码"
  }
}
```

## 使用限制

### API 推理限制

根据魔搭社区官方文档，API Inference 服务有以下重要限制：

1. **模型限制**
   - 仅支持标记为 `inference_type` 的模型
   - 不是所有"可体验"的模型都支持 API 调用
   - 使用前请确认模型是否支持 API 推理

2. **使用性质**
   - API Inference 为非商业化、非盈利产品
   - 仅适用于功能测试和前期验证
   - 商业用途请考虑付费方案

3. **并发限制**
   - 建议控制并发请求数量
   - 服务启动阶段避免立即发起高并发请求
   - 网络异常时注意重连策略

4. **速率限制**
   - 可能存在请求频率限制
   - 如遇到限制请稍后重试
   - 具体限制可能因账号类型而异

### 查看完整限制

访问官方文档查看最新的限制说明：
https://modelscope.cn/docs/model-service/API-Inference/limits

## 支持的模型

### 文生图模型（text-to-image-synthesis）

只有支持 `inference_type` 的模型才能通过 API 调用。

#### 热门模型

1. **Kolors** - `Kwai-Kolors/Kolors`
   - 快手可图模型
   - 支持中英文提示词
   - 高质量中文场景理解
   - 推荐：最适合中文提示词

2. **Stable Diffusion XL** - `AI-ModelScope/stable-diffusion-xl-base-1.0`
   - SDXL 1.0 基础模型
   - 高质量图像生成
   - 支持多种风格

3. **SDXL Turbo** - `AI-ModelScope/sdxl-turbo`
   - 快速生成
   - 一步推理
   - 适合实时应用

4. **FLUX.1 schnell** - `black-forest-labs/FLUX.1-schnell`
   - 高质量快速生成
   - 优秀的文本理解

#### 查找更多模型

**方法 1：使用命令行**
```bash
python3 gen.py --list-models
```

**方法 2：在线查看**
访问：https://modelscope.cn/models?filter=inference_type&tasks=text-to-image-synthesis

**方法 3：筛选条件**
在模型库页面使用以下筛选条件：
- 过滤器：`inference_type`
- 任务类型：`text-to-image-synthesis`
- 类型：`multi-modal`

## 示例代码

### Python 示例

```python
import requests
import json

url = "https://api-inference.modelscope.cn/api/v1/images/generations"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "Kwai-Kolors/Kolors",
    "prompt": "一只可爱的猫咪在花园里",
    "n": 1,
    "size": "1024x1024"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)
```

### cURL 示例

```bash
curl -X POST https://api-inference.modelscope.cn/api/v1/images/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Kwai-Kolors/Kolors",
    "prompt": "一只可爱的猫咪在花园里",
    "n": 1,
    "size": "1024x1024"
  }'
```

### 使用 urllib（Python 标准库）

```python
import urllib.request
import json

url = "https://api-inference.modelscope.cn/api/v1/images/generations"
data = {
    "model": "Kwai-Kolors/Kolors",
    "prompt": "一只可爱的猫咪",
    "n": 1,
    "size": "1024x1024"
}

req = urllib.request.Request(
    url,
    method="POST",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    },
    data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
)

with urllib.request.urlopen(req, timeout=300) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(result)
```

## 错误处理

### 常见错误码

| 状态码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | API Key 无效或未提供 | 检查 API Key 是否正确 |
| 404 | 模型不存在或不支持 API | 确认模型 ID，检查是否支持 inference_type |
| 429 | 请求过于频繁，触发限流 | 稍后重试，减少请求频率 |
| 500 | 服务器内部错误 | 稍后重试，如持续出现请联系支持 |

### 错误响应示例

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

## 最佳实践

### 1. 提示词优化

**中文提示词**
- 使用具体、详细的描述
- 包含风格、光照、角度等信息
- 示例：`"水墨画风格的江南水乡，柔和的晨光，远山如黛"`

**英文提示词**
- 遵循英文提示词最佳实践
- 使用修饰词增强效果
- 示例：`"ultra-detailed studio photo of a cat, soft lighting, high quality"`

### 2. 性能优化

- **快速生成**：使用 `sdxl-turbo` 或 `flux-schnell`
- **高质量生成**：使用 Kolors 或 SDXL
- **批量生成**：控制并发数量，避免触发限流

### 3. 成本控制

- 选择合适的图片尺寸
- 合理设置生成数量
- 测试阶段使用小尺寸快速迭代

### 4. 错误处理

```python
import time
import random

def call_api_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # 速率限制，等待后重试
                wait_time = (attempt + 1) * 2 + random.random()
                time.sleep(wait_time)
                continue
            else:
                raise Exception(f"API error: {response.status_code}")
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2)
```

## OpenAI API 兼容性

魔搭社区的 API Inference 服务提供与 OpenAI API 兼容的接口：

```python
from openai import OpenAI

client = OpenAI(
    api_key="MODELSCOPE_SDK_TOKEN",
    base_url="https://api-inference.modelscope.cn/v1"
)

response = client.images.generate(
    model="Kwai-Kolors/Kolors",
    prompt="一只可爱的猫咪",
    size="1024x1024",
    n=1
)

image_url = response.data[0].url
```

## 相关链接

- [官方文档](https://modelscope.cn/docs)
- [API 推理介绍](https://modelscope.cn/docs/model-service/API-Inference/intro)
- [使用限制](https://modelscope.cn/docs/model-service/API-Inference/limits)
- [模型库](https://modelscope.cn/models)
- [社区论坛](https://modelscope.cn/forum)

## 获取帮助

- 钉钉群：魔搭 ModelScope 开发者联盟群
- GitHub Issues：https://github.com/modelscope/modelscope/issues
- 社区论坛：https://modelscope.cn/forum
