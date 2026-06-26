# JokeAPI Skill

获取各种类型的幽默笑话，支持分类、语言、格式过滤。

## 概述

使用 JokeAPI 免费获取笑话，无需注册或 API 密钥。支持多种分类、语言和响应格式。

## 基本用法

### 获取随机笑话

```bash
joke random
```

### 获取指定分类的笑话

```bash
joke random --category Programming
joke random --category Misc,Pun
```

### 获取特定类型的笑话

```bash
joke random --type single    # 单句笑话
joke random --type twopart   # 双部分笑话 (setup + delivery)
```

### 过滤不当内容

```bash
joke random --safe-mode              # 仅获取安全内容
joke random --blacklist nsfw,explicit  # 过滤特定类型内容
```

### 指定语言

```bash
joke random --lang en    # 英语笑话
joke random --lang de    # 德语笑话
```

### 获取多个笑话

```bash
joke random --amount 5
```

### 搜索包含特定关键词的笑话

```bash
joke random --contains "programmer"
```

## API 端点

### 主要端点

- **基础 URL**: `https://v2.jokeapi.dev`
- **获取笑话**: `GET /joke/{categories}`
- **获取信息**: `GET /info`
- **获取分类**: `GET /categories`
- **获取语言**: `GET /languages`

### 可用分类

- `Any` - 随机分类
- `Misc` - 杂项
- `Programming` - 编程
- `Dark` - 黑暗幽默
- `Pun` - 双关语
- `Spooky` - 恐怖
- `Christmas` - 圣诞

### 过滤标志 (blacklistFlags)

- `nsfw` - 不适宜工作场所
- `religious` - 宗教
- `political` - 政治
- `racist` - 种族主义
- `sexist` - 性别歧视
- `explicit` - 露骨内容

### 响应格式

- `json` (默认)
- `xml`
- `yaml`
- `txt` (纯文本)

## 示例代码

### JavaScript/Node.js

```javascript
const baseURL = "https://v2.jokeapi.dev";
const categories = ["Programming", "Misc"];
const params = [
  "blacklistFlags=nsfw,religious,racist",
  "type=single"
];

fetch(`${baseURL}/joke/${categories.join(",")}?${params.join("&")}`)
  .then(res => res.json())
  .then(joke => {
    if(joke.type == "single") {
      console.log(joke.joke);
    } else {
      console.log(joke.setup);
      setTimeout(() => {
        console.log(joke.delivery);
      }, 3000);
    }
  });
```

### Python

```python
import requests

url = "https://v2.jokeapi.dev/joke/Programming,Misc"
params = {
    "blacklistFlags": "nsfw,religious,racist",
    "type": "single",
    "format": "json"
}

response = requests.get(url, params=params)
joke = response.json()

if joke["type"] == "single":
    print(joke["joke"])
else:
    print(joke["setup"])
    # 延迟后显示 delivery
    print(joke["delivery"])
```

### Bash

```bash
curl -s "https://v2.jokeapi.dev/joke/Programming?format=txt&type=single&blacklistFlags=nsfw,religious,racist"
```

## 速率限制

- 每分钟最多 120 次请求
- 超出限制会返回 HTTP 429 错误
- 响应头包含速率限制信息：
  - `Retry-After` - 多少秒后重置
  - `RateLimit-Limit` - 每分钟最大请求数
  - `RateLimit-Remaining` - 剩余请求数

## 错误处理

API 返回统一格式的错误响应：

```json
{
  "error": true,
  "internalError": false,
  "code": 106,
  "message": "No matching joke found",
  "causedBy": ["No jokes were found that match your provided filter(s)"],
  "additionalInfo": "The specified category is invalid...",
  "timestamp": 1579170794412
}
```

## HTTP 状态码

- `200` - 成功
- `201` - 提交成功
- `400` - 请求格式错误
- `403` - 被黑名单封锁
- `404` - URL 不存在
- `429` - 请求过多
- `500` - 服务器内部错误

## 注意事项

⚠️ JokeAPI 包含多种类型的笑话，有些可能被视为冒犯性内容。建议：
- 启用 `safe-mode` 参数
- 使用 `blacklistFlags` 过滤不当内容
- 根据使用场景选择合适的分类

## 相关链接

- [官方文档](https://jokeapi.dev/)
- [GitHub 仓库](https://github.com/Sv443-Network/JokeAPI)
- [状态页面](https://status.sv443.net/)
- [Discord 服务器](https://sv443.net/discord)
