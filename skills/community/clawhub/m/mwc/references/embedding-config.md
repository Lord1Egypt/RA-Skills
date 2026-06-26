# Embedding 配置（高级智能推荐）

配置模板：`assets/embedding-config.template.json`

## 配置位置

- `~/.wallpaper_prefs.json` 的 `embedding` 字段
- 或环境变量 `WALLPAPER_EMBEDDING_CONFIG` 指向的 JSON 路径

## Schema

| 字段              | 类型     | 说明                                                     |
| ----------------- | -------- | -------------------------------------------------------- |
| `provider`        | string   | `openai` / `ollama` / `sentence-transformers` / `custom` |
| `model`           | string   | 模型名称                                                 |
| `api_key`         | string   | API Key（OpenAI/custom 需填）                            |
| `dimensions`      | int      | 向量维度（可选）                                         |
| `endpoint`        | string   | 自定义端点（ollama/custom 需填）                         |
| `metadata_fields` | string[] | 参与 embedding 的偏好字段                                |

## 提供商示例

**OpenAI**：`provider: openai`，`api_key` 必填  
**Ollama**：`provider: ollama`，`endpoint: http://localhost:11434/api/embeddings`  
**Sentence-Transformers**：`provider: sentence-transformers`，无需 api_key  
**Custom**：`provider: custom`，`endpoint` + `api_key` 必填
