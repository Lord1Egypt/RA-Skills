# Provider 設定

## 設定方式

透過 `opencode.json` 的 `provider` 欄位自訂：

```json
{
  "provider": {
    "minimax-portal": {
      "options": {
        "baseURL": "https://api.minimax.io/v1",
        "apiKey": "{env:MINIMAX_API_KEY}"
      }
    }
  }
}
```

## 自訂 Base URL

```json
{
  "provider": {
    "anthropic": {
      "options": {
        "baseURL": "https://api.anthropic.com/v1"
      }
    }
  }
}
```

## OpenAI 相容 Provider

用 `@ai-sdk/openai-compatible` 包裝任何 OpenAI 相容 API：

```json
{
  "provider": {
    "myprovider": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "My Provider",
      "options": {
        "baseURL": "https://api.myprovider.com/v1",
        "apiKey": "{env:MY_API_KEY}",
        "headers": {
          "Authorization": "Bearer custom-token"
        }
      },
      "models": {
        "my-model": {
          "name": "My Model Display",
          "limit": {
            "context": 128000,
            "output": 65536
          }
        }
      }
    }
  }
}
```

## LM Studio（本地模型）

```json
{
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (local)",
      "options": {
        "baseURL": "http://127.0.0.1:1234/v1"
      },
      "models": {
        "google/gemma-3n-e4b": {
          "name": "Gemma 3n-e4b (local)"
        }
      }
    }
  }
}
```

## Ollama（本地模型）

```json
{
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "llama2": { "name": "Llama 2" }
      }
    }
  }
}
```

## llama.cpp（本地模型）

```json
{
  "provider": {
    "llama.cpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama-server (local)",
      "options": {
        "baseURL": "http://127.0.0.1:8080/v1"
      },
      "models": {
        "qwen3-coder:a3b": {
          "name": "Qwen3-Coder: a3b-30b (local)",
          "limit": { "context": 128000, "output": 65536 }
        }
      }
    }
  }
}
```

## Ollama Cloud

```json
{
  "provider": {
    "ollama-cloud": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama Cloud",
      "options": {
        "baseURL": "https://api.ollama.cloud/v1"
      }
    }
  }
}
```

## Cloudflare AI Gateway

```json
{
  "provider": {
    "cloudflare-ai-gateway": {
      "options": {
        "baseURL": "https://gateway.ai.cloudflare.com/{account_id}/{gateway_id}/v1"
      }
    }
  }
}
```

## 認證方式

| 方式 | 說明 |
|------|------|
| `/connect` 指令 | 互動式設定，儲存到 `~/.local/share/opencode/auth.json` |
| 環境變數 | `{env:VARIABLE_NAME}` 語法 |
| 檔案內容 | `{file:path/to/file}` 語法 |
| 直接設定 | 在 JSON 中設定 `options.apiKey` |

## API Key 優先順序

1. 設定檔中的 `options.apiKey`
2. 環境變數 `OPENAI_API_KEY` 等
3. `/connect` 儲存的認證

## 疑難排解

- 檢查 `/connect` 指令中使用的 Provider ID 是否與設定檔一致
- 確認 `options.baseURL` 正確（有些需要 `/v1` 尾綴，有些不需要）
- 執行 `opencode auth list` 查看已儲存的憑證
- 用 `{env:VAR}` 而非直接寫入 API Key
