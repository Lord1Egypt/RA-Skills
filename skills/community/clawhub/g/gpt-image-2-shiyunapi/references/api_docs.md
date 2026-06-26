# ShiyunApi GPT-Image-2 图片接口参考

## 文档来源

- 文生图：`https://shiyunapi.apifox.cn/api-448504710`
- 图片编辑：`https://shiyunapi.apifox.cn/api-448504709`

## 通用信息

- Base URL: `https://shiyunapi.com`
- Authentication: Bearer Token
- API Key 创建地址：`https://shiyunapi.com/console/token`
- 充值地址：`https://shiyunapi.com/console/topup`

```http
Authorization: Bearer <SHIYUN_API_KEY>
Accept: application/json
```

公共文档中 Header 表可能把 `Authorization` 标为可选，但全局 bearer security 已声明。默认按必填处理。

用户提供 API Key 时，使用：

```bash
python "scripts/save_api_key.py" --api-key-stdin
```

通过 stdin 传入 Key，不要将 Key 写入 Markdown、memory、日志或报告。

## 文生图接口

- Path: `/v1/images/generations`
- Method: `POST`
- Full URL: `https://shiyunapi.com/v1/images/generations`
- Content-Type: `application/json`

### 请求字段

| Field | Type | Required | Notes |
|---|---|---:|---|
| `prompt` | string | yes | 图片提示词，文档最大 1000 字符。 |
| `model` | string | example yes | 文档示例使用 `model: gpt-image-2`；默认优先使用。 |
| `modal` | string | schema yes | 文档 schema 写 `modal`；当 `model` 报字段错误时可切换。 |
| `n` | integer | yes | 生成数量，1 到 10。 |
| `size` | string | no | 尺寸，见下方。 |
| `format` | string | no | `png`、`jpeg` 或 `webp`。 |
| `quality` | string | no | `low`、`medium`、`high` 或 `auto`。 |

### 尺寸约束

文档示例值：

- `1024x1024`
- `1536x1024`
- `1024x1536`
- `2048x2048`
- `2048x1152`
- `3840x2160`
- `2160x3840`
- `auto`

严格约束：

1. 最大边长 `<= 3840px`。
2. 宽高必须都是 `16px` 的倍数。
3. 长边 / 短边比例 `<= 3:1`。
4. 总像素在 `655360` 到 `8294400` 之间。

### 示例请求

```json
{
  "model": "gpt-image-2",
  "prompt": "A childrens book drawing of a veterinarian using a stethoscope to listen to the heartbeat of a baby otter.",
  "n": 1,
  "size": "1024x1024",
  "quality": "low",
  "format": "jpeg"
}
```

如遇字段校验异常，可尝试 schema-strict variant：

```json
{
  "modal": "gpt-image-2",
  "prompt": "A childrens book drawing of a veterinarian using a stethoscope to listen to the heartbeat of a baby otter.",
  "n": 1,
  "size": "1024x1024",
  "quality": "low",
  "format": "jpeg"
}
```

## 图片编辑接口

- Path: `/v1/images/edits`
- Method: `POST`
- Full URL: `https://shiyunapi.com/v1/images/edits`
- Content-Type: `multipart/form-data`

### 请求字段

| Field | Type | Required | Notes |
|---|---|---:|---|
| `image` | binary file or repeated binary files | yes | 待编辑图片。GPT 图像模型可用 `png`、`webp`、`jpg`、`jpeg`，单图建议小于 25MB。 |
| `prompt` | string | yes | 编辑提示词。GPT 图像模型文档最大 32000 字符。 |
| `mask` | binary file | no | PNG 遮罩。完全透明区域表示需要编辑的位置；小于 4MB，尺寸与第一张图一致。 |
| `model` | string | no | 默认 `gpt-image-2`。 |
| `n` | string/integer | no | 数量，1 到 10。 |
| `quality` | string | no | `auto`、`high`、`medium`、`low`；默认 `auto`。 |
| `response_format` | string | no | `url` 或 `b64_json`；仅 `dall-e-2` 使用，GPT 图像模型不要主动传。 |
| `size` | string | no | 常用 `1024x1024`、`1536x1024`、`1024x1536` 或 `auto`。 |
| `background` | string | no | `transparent`、`opaque` 或 `auto`。 |
| `moderation` | string | no | `low` 或 `auto`。 |

### 示例请求

```bash
curl -X POST "https://shiyunapi.com/v1/images/edits" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "image=@/path/to/image.png" \
  -F "prompt=将背景换成雪山日出，保留主体" \
  -F "model=gpt-image-2" \
  -F "n=1" \
  -F "size=1024x1024"
```

多图合成可重复 `image` 字段：

```bash
curl -X POST "https://shiyunapi.com/v1/images/edits" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "image=@/path/to/person.png" \
  -F "image=@/path/to/product.png" \
  -F "prompt=将人物和产品合并在一张图片里面" \
  -F "model=gpt-image-2"
```

## 响应解析

文档中的 200 响应示例看起来是 chat completion 结构，可能不是真实图片输出。真实输出可能包含：

- `data[].url`
- `data[].b64_json`
- `base64`
- `image_base64`
- `images`
- `result` / `results` / `output` / `outputs`

脚本会尽量解析上述字段并保存图片；无法识别时保存 `response.json`。

## 错误处理

- 非 2xx HTTP 状态视为失败。
- 优先解析 `error`、`message`、`msg`、`code`、`detail`。
- `401` / `403`：检查 bearer token 和 API Key。
- `400` / `422`：检查字段名、模型名、图片格式、提示词长度和参数范围。
- `413`：输入图片或遮罩过大。
- 余额/额度错误：引导到 `https://shiyunapi.com/console/topup`。

余额相关关键词：`余额不足`、`额度不足`、`欠费`、`充值`、`insufficient balance`、`insufficient quota`、`quota exceeded`、`billing`、`payment required`、`top up`。

## 已知文档不一致

- 文生图 schema 写 `modal`，示例写 `model`。
- 图片编辑文档标题、标签和参数说明存在 GPT Image-1 / GPT-Image-2 混写；本 skill 默认使用 `gpt-image-2`。
- 响应示例可能不是图片接口真实结构。
- Authorization 可选性与 bearer security 声明冲突。
