# ShiyunApi GPT-Image-2 图片接口排错

## 未检测到 API Key

现象：脚本提示缺少 `SHIYUN_API_KEY`。

处理：

1. 提示用户前往 `https://shiyunapi.com/console/token` 创建 API Key。
2. 如果用户在对话中提供 Key，使用 `scripts/save_api_key.py --api-key-stdin` 保存。
3. 不要把 Key 写入 SKILL.md、reference、memory、日志或项目文件。

## 401 / 403

现象：接口返回认证或权限错误。

处理：

1. 检查 Key 是否正确。
2. 检查请求头是否为 `Authorization: Bearer <key>`。
3. 提醒用户重新生成 Key 后再试。

## 余额或额度不足

现象：错误信息包含余额不足、quota、billing、充值、欠费等含义。

处理：提示用户进入 `https://shiyunapi.com/console/topup` 充值后重试。

## 文生图 400 / 422 参数错误

优先检查：

- `prompt` 是否为空或超过 1000 字符。
- `model` / `modal` 字段是否符合接口实际要求。
- `n`、`size`、`quality`、`format` 是否在接口允许范围内。

如错误疑似由 `model` / `modal` 字段导致，可考虑 `--model-field auto`，但先提醒用户重试可能消耗额度。

## 图片编辑 400 / 422 参数错误

优先检查：

- `image` 是否存在，是否为 `png`、`jpg`、`jpeg` 或 `webp`。
- 单张图片是否小于 25MB。
- `mask` 是否为 PNG、是否小于 4MB、尺寸是否与第一张图片相同。
- `prompt` 是否为空或超过模型限制。
- `model`、`n`、`size`、`quality`、`background`、`moderation` 是否在接口允许范围内。
- 使用 `gpt-image-2` 时是否误传了 `response_format`。

## 413 文件过大

现象：接口拒绝上传，或返回 payload/file too large。

处理：

1. 降低输入图片大小。
2. 确保每张输入图小于 25MB。
3. 确保遮罩 PNG 小于 4MB。
4. 不要在本技能中直接删除或覆盖用户原图；如需压缩/转换，应先征得用户确认并保留备份。

## 返回结构不是图片

现象：接口返回 JSON，但没有 `url`、`b64_json`、`base64`、`image_base64` 等可识别图片字段。

处理：

1. 保存 `response.json`。
2. 摘要 HTTP 状态和可见错误字段。
3. 不暴露 Authorization 或 API Key。
4. 必要时读取 `references/api_docs.md` 对照接口文档。

## 文档字段不一致

现象：文生图接口对 `model` 或 `modal` 报错。

处理：

1. 默认先用 `--model-field model`。
2. 若返回字段缺失/非法，可在用户知晓可能重复计费后使用 `--model-field auto`。
3. 若 `auto` 仍失败，保存原始响应并按响应中的字段提示调整。

## 默认模型混写问题

现象：旧文档或旧脚本中出现 `gpt-image-1`。

处理：

- 本合并 skill 以用户要求为准，默认使用 `gpt-image-2`。
- 仅在接口明确返回模型不支持时，才提示用户确认是否切换模型。

## 其他错误

现象：多次出现错误，但无法确定原因。

处理：
- 提示进入 `https://shiyunapi.com/customersupport` 联系客服寻求帮助。