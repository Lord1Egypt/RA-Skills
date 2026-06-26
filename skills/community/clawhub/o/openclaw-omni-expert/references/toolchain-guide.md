# OpenClaw 工具链配置指南

## 目录
- [内置工具](#内置工具)
- [工具分类](#工具分类)
- [自定义工具开发](#自定义工具开发)
- [API 接入模式](#api-接入模式)
- [工具链编排](#工具链编排)

---

## 内置工具

### 搜索工具

| 工具名称 | 功能 | 必填参数 |
|---------|------|---------|
| `google_search` | Google 搜索 | query |
| `bing_search` | Bing 搜索 | query |
| `ddg_search` | DuckDuckGo 搜索 | query |

### 网络工具

| 工具名称 | 功能 | 必填参数 |
|---------|------|---------|
| `web_fetch` | 网页抓取 | url |
| `web_screenshot` | 网页截图 | url |

### 实用工具

| 工具名称 | 功能 | 必填参数 |
|---------|------|---------|
| `calculator` | 数学计算 | expression |
| `code_interpreter` | 代码执行 | language, code |
| `json_parser` | JSON 解析 | data |

### 文件工具

| 工具名称 | 功能 | 必填参数 |
|---------|------|---------|
| `file_read` | 读取文件 | path |
| `file_write` | 写入文件 | path, content |

---

## 工具分类

### 1. 数据获取工具

```json
{
  "tools": [
    {
      "name": "web_search",
      "category": "data_acquisition",
      "description": "从互联网获取信息"
    },
    {
      "name": "db_query",
      "category": "data_acquisition",
      "description": "从数据库查询数据"
    },
    {
      "name": "api_call",
      "category": "data_acquisition",
      "description": "调用第三方 API"
    }
  ]
}
```

### 2. 数据处理工具

```json
{
  "tools": [
    {
      "name": "calculator",
      "category": "data_processing",
      "description": "数学运算"
    },
    {
      "name": "json_parser",
      "category": "data_processing",
      "description": "JSON 解析和转换"
    },
    {
      "name": "csv_processor",
      "category": "data_processing",
      "description": "CSV 数据处理"
    }
  ]
}
```

### 3. 通知工具

```json
{
  "tools": [
    {
      "name": "send_email",
      "category": "notification",
      "description": "发送邮件"
    },
    {
      "name": "send_sms",
      "category": "notification",
      "description": "发送短信"
    },
    {
      "name": "slack_notify",
      "category": "notification",
      "description": "发送 Slack 消息"
    }
  ]
}
```

---

## 自定义工具开发

### 工具结构

```python
from openclaw import BaseTool, ToolParameter

class MyCustomTool(BaseTool):
    name = "my_custom_tool"
    description = "自定义工具描述"
    category = "custom"
    
    parameters = [
        ToolParameter(
            name="input_param",
            type="string",
            required=True,
            description="输入参数描述"
        )
    ]
    
    def execute(self, params):
        # 获取参数
        input_value = params.get("input_param")
        
        # 执行逻辑
        result = self.process(input_value)
        
        return {
            "success": True,
            "result": result
        }
```

### 工具注册

```json
{
  "tools": [
    {
      "name": "my_custom_tool",
      "type": "custom",
      "path": "./plugins/my_tool.py",
      "enabled": true
    }
  ]
}
```

---

## API 接入模式

### 1. REST API 接入

```json
{
  "type": "tool",
  "name": "weather_api",
  "provider": "custom_api",
  "config": {
    "base_url": "https://api.weather.example.com",
    "auth": {
      "type": "api_key",
      "key": "YOUR_API_KEY"
    },
    "endpoints": {
      "current_weather": {
        "method": "GET",
        "path": "/weather/current",
        "params": {
          "city": "{{city}}"
        }
      }
    }
  }
}
```

### 2. OAuth API 接入

```json
{
  "config": {
    "auth": {
      "type": "oauth",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET",
      "authorization_url": "https://auth.example.com/authorize",
      "token_url": "https://auth.example.com/token"
    }
  }
}
```

### 3. Webhook 工具

```json
{
  "type": "tool",
  "name": "webhook_notification",
  "config": {
    "url": "https://your-webhook.com/endpoint",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer {{token}}"
    },
    "body": {
      "message": "{{message}}",
      "timestamp": "{{timestamp}}"
    }
  }
}
```

---

## 工具链编排

### 顺序执行

```json
{
  "chain": {
    "type": "sequential",
    "tools": [
      {"tool": "web_search", "output": "search_result"},
      {"tool": "web_fetch", "input": {"url": "{{search_result.0.url}}"}},
      {"tool": "summarize", "input": {"text": "{{web_fetch.content}}"}}
    ]
  }
}
```

### 并行执行

```json
{
  "chain": {
    "type": "parallel",
    "tools": [
      {"tool": "search_google", "query": "{{query}}"},
      {"tool": "search_bing", "query": "{{query}}"},
      {"tool": "search_duckduckgo", "query": "{{query}}"}
    ],
    "merge": "union"
  }
}
```

### 条件调用

```json
{
  "chain": {
    "type": "conditional",
    "condition": "{{input.type}}",
    "branches": {
      "weather": {"tool": "get_weather"},
      "news": {"tool": "get_news"},
      "default": {"tool": "general_search"}
    }
  }
}
```

---

## 最佳实践

### 1. 工具命名规范

```
category_action
- web_search
- db_query
- email_send
- file_read
```

### 2. 参数校验

```python
def validate_params(self, params):
    required = ["input", "format"]
    for param in required:
        if param not in params:
            raise ValueError(f"Missing required parameter: {param}")
    return True
```

### 3. 错误处理

```python
def execute(self, params):
    try:
        result = self.process(params)
        return {"success": True, "result": result}
    except TimeoutError:
        return {"success": False, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 4. 超时配置

```json
{
  "config": {
    "timeout": 30,
    "retry": {
      "enabled": true,
      "max_attempts": 3,
      "backoff": "exponential"
    }
  }
}
```

---

## 第三方 API 接入示例

### 天气 API

```json
{
  "name": "weather",
  "type": "tool",
  "api": {
    "provider": "openweathermap",
    "base_url": "https://api.openweathermap.org/data/2.5",
    "endpoints": {
      "current": {
        "method": "GET",
        "path": "/weather",
        "params": {
          "q": "{{city}}",
          "appid": "{{api_key}}"
        }
      }
    }
  }
}
```

### 翻译 API

```json
{
  "name": "translator",
  "type": "tool",
  "api": {
    "provider": "deepl",
    "base_url": "https://api-free.deepl.com/v2",
    "auth": {"type": "api_key", "key": "{{DEEPL_API_KEY}}"},
    "endpoints": {
      "translate": {
        "method": "POST",
        "path": "/translate",
        "body": {
          "text": "{{text}}",
          "target_lang": "{{target_lang}}"
        }
      }
    }
  }
}
```
