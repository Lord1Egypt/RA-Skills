# 模型接口说明（中文）

## 适用范围

本技能只依赖**文本改写模型接口**，不直接调用音频 ASR。
适用于：

- 输入法语音识别结束后的文本润色
- 聊天消息发送前的口语转书面语
- 将短文本整理成更自然、更干净的即时通讯表达
- 按需翻译到目标语言

## 默认接入配置

- 基地址：`https://models.audiozen.cn/v1`
- SDK：`openai`
- 默认模型：`doubao-seed-2-0-lite-260215`
- 鉴权：`api_key=<API_TOKEN>`

`API_TOKEN` 由使用者自行填写，**不要写死在技能包里**。

## 与你当前可用写法保持一致

脚本默认按下面这种方式调用：

```python
from openai import OpenAI

client = OpenAI(
    api_key="<YOUR_TOKEN>",
    base_url="https://models.audiozen.cn/v1"
)

resp = client.chat.completions.create(
    model="doubao-seed-2-0-pro-260215",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(resp.choices[0].message.content)
```

也就是说，脚本现在默认：

- 直接把 `base_url` 设为 `https://models.audiozen.cn/v1`
- 不再额外拼接 `/v1/chat/completions`
- 通过 `client.chat.completions.create(...)` 发起请求

## 环境变量

脚本支持以下环境变量：

- `IME_MODEL_BASE_URL`：模型服务基地址，默认 `https://models.audiozen.cn/v1`
- `IME_MODEL_NAME`：模型名，默认 `doubao-seed-2-0-lite-260215`
- `IME_MODEL_API_KEY`：调用 token，必填
- `IME_MODEL_TEMPERATURE`：采样温度，默认 `0.2`
- `IME_MODEL_TIMEOUT`：请求超时秒数，默认 `30`

## 默认请求格式

脚本默认按 OpenAI 兼容 chat completions 发送：

```json
{
  "model": "doubao-seed-2-0-lite-260215",
  "messages": [
    {
      "role": "system",
      "content": "你是输入法语音消息书面化助手。只输出最终文本。"
    },
    {
      "role": "user",
      "content": "原文：嗯我这边可能晚十分钟到你们先开始吧\n要求：将口语输入整理成适合即时通讯发送的自然书面语，保留原意，去掉语气词和重复，不要过度正式。"
    }
  ],
  "temperature": 0.2
}
```

默认从响应中读取：

- `choices[0].message.content`

## 默认改写要求

推荐默认值：

`将口语输入整理成适合即时通讯发送的自然书面语，保留原意，去掉语气词和重复，不要过度正式。`

## 翻译写法

当用户要求翻译时，建议把要求直接拼进 instruction：

- `将口语输入整理成适合即时通讯发送的自然书面语，然后翻译成英文。`
- `将口语输入整理成适合即时通讯发送的自然书面语，然后翻译成日文。`

## 错误处理

### 401 / 403
通常是 token 无效或权限不足。检查：
- `IME_MODEL_API_KEY` 是否填写
- token 是否过期
- 当前模型是否有调用权限

### 404
通常是基地址不对。检查：
- `IME_MODEL_BASE_URL` 是否确实为 `https://models.audiozen.cn/v1`
- 不要重复再拼 `/v1`

### 422 / 400
通常是请求字段不符合网关要求。检查：
- `model`
- `messages`
- `temperature`
- 认证配置

### 500
服务端内部错误。建议提示稍后重试，并可退回原始识别文本。

## 推荐回退策略

如果接口调用失败：

1. 优先提示“书面化失败，请稍后重试”。
2. 如果产品需要不中断流程，可退回原始识别文本。
3. 不要伪造模型返回结果。
