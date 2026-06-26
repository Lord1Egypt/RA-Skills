{
  "name": "openclaw-fallback-skill",
  "version": "1.0.0",
  "description": "当本地模型无法回答时，自动调用配置的云端大模型 API",
  "author": "Your Name",
  "permissions": ["http", "config"],
  "events": ["beforeResponse", "modelFailure"],
  "configSchema": {
    "type": "object",
    "properties": {
      "apiUrl": {
        "type": "string",
        "format": "uri",
        "description": "云端大模型的 API 地址"
      },
      "apiKey": {
        "type": "string",
        "description": "API 密钥"
      },
      "modelName": {
        "type": "string",
        "description": "模型名称（如 gpt-4, claude-3 等）",
        "default": "gpt-3.5-turbo"
      },
      "fallbackThreshold": {
        "type": "number",
        "description": "置信度阈值，低于此值触发 fallback",
        "default": 0.6,
        "minimum": 0,
        "maximum": 1
      },
      "maxRetries": {
        "type": "number",
        "default": 2
      },
      "timeout": {
        "type": "number",
        "description": "API 超时时间（秒）",
        "default": 30
      },
      "enableStreaming": {
        "type": "boolean",
        "default": false
      }
    },
    "required": ["apiUrl", "apiKey"]
  }
}