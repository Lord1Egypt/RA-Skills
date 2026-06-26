# MediaIO AIGC API Capability Reference (Generated from c_api_doc_detail.json)

- Generated at: 2026-03-10 17:26:49
- Total APIs: 24
- Invocation pattern: Skill.invoke(api_name, params, api_key)
- Important note: API names are unique in the current `c_api_doc_detail.json`; keep names unique to avoid routing ambiguity.

## 1. General Invocation Rules

### 1.1 Unified Entry Point
```python
from scripts.skill_router import Skill
import os

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')

result = skill.invoke(api_name, params, api_key=api_key)
print(result)
```

### 1.2 Standard Async Workflow
1. Call a generation endpoint and obtain `data.task_id`.
2. Poll `Task Result` with the task ID.
3. When status becomes `completed` or `succeeded`, extract output URLs from `data.result`.

### 1.3 Common Status and Error Codes
- Task status: `waiting`, `processing`, `completed`, `failed`, `timeout`
- `374004`: authentication required / invalid API key
- `490505`: insufficient credits

## 2. Capability Overview

### Query APIs (2)
- Credits | model_code=user-credits | POST https://openapi.media.io/user/credits
- Task Result | model_code=generation-result | POST https://openapi.media.io/generation/result/{task_id}

### Text To Image (2)
- Imagen 4 | model_code=t2i-imagen-4 | POST https://openapi.media.io/generation/imagen/t2i-imagen-4
- soul_character | model_code=t2i-soul-character | POST https://openapi.media.io/generation/soul/t2i-soul-character

### Image To Image (3)
- Nano Banana | model_code=i2i-banana | POST https://openapi.media.io/generation/banana/i2i-banana
- Seedream 4.0 | model_code=i2i-seedream-v4-0 | POST https://openapi.media.io/generation/seedream/i2i-seedream-v4-0
- Nano Banana Pro | model_code=i2i-banana-2 | POST https://openapi.media.io/generation/banana/i2i-banana-2

### Image To Video (14)
- Wan 2.6 | model_code=i2v-wan-v2-6 | POST https://openapi.media.io/generation/wan/i2v-wan-v2-6
- Wan 2.2 | model_code=i2v-wan-v2-2 | POST https://openapi.media.io/generation/wan/i2v-wan-v2-2
- Hailuo 02 | model_code=i2v-minimax-02 | POST https://openapi.media.io/generation/minimax/i2v-minimax-02
- Kling 2.1 | model_code=i2v-kling-v2-1 | POST https://openapi.media.io/generation/kling/i2v-kling-v2-1
- Vidu Q3 | model_code=i2v-vidu-q3 | POST https://openapi.media.io/generation/vidu/i2v-vidu-q3
- Kling 2.5 Turbo | model_code=i2v-kling-v2-5-turbo | POST https://openapi.media.io/generation/kling/i2v-kling-v2-5-turbo
- Google Veo 3.1 | model_code=i2v-veo-v3-1 | POST https://openapi.media.io/generation/veo/i2v-veo-v3-1
- Kling 3.0 | model_code=i2v-kling-v3-0 | POST https://openapi.media.io/generation/kling/i2v-kling-v3-0
- Hailuo 2.3 | model_code=i2v-minimax-v2-3 | POST https://openapi.media.io/generation/minimax/i2v-minimax-v2-3
- Vidu Q2 | model_code=i2v-vidu-q2 | POST https://openapi.media.io/generation/vidu/i2v-vidu-q2
- Wan 2.5 | model_code=i2v-wan-v2-5 | POST https://openapi.media.io/generation/wan/i2v-wan-v2-5
- Kling 2.6 | model_code=i2v-kling-v2-6 | POST https://openapi.media.io/generation/kling/i2v-kling-v2-6
- Motion Control Kling 2.6 | model_code=i2v-motion-control-kling-v2-6 | POST https://openapi.media.io/generation/kling/i2v-motion-control-kling-v2-6
- Google Veo 3.1 Fast | model_code=i2v-veo-v3-1-fast | POST https://openapi.media.io/generation/veo/i2v-veo-v3-1-fast

### Text To Video (3)
- Wan 2.6 (Text To Video) | model_code=t2v-wan-v2-6 | POST https://openapi.media.io/generation/wan/t2v-wan-v2-6
- Vidu Q3 (Text To Video) | model_code=t2v-vidu-q3 | POST https://openapi.media.io/generation/vidu/t2v-vidu-q3
- Wan 2.5 (Text To Video) | model_code=t2v-wan-v2-5 | POST https://openapi.media.io/generation/wan/t2v-wan-v2-5

## 3. Detailed API Documentation

### Query APIs

#### Query APIs-1 Credits (model_code: user-credits)
- API ID: 196
- Method: POST
- Endpoint: https://openapi.media.io/user/credits
- Description: API to query user credits balance.

- Parameters: none (use `{}`)

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "Query User Credits",
      "language": "cURL",
      "code_example": "curl --request POST \n  --url https://openapi.media.io/user/credits \n  --header 'Content-Type: application/json' \n  --header 'X-API-KEY: <api-key>' \n  --data '{}'"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "credits",
      "type": "integer",
      "describe": "User credits balance, located within the data object"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Credits',
    {},
    api_key=api_key
)
print(result)
```

#### Query APIs-2 Task Result (model_code: generation-result)
- API ID: 197
- Method: POST
- Endpoint: https://openapi.media.io/generation/result/{task_id}
- Description: API to query generation task result by task ID.

| Parameter | Type | Required | Description |
|---|---|---|---|
| task_id | string | Yes | The task ID to query, located in the URL path parameter |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "Query Task Result",
      "language": "cURL",
      "code_example": "curl --request POST \n  --url https://openapi.media.io/generation/result/<task_id> \n  --header 'Content-Type: application/json' \n  --header 'X-API-KEY: <api-key>' \n  --data '{}'"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Task identifier"
    },
    {
      "name": "status",
      "type": "string",
      "describe": "Task status: pending, processing, succeeded, failed"
    },
    {
      "name": "result",
      "type": "object",
      "describe": "Generation result when task succeeded"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Task Result',
    {
        "task_id": "<required>"
    },
    api_key=api_key
)
print(result)
```

### Text To Image

#### Text To Image-1 Imagen 4 (model_code: t2i-imagen-4)
- API ID: 259
- Method: POST
- Endpoint: https://openapi.media.io/generation/imagen/t2i-imagen-4
- Description: Sets a new standard for photorealism and text rendering accuracy, handling the most complex prompts with ease.

| Parameter | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1200. |
| ratio | string | No | Target aspect ratio. Options: 9:16, 16:9, 1:1, 4:3, 3:4. Default is 9:16. Allowed values: 9:16, 16:9, 1:1, 4:3, 3:4. |
| counts | string | No | Counts parameter. Options: 1, 2, 3, 4. Default is 1. Allowed values: 1, 2, 3, 4. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create image by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/imagen/t2i-imagen-4 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"counts\": \"1\",\n    \"prompt\": \"<string>\",\n    \"ratio\": \"9:16\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Imagen 4',
    {
        "prompt": "<required>",
        "ratio": "<optional>",
        "counts": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Text To Image-2 soul_character (model_code: t2i-soul-character)
- API ID: 260
- Method: POST
- Endpoint: https://openapi.media.io/generation/soul/t2i-soul-character
- Description: Delivers the most cost-effective solution with ultra-fast generation speeds, perfect for high-volume commercial applications.

| Parameter | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| ratio | string | No | Target aspect ratio. Options: 2:3, 1:1, 3:2, 9:16, 16:9. Default is 16:9. Allowed values: 2:3, 1:1, 3:2, 9:16, 16:9. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create image by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/soul/t2i-soul-character \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"prompt\": \"<string>\",\n    \"ratio\": \"16:9\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'soul_character',
    {
        "prompt": "<required>",
        "ratio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

### Image To Image

#### Image To Image-1 Nano Banana (model_code: i2i-banana)
- API ID: 242
- Method: POST
- Endpoint: https://openapi.media.io/generation/banana/i2i-banana
- Description: Utilizes next-gen multimodal reasoning to generate images that perfectly align with nuanced conceptual descriptions.

| Parameter | Type | Required | Description |
|---|---|---|---|
| images | array<string> | Yes | The URLs of the input images. Supported formats include PNG, JPEG, and JPG. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 1280x1280. Aspect ratio must be between 1:2 and 2:1. Maximum 9 file(s). |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1200. |
| ratio | string | No | Target aspect ratio. Options: 9:16, 16:9, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9. Default is 16:9. Allowed values: 9:16, 16:9, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create image by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/banana/i2i-banana \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"images\": [\n      \"<string>\"\n    ],\n    \"prompt\": \"<string>\",\n    \"ratio\": \"16:9\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Nano Banana',
    {
        "images": "<required>",
        "prompt": "<required>",
        "ratio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Image-2 Seedream 4.0 (model_code: i2i-seedream-v4-0)
- API ID: 243
- Method: POST
- Endpoint: https://openapi.media.io/generation/seedream/i2i-seedream-v4-0
- Description: A versatile powerhouse supporting 4K generation and advanced editing, ensuring character and style consistency.

| Parameter | Type | Required | Description |
|---|---|---|---|
| images | array<string> | Yes | The URLs of the input images. Supported formats include PNG, JPEG, and JPG. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 300x300 and 1280x1280. Aspect ratio must be between 3:10 and 3:1. Maximum 9 file(s). |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 800. |
| ratio | string | No | Target aspect ratio. Options: 9:16, 16:9, 1:1, 4:3, 3:4, 3:2, 2:3. Default is 9:16. Allowed values: 9:16, 16:9, 1:1, 4:3, 3:4, 3:2, 2:3. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create image by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/seedream/i2i-seedream-v4-0 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"images\": [\n      \"<string>\"\n    ],\n    \"prompt\": \"<string>\",\n    \"ratio\": \"9:16\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Seedream 4.0',
    {
        "images": "<required>",
        "prompt": "<required>",
        "ratio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Image-3 Nano Banana Pro (model_code: i2i-banana-2)
- API ID: 244
- Method: POST
- Endpoint: https://openapi.media.io/generation/banana/i2i-banana-2
- Description: Utilizes next-gen multimodal reasoning to generate images that perfectly align with nuanced conceptual descriptions.

| Parameter | Type | Required | Description |
|---|---|---|---|
| images | array<string> | Yes | The URLs of the input images. Supported formats include PNG, JPEG, and JPG. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 1280x1280. Aspect ratio must be between 1:2 and 2:1. Maximum 9 file(s). |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1200. |
| ratio | string | No | Target aspect ratio. Options: 9:16, 16:9, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9. Default is 16:9. Allowed values: 9:16, 16:9, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9. |
| resolution | string | No | Output resolution. Options: 1K, 2K, 4K. Default is 1K. Allowed values: 1K, 2K, 4K. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create image by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/banana/i2i-banana-2 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"images\": [\n      \"<string>\"\n    ],\n    \"prompt\": \"<string>\",\n    \"ratio\": \"16:9\",\n    \"resolution\": \"1K\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Nano Banana Pro',
    {
        "images": "<required>",
        "prompt": "<required>",
        "ratio": "<optional>",
        "resolution": "<optional>"
    },
    api_key=api_key
)
print(result)
```

### Image To Video

#### Image To Video-1 Wan 2.6 (model_code: i2v-wan-v2-6)
- API ID: 245
- Method: POST
- Endpoint: https://openapi.media.io/generation/wan/i2v-wan-v2-6
- Description: Features advanced multi-shot storytelling and native audio-visual synchronization, ideal for creating complex narratives with consistent characters.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, and BMP. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 300x300 and 2000x2000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1500. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 720P. Allowed values: 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s, 15s. Default is 5s. Allowed values: 5s, 10s, 15s. |
| shot_type | string | No | Shot Type parameter. Options: Multi, Single. Default is Multi. Allowed values: Multi, Single. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/wan/i2v-wan-v2-6 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"generate_audio\": \"True\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"720P\",\n    \"shot_type\": \"Multi\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Wan 2.6',
    {
        "image": "<required>",
        "prompt": "<required>",
        "resolution": "<optional>",
        "duration": "<optional>",
        "shot_type": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-2 Wan 2.2 (model_code: i2v-wan-v2-2)
- API ID: 246
- Method: POST
- Endpoint: https://openapi.media.io/generation/wan/i2v-wan-v2-2
- Description: A balanced video generation model offering reliable motion quality and prompt adherence for general tasks.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, and BMP. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 300x300 and 2000x2000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 800. |
| resolution | string | No | Output resolution. Options: 1080P. Default is 1080P. Allowed values: 1080P. |
| duration | string | No | Video duration in seconds. Options: 5s. Default is 5s. Allowed values: 5s. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/wan/i2v-wan-v2-2 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"1080P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Wan 2.2',
    {
        "image": "<required>",
        "prompt": "<required>",
        "resolution": "<optional>",
        "duration": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-3 Hailuo 02 (model_code: i2v-minimax-02)
- API ID: 247
- Method: POST
- Endpoint: https://openapi.media.io/generation/minimax/i2v-minimax-02
- Description: Excels in cinematic realism and complex physics simulation, offering 'Director-level' control over camera movements and high fidelity.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| duration | string | No | Video duration in seconds. Options: 6s. Default is 6s. Allowed values: 6s. |
| resolution | string | No | Output resolution. Options: 768P, 1080P. Default is 768P. Allowed values: 768P, 1080P. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/minimax/i2v-minimax-02 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"6s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"768P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Hailuo 02',
    {
        "image": "<required>",
        "prompt": "<required>",
        "duration": "<optional>",
        "resolution": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-4 Kling 2.1 (model_code: i2v-kling-v2-1)
- API ID: 248
- Method: POST
- Endpoint: https://openapi.media.io/generation/kling/i2v-kling-v2-1
- Description: A robust model known for producing realistic videos with stable motion and good prompt understanding.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s. Default is 5s. Allowed values: 5s, 10s. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 720P. Allowed values: 720P, 1080P. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/kling/i2v-kling-v2-1 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"720P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Kling 2.1',
    {
        "image": "<required>",
        "prompt": "<required>",
        "duration": "<optional>",
        "resolution": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-5 Vidu Q3 (model_code: i2v-vidu-q3)
- API ID: 249
- Method: POST
- Endpoint: https://openapi.media.io/generation/vidu/i2v-vidu-q3
- Description: The latest iteration optimized for superior speed and high-definition output, enabling rapid high-quality video creation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, and JPG. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 150x150 and 4000x4000. Aspect ratio must be between 1:4 and 4:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| resolution | string | No | Output resolution. Options: 540P, 720P, 1080P. Default is 720P. Allowed values: 540P, 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 4s, 8s, 12s, 16s. Default is 4s. Allowed values: 4s, 8s, 12s, 16s. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/vidu/i2v-vidu-q3 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"4s\",\n    \"generate_audio\": \"True\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"720P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Vidu Q3',
    {
        "image": "<required>",
        "prompt": "<required>",
        "resolution": "<optional>",
        "duration": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-6 Kling 2.5 Turbo (model_code: i2v-kling-v2-5-turbo)
- API ID: 251
- Method: POST
- Endpoint: https://openapi.media.io/generation/kling/i2v-kling-v2-5-turbo
- Description: Offers advanced motion control and high realism, bridging the gap between standard and professional output.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2500. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s. Default is 5s. Allowed values: 5s, 10s. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 1080P. Allowed values: 720P, 1080P. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/kling/i2v-kling-v2-5-turbo \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"1080P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Kling 2.5 Turbo',
    {
        "image": "<required>",
        "prompt": "<required>",
        "duration": "<optional>",
        "resolution": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-7 Google Veo 3.1 (model_code: i2v-veo-v3-1)
- API ID: 252
- Method: POST
- Endpoint: https://openapi.media.io/generation/veo/i2v-veo-v3-1
- Description: A state-of-the-art model offering exceptional resolution and deep understanding of complex prompts for cinematic results.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include JPG, JPEG, PNG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 50.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1000. |
| aspect_ratio | string | No | Target aspect ratio. Options: 9:16, 16:9. Default is 9:16. Allowed values: 9:16, 16:9. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 720P. Allowed values: 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 4s, 6s, 8s. Default is 4s. Allowed values: 4s, 6s, 8s. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/veo/i2v-veo-v3-1 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"aspect_ratio\": \"9:16\",\n    \"duration\": \"4s\",\n    \"generate_audio\": \"True\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"720P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Google Veo 3.1',
    {
        "image": "<required>",
        "prompt": "<required>",
        "aspect_ratio": "<optional>",
        "resolution": "<optional>",
        "duration": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-8 Kling 3.0 (model_code: i2v-kling-v3-0)
- API ID: 253
- Method: POST
- Endpoint: https://openapi.media.io/generation/kling/i2v-kling-v3-0
- Description: The latest high-fidelity generation delivering ultra-realistic motion and superior detail, suitable for professional-grade video production.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2500. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 1080P. Allowed values: 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 5s, 8s, 10s, 15s. Default is 5s. Allowed values: 5s, 8s, 10s, 15s. |
| multi_shots | string | No | Multi Shots parameter. Options: True, False. Default is True. Allowed values: True, False. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/kling/i2v-kling-v3-0 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"generate_audio\": \"True\",\n    \"image\": \"<string>\",\n    \"multi_shots\": \"True\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"1080P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Kling 3.0',
    {
        "image": "<required>",
        "prompt": "<required>",
        "resolution": "<optional>",
        "duration": "<optional>",
        "multi_shots": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-9 Hailuo 2.3 (model_code: i2v-minimax-v2-3)
- API ID: 254
- Method: POST
- Endpoint: https://openapi.media.io/generation/minimax/i2v-minimax-v2-3
- Description: Excels in cinematic realism and complex physics simulation, offering 'Director-level' control over camera movements and high fidelity.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| resolution | string | No | Output resolution. Options: 768P, 1080P (when duration is 6s). Default is 768P. Allowed values: 768P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 6s, 10s. Default is 6s. Allowed values: 6s, 10s. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/minimax/i2v-minimax-v2-3 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"6s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"768P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Hailuo 2.3',
    {
        "image": "<required>",
        "prompt": "<required>",
        "resolution": "<optional>",
        "duration": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-10 Vidu Q2 (model_code: i2v-vidu-q2)
- API ID: 255
- Method: POST
- Endpoint: https://openapi.media.io/generation/vidu/i2v-vidu-q2
- Description: A fast and efficient model that balances generation speed with good visual fidelity.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 150x150 and 4000x4000. Aspect ratio must be between 1:4 and 4:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| duration | string | No | Video duration in seconds. Options: 4s, 6s, 8s. Default is 4s. Allowed values: 4s, 6s, 8s. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 720P. Allowed values: 720P, 1080P. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/vidu/i2v-vidu-q2 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"4s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"720P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Vidu Q2',
    {
        "image": "<required>",
        "prompt": "<required>",
        "duration": "<optional>",
        "resolution": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-11 Wan 2.5 (model_code: i2v-wan-v2-5)
- API ID: 256
- Method: POST
- Endpoint: https://openapi.media.io/generation/wan/i2v-wan-v2-5
- Description: An enhanced version offering improved motion stability and visual quality compared to earlier iterations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, and BMP. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 300x300 and 2000x2000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 800. |
| resolution | string | No | Output resolution. Options: 480P, 720P, 1080P. Default is 480P. Allowed values: 480P, 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s. Default is 5s. Allowed values: 5s, 10s. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/wan/i2v-wan-v2-5 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"480P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Wan 2.5',
    {
        "image": "<required>",
        "prompt": "<required>",
        "resolution": "<optional>",
        "duration": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-12 Kling 2.6 (model_code: i2v-kling-v2-6)
- API ID: 257
- Method: POST
- Endpoint: https://openapi.media.io/generation/kling/i2v-kling-v2-6
- Description: Kling AI's video model, recognized for its ability to generate realistic and coherent motion.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, JPG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 20.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2.5:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2500. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s. Default is 5s. Allowed values: 5s, 10s. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/kling/i2v-kling-v2-6 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"generate_audio\": \"True\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Kling 2.6',
    {
        "image": "<required>",
        "prompt": "<required>",
        "duration": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-13 Motion Control Kling 2.6 (model_code: i2v-motion-control-kling-v2-6)
- API ID: 258
- Method: POST
- Endpoint: https://openapi.media.io/generation/kling/i2v-motion-control-kling-v2-6
- Description: Offers advanced motion control and high realism, bridging the gap between standard and professional output.

| Parameter | Type | Required | Description |
|---|---|---|---|
| video | string | Yes | The URL of the input video. Supported formats include MP4 and MOV. File size must be between 0.0 MB and 100.0 MB. Video resolution must be between 720x720 and 2160x2160. Frame rate must be between 24 and 60 FPS. Duration must be between 3 and 30 seconds. |
| image | string | Yes | The URL of the input image. Supported formats include PNG, JPEG, and JPG. File size must be between 0.0 MB and 10.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 1:2 and 2:1. |
| prompt | string | No | The text prompt describing the content to generate. Maximum string length: 2500. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/kling/i2v-motion-control-kling-v2-6 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"video\": \"<string>\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Motion Control Kling 2.6',
    {
        "video": "<required>",
        "image": "<required>",
        "prompt": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Image To Video-14 Google Veo 3.1 Fast (model_code: i2v-veo-v3-1-fast)
- API ID: 264
- Method: POST
- Endpoint: https://openapi.media.io/generation/veo/i2v-veo-v3-1-fast
- Description: Google Veo 3.1 Fast is an AI model for video generation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| image | string | Yes | The URL of the input image. Supported formats include JPG, JPEG, PNG, WEBP, GIF, and HEIC. File size must be between 0.0 MB and 50.0 MB. Image resolution must be between 300x300 and 4000x4000. Aspect ratio must be between 0.4:1 and 2:1. |
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1000. |
| aspect_ratio | string | No | Target aspect ratio. Options: 9:16, 16:9. Default is 9:16. Allowed values: 9:16, 16:9. |
| resolution | string | No | Output resolution. Options: 720P, 1080P. Default is 720P. Allowed values: 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 4s, 6s, 8s. Default is 4s. Allowed values: 4s, 6s, 8s. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/veo/i2v-veo-v3-1-fast \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"aspect_ratio\": \"9:16\",\n    \"duration\": \"4s\",\n    \"generate_audio\": \"True\",\n    \"image\": \"<string>\",\n    \"prompt\": \"<string>\",\n    \"resolution\": \"720P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Google Veo 3.1 Fast',
    {
        "image": "<required>",
        "prompt": "<required>",
        "aspect_ratio": "<optional>",
        "resolution": "<optional>",
        "duration": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

### Text To Video

#### Text To Video-1 Wan 2.6 (model_code: t2v-wan-v2-6)
- API ID: 261
- Method: POST
- Endpoint: https://openapi.media.io/generation/wan/t2v-wan-v2-6
- Description: Features advanced multi-shot storytelling and native audio-visual synchronization, ideal for creating complex narratives with consistent characters.

| Parameter | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 1500. |
| size | string | No | Output size. Options: 9:16, 16:9, 1:1, 4:3, 3:4. Default is 16:9. Allowed values: 9:16, 16:9, 1:1, 4:3, 3:4. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s, 15s. Default is 5s. Allowed values: 5s, 10s, 15s. |
| shot_type | string | No | Shot Type parameter. Options: Multi, Single. Default is Multi. Allowed values: Multi, Single. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/wan/t2v-wan-v2-6 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"generate_audio\": \"True\",\n    \"prompt\": \"<string>\",\n    \"shot_type\": \"Multi\",\n    \"size\": \"16:9\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Wan 2.6',
    {
        "prompt": "<required>",
        "size": "<optional>",
        "duration": "<optional>",
        "shot_type": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Text To Video-2 Vidu Q3 (model_code: t2v-vidu-q3)
- API ID: 262
- Method: POST
- Endpoint: https://openapi.media.io/generation/vidu/t2v-vidu-q3
- Description: The latest iteration optimized for superior speed and high-definition output, enabling rapid high-quality video creation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 2000. |
| ratio | string | No | Target aspect ratio. Options: 9:16, 16:9, 1:1, 4:3, 3:4. Default is 16:9. Allowed values: 9:16, 16:9, 1:1, 4:3, 3:4. |
| resolution | string | No | Output resolution. Options: 540P, 720P, 1080P. Default is 720P. Allowed values: 540P, 720P, 1080P. |
| duration | string | No | Video duration in seconds. Options: 4s, 8s, 12s, 16s. Default is 8s. Allowed values: 4s, 8s, 12s, 16s. |
| generate_audio | string | No | Generate Audio parameter. Options: True, False. Default is True. Allowed values: True, False. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/vidu/t2v-vidu-q3 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"8s\",\n    \"generate_audio\": \"True\",\n    \"prompt\": \"<string>\",\n    \"ratio\": \"16:9\",\n    \"resolution\": \"720P\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Vidu Q3',
    {
        "prompt": "<required>",
        "ratio": "<optional>",
        "resolution": "<optional>",
        "duration": "<optional>",
        "generate_audio": "<optional>"
    },
    api_key=api_key
)
print(result)
```

#### Text To Video-3 Wan 2.5 (model_code: t2v-wan-v2-5)
- API ID: 263
- Method: POST
- Endpoint: https://openapi.media.io/generation/wan/t2v-wan-v2-5
- Description: An enhanced version offering improved motion stability and visual quality compared to earlier iterations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | The text prompt describing the content to generate. Maximum string length: 800. |
| ratio | string | No | Target aspect ratio. Options: 16:9, 9:16, 1:1, 4:3, 3:4. Default is 16:9. Allowed values: 16:9, 9:16, 1:1, 4:3, 3:4. |
| duration | string | No | Video duration in seconds. Options: 5s, 10s. Default is 5s. Allowed values: 5s, 10s. |

##### Request Example
```json
{
  "title": "Example Request",
  "request": [
    {
      "title": "create video by text or image",
      "language": "cURL",
      "code_example": "curl --request POST \\\n  --url https://openapi.media.io/generation/wan/t2v-wan-v2-5 \\\n  --header 'Content-Type: application/json' \\\n  --header 'X-API-KEY: <api-key>' \\\n  --data '\n{\n  \"data\": {\n    \"duration\": \"5s\",\n    \"prompt\": \"<Your prompt text, 1-800 characters>\",\n    \"ratio\": \"16:9\"\n  }\n}'\n"
    }
  ],
  "describe": "",
  "response": [
    {
      "type": "200",
      "code_example": "{\n  \"code\": 0,\n  \"msg\": \"\",\n  \"data\": {\n    \"task_id\": <string>\"\n  },\n  \"trace_id\": <string>\"\n}"
    },
    {
      "type": "default",
      "code_example": "{\n  \"code\": <integer>,\n  \"msg\": <string>,\n  \"data\": {},\n  \"trace_id\": <string>\"\n}"
    }
  ]
}
```

##### Response Example
```json
{
  "list": [
    {
      "name": "code",
      "type": "integer",
      "describe": "Response status code, 0 indicates success"
    },
    {
      "name": "msg",
      "type": "string",
      "describe": "Response message, empty string on success"
    },
    {
      "name": "data",
      "type": "object",
      "describe": "Response data object"
    },
    {
      "name": "task_id",
      "type": "string",
      "describe": "Unique task identifier, located within the data object"
    },
    {
      "name": "trace_id",
      "type": "string",
      "describe": "Request tracking ID"
    }
  ],
  "title": "Response",
  "describe": "After the request is successfully processed, the server will return the following response"
}
```

##### Skill.invoke Template
```python
result = skill.invoke(
    'Wan 2.5',
    {
        "prompt": "<required>",
        "ratio": "<optional>",
        "duration": "<optional>"
    },
    api_key=api_key
)
print(result)
```

## 4. Recommended Runtime Templates

### 4.1 Text-to-Image Workflow (`Imagen 4` + `Task Result`)
```python
import os
import time
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')

create = skill.invoke('Imagen 4', {
    'prompt': 'A cute kitten, photorealistic, soft natural light, highly detailed',
    'ratio': '1:1',
    'counts': '1'
}, api_key=api_key)

task_id = (create.get('data') or {}).get('task_id')
for _ in range(24):
    r = skill.invoke('Task Result', {'task_id': task_id}, api_key=api_key)
    status = (r.get('data') or {}).get('status')
    if status in ('completed', 'succeeded', 'failed', 'timeout'):
        print(r)
        break
    time.sleep(5)
```

## 5. Quick Reference (Minimum Viable Params)

### 5.1 Query APIs
| API | Purpose | Minimum params |
|---|---|---|
| Credits | Query account credits | {} |
| Task Result | Query task status/result | {"task_id": "<task_id>"} |

### 5.2 Text To Image
| API | Minimum params |
|---|---|
| Imagen 4 | {"prompt": "<text prompt>"} |
| soul_character | {"prompt": "<text prompt>"} |

### 5.3 Image To Image
| API | Minimum params |
|---|---|
| Nano Banana | {"images": "<image_url>", "prompt": "<text prompt>"} |
| Seedream 4.0 | {"images": "<image_url>", "prompt": "<text prompt>"} |
| Nano Banana Pro | {"images": "<image_url>", "prompt": "<text prompt>"} |

### 5.4 Image To Video
| API | Minimum params |
|---|---|
| Wan 2.6 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Wan 2.2 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Hailuo 02 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Kling 2.1 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Vidu Q3 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Kling 2.5 Turbo | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Google Veo 3.1 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Kling 3.0 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Hailuo 2.3 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Vidu Q2 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Wan 2.5 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Kling 2.6 | {"image": "<image_url>", "prompt": "<text prompt>"} |
| Motion Control Kling 2.6 | {"video": "<prompt_or_value>", "image": "<image_url>"} |
| Google Veo 3.1 Fast | {"image": "<image_url>", "prompt": "<text prompt>"} |

### 5.5 Text To Video
| API | Minimum params |
|---|---|
| Wan 2.6 | {"prompt": "<text prompt>"} |
| Vidu Q3 | {"prompt": "<text prompt>"} |
| Wan 2.5 | {"prompt": "<text prompt>"} |

## 6. Reusable Helper Snippets

### 6.1 Unified submit + poll function
```python
import os
import time
from scripts.skill_router import Skill

skill = Skill('scripts/c_api_doc_detail.json')
api_key = os.getenv('API_KEY', '')

def submit_and_wait(api_name, params, retries=36, interval_sec=5):
    create = skill.invoke(api_name, params, api_key=api_key)
    task_id = (create.get('data') or {}).get('task_id')
    if not task_id:
        return {'stage': 'create', 'response': create}

    for _ in range(retries):
        r = skill.invoke('Task Result', {'task_id': task_id}, api_key=api_key)
        status = (r.get('data') or {}).get('status')
        if status in ('completed', 'succeeded', 'failed', 'timeout'):
            return {'stage': 'result', 'task_id': task_id, 'response': r}
        time.sleep(interval_sec)

    return {'stage': 'timeout', 'task_id': task_id}
```

### 6.2 Quick T2I call
```python
r = submit_and_wait('Imagen 4', {
    'prompt': 'A cute kitten, cinematic composition, soft daylight, ultra-detailed',
    'ratio': '1:1',
    'counts': '1'
})
print(r)
```

### 6.3 Quick I2V call
```python
r = submit_and_wait('Kling 3.0', {
    'image': 'https://example.com/input.jpg',
    'prompt': 'Slow camera push-in, stable subject, cinematic lighting',
    'duration': '5s',
    'resolution': '1080P'
})
print(r)
```

## 7. Troubleshooting Checklist

1. `code=374004`: verify that `API_KEY` is configured and valid.
2. `code=490505`: your account is out of credits; recharge before retrying.
3. `API not found`: ensure `api_name` exactly matches the `name` field in API definitions.
4. Task remains `processing`: increase polling retries or reduce duration/resolution.
5. Missing `task_id`: check required parameters and payload shape against this document.