# Python 调用模板

> 这里放不同平台的最小 Python 调用骨架，优先给能跑的最短版本。

## Moonshot / Kimi

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MOONSHOT_API_KEY",
    base_url="https://api.moonshot.cn/v1",
)

resp = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[{"role": "user", "content": "你好"}]
)
print(resp.choices[0].message.content)
```

## 阿里云百炼

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

resp = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(resp.choices[0].message.content)
```

## SiliconFlow

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.siliconflow.cn/v1",
)

resp = client.chat.completions.create(
    model="Pro/zai-org/GLM-4.7",
    messages=[{"role": "user", "content": "你好"}]
)
print(resp.choices[0].message.content)
```

## DeepSeek

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com/v1",
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
print(resp.choices[0].message.content)
```

## MiniMax

> MiniMax 当前主文本接口路径与标准 OpenAI 路径不同，优先参考官方文档页面：
> https://platform.minimaxi.com/docs/api-reference/text-post
