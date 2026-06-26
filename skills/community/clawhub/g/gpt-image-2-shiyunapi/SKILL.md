---
skill_id: gpt_image_2_shiyunapi
name: gpt-image-2-shiyunapi
display_name: GPT-image-2 图片生成与编辑 诗云API
tags: [图片, 文生图, 图生图, 图片生成, 图片编辑, AI绘图, AI修图, 局部重绘, 换背景, 多图合成, 诗云API, ShiyunApi, gpt-image-2]
description: 
  【功能】通过 GPT-image-2 模型完成文生图和基于图片的编辑/修图，通过诗云API(ShiyunApi)提供GPT-image-2 模型服务。
  【场景】用户要生成图片、画图、做海报/头像/封面/插画/产品图，或要修改图片、局部重绘、换背景、合成多张图、调整风格、基于参考图生成新图时触发。
  【输入】文本提示词；编辑场景还需要一张或多张待编辑图片；可选尺寸/数量/质量/格式/遮罩/背景/审核级别；ShiyunApi API Key。
  【输出】PNG/JPEG/WebP 图片文件，或保存原始 JSON 便于排错。
trigger:
  keywords: [诗云, 诗云API, ShiyunApi, shiyunapi, GPT-image-2, image-2, image2, gptimage2, gpt image 2, gpt-image-2, GPT Image, 文生图, 文本生成图片, AI绘图, AI作图, AI画图, 图片生成, 生成图片, 生成一张图, 做一张图, 设计一张图, 画一张图, 帮我画, 做个海报, 生成海报, 生成插画, 生成头像, 生成封面, 产品图, 电商图, 图生图, 图片编辑, 编辑图片, 修改图片, AI修图, 修图, 局部修改, 局部重绘, 遮罩, mask, 换背景, 去背景, 改背景, 合成图片, 多图合成, 参考图, 根据这张图, edit image, image-to-image, inpaint, outpaint, replace background, combine images, create image, generate image, text-to-image]
  intent: image.generate, text_to_image, image.edit, image_to_image, ai.draw, ai.retouch
  file_types: [png, jpg, jpeg, webp]
agent_created: true
---

# ShiyunApi GPT-image-2 图片生成与编辑

## 功能

通过诗云API / ShiyunApi 的 GPT-image-2 图片接口完成两类任务：

- 文生图：`POST https://shiyunapi.com/v1/images/generations`，由文本提示词生成全新图片。
- 图片编辑：`POST https://shiyunapi.com/v1/images/edits`，基于一张或多张输入图片进行修改、局部重绘、换背景、风格调整或合成。

核心判断：

- 用户只提供文字并要求“生成、画、做、设计一张新图片”时，走文生图流程，运行 `scripts/generate_image.py`。
- 用户提供或引用已有图片，并要求“修改、参考、合成、换背景、局部重绘、把这张图改成……”时，走图片编辑流程，运行 `scripts/edit_image.py`。
- 用户需求是视频、本地离线修图、截图、压缩、裁剪或其他供应商时，不使用本技能，除非用户明确要求切换到 ShiyunApi。

## 能力边界

支持：

- 中文/英文提示词文生图。
- 海报、头像、封面、插画、产品图、电商图、宣传图、概念图、角色设定图、场景图等新图片生成。
- 基于一张或多张 `png` / `jpg` / `jpeg` / `webp` 图片进行编辑。
- 换背景、保留主体、改变风格、多图合成、局部补全或重绘。
- 可选使用 `mask` 遮罩图进行局部编辑；完全透明区域表示需要编辑的位置。
- 指定模型、数量、尺寸、质量、输出格式、背景透明度、审核级别等参数。
- 保存 URL 图片、base64 图片或原始 JSON 响应。

不支持：

- 视频生成、图生视频、视频续写。
- 本地离线图片处理、截图、压缩、裁剪、无 API 的离线修图。
- 非 ShiyunApi 的图片供应商，除非用户明确要求改用 ShiyunApi。

## 执行流程

1. 判断任务类型：
   - 无输入图片且目标是创建新图：选择文生图。
   - 有输入图片、参考图、遮罩或“修改这张图”的目标：选择图片编辑。
2. 提取提示词；缺失时先询问用户想生成什么或如何修改图片。
3. 编辑场景提取待编辑图片路径；缺失时先询问用户提供图片文件。
4. 校验 API Key：优先读取 `SHIYUN_API_KEY`。
5. 用户直接提供 API Key 时，运行 `scripts/save_api_key.py --api-key-stdin` 持久化；通过 stdin 传入，不写入文档、日志或 memory。
6. 需要确认接口限制时读取 `references/api_docs.md`；需要示例时读取 `references/examples.md`；遇到失败时读取 `references/troubles.md`。
7. 根据任务类型运行对应脚本。
8. 检查输出：有图片则交付图片；只有 JSON 则说明响应结构和下一步。

## 参数

### 通用参数

- `prompt`：必填，图片生成或编辑提示词。
- `model`：可选，默认 `gpt-image-2`。
- `n`：可选，默认 `1`，范围 `1` 到 `10`。
- `size`：可选，默认 `1024x1024`；常用 `1024x1024`、`1536x1024`、`1024x1536`、`auto`。
- `quality`：可选，默认 `auto`；常用 `high`、`medium`、`low`、`auto`。
- `format`：可选，默认 `png`，用于保存图片，可为 `png` / `jpeg` / `webp`。
- `output_dir`：可选，默认应使用当前工作区下的任务专属目录。

### 文生图专用参数

- `model_field`：可选，默认 `model`；接口字段异常时可用 `modal` 或 `auto`。
- `format`：会作为 JSON 请求体字段传给接口。

### 图片编辑专用参数

- `image` / `images`：必填，待编辑图片路径，可传一张或多张。
- `mask`：可选，遮罩 PNG；透明区域表示要编辑的位置；应小于 4MB 且尺寸与第一张图片一致。
- `background`：可选，默认 `auto`，支持 `transparent`、`opaque`、`auto`。
- `moderation`：可选，默认 `auto`，支持 `low`、`auto`。
- `response_format`：可选，仅 `dall-e-2` 使用；`gpt-image-2` 默认按 base64/URL 响应解析，不要主动传该参数。

## 调用脚本

### 文生图

```bash
python "scripts/generate_image.py" \
  --prompt "一只穿宇航服的小龙虾，赛博朋克海报风格" \
  --model gpt-image-2 \
  --n 1 \
  --size 1024x1024 \
  --quality auto \
  --format png \
  --output-dir "C:/path/to/output"
```

### 编辑单张图片

```bash
python "scripts/edit_image.py" \
  --image "C:/path/to/input.png" \
  --prompt "保留主体，把背景改成雪山日出，真实摄影风格" \
  --model gpt-image-2 \
  --n 1 \
  --size 1024x1024 \
  --quality auto \
  --output-dir "C:/path/to/output"
```

### 编辑多张参考图并合成

```bash
python "scripts/edit_image.py" \
  --image "C:/path/to/person.png" \
  --image "C:/path/to/product.png" \
  --prompt "将人物和产品自然合成到同一张电商海报中，保留人物面部特征" \
  --model gpt-image-2 \
  --output-dir "C:/path/to/output"
```

### 局部编辑

```bash
python "scripts/edit_image.py" \
  --image "C:/path/to/input.png" \
  --mask "C:/path/to/mask.png" \
  --prompt "只修改透明遮罩区域，将天空改成晚霞" \
  --output-dir "C:/path/to/output"
```

### 保存用户提供的 API Key

```bash
python "scripts/save_api_key.py" --api-key-stdin
```

通过 stdin 传入 Key，避免把 Key 暴露在命令文本、日志或历史记录中。

## 脚本行为

`scripts/generate_image.py`：

- 发送 `POST https://shiyunapi.com/v1/images/generations`。
- 添加 `Content-Type: application/json`、`Accept: application/json`、`Authorization: Bearer <key>`。
- 校验 `prompt`、`n`、`quality`、`format`、`size`。
- 默认使用请求字段 `model`；必要时支持 `--model-field modal`。
- 使用 `--model-field auto` 时，仅在疑似参数校验失败后重试 alternate field；提醒用户重试可能消耗额度。

`scripts/edit_image.py`：

- 发送 `POST https://shiyunapi.com/v1/images/edits`。
- 添加 `Accept: application/json`、`Authorization: Bearer <key>`，请求体使用 `multipart/form-data`。
- 校验 `image`、`mask`、`prompt`、`n`、`size`、`quality`、`background`、`moderation`、`response_format`。
- 将每个 `--image` 作为 `image` 字段重复上传，兼容多图数组语义。

两个脚本都会：

- 遇到 `url` 字段时下载图片。
- 遇到 `b64_json`、`base64`、`image_base64` 字段时保存图片。
- 遇到未知结构时保存 `response.json`。
- 输出 `metadata.json` 记录接口、状态、原始响应路径和保存文件路径。

## 输出

成功时：

```json
{
  "code": 0,
  "files": ["C:/path/to/image_1.png"],
  "msg": "图片生成或编辑成功"
}
```

未返回图片但有响应时：

```json
{
  "code": 202,
  "raw_response": "C:/path/to/response.json",
  "msg": "已保存原始响应，请根据接口返回继续处理"
}
```

## 异常处理

- 未检测到 API Key：提示进入 `https://shiyunapi.com/console/token` 创建 Key，并设置 `SHIYUN_API_KEY`。
- `401` / `403`：提示检查 API Key 和 Bearer 授权格式。
- 余额/额度不足：提示进入 `https://shiyunapi.com/console/topup` 充值后重试。
- `400` / `422`：
  - 文生图优先检查 `prompt`、`model`/`modal`、`n`、`size`、`quality`、`format`。
  - 图片编辑优先检查图片格式/大小、`prompt`、`model`、`n`、`size`、`quality`、`mask`。
- `413`：提示图片文件过大；编辑场景单图应小于 25MB，遮罩应小于 4MB。
- 非 2xx：提取 `error`、`message`、`msg`、`code`、`detail` 后说明失败原因。
- 多次出现错误，但无法确定原因提示进入 `https://shiyunapi.com/customersupport` 联系客服寻求帮助。
- 未知响应：保存原始响应并总结 HTTP 状态，不暴露密钥。

## 已知接口文档问题

- 文生图文档 schema 写 `modal`，示例请求写 `model`；默认先用 `model`。
- 图片编辑文档中标题/标签/model 名称存在 GPT Image-1 与 GPT-image-2 混写；本合并技能默认使用 `gpt-image-2`。
- 响应示例可能是 chat completion 结构，不一定是真实图片生成/编辑结构。
- Header 表中 Authorization 标为可选，但实际按必填处理。

## 安全规则

- 不把 API Key 写入 `SKILL.md`、reference、memory 或项目文件。
- 优先使用 `SHIYUN_API_KEY`，避免用命令行 `--api-key`。
- 用户提供 Key 时，用 `save_api_key.py --api-key-stdin` 保存。
- 对日志、报错、总结中的 Authorization 和 Key 做脱敏。
- 未经用户明确要求，不把用户图片、生成结果或提示词上传到其他服务。
