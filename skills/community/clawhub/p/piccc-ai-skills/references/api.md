# Piccc AI 媒体接口

## 连接账号

首次使用时运行：

```bash
node scripts/piccc.mjs auth login
```

命令会自动打开授权页面。登录 Piccc AI（皮可AI）并确认授权后，页面会跳转到本机回调页，脚本随后自动创建并保存 API 密钥、查询当前可用积分。命令会一直等待授权结果，不要让用户在对话中发送密钥，也不要要求用户另行回复“已完成”。浏览器无法打开时，使用命令显示的链接和验证码；`auth login --no-browser` 可保留纯手动流程。

## 模型接口

| 类型 | 接口 | 主要能力字段 |
| --- | --- | --- |
| 图片 | `GET /v1/images/models` | 比例、分辨率、质量、生成数量 |
| 视频 | `GET /v1/videos/models` | 分辨率、比例、时长、生成模式、参考模式 |
| 音频 | `GET /v1/audio/models` | 格式、采样率、参数范围、参考模式、音色 |

每次创建任务前使用模型响应中的 `data[].id`。音色使用 `voice_presets[].id`，不要传显示名称。

## 经济规格

默认先运行：

```bash
node scripts/piccc.mjs models image --economy
```

将 `image` 换成 `video` 或 `audio`。命令会返回推荐模型、`defaults`、`special_offer` 和 `warning`。

- 用户没有指定时，使用 `defaults` 中的低分辨率、低质量、单个输出、最短视频时长和低采样率。
- 默认关闭视频音频、联网搜索和不必要的参考素材。
- 用户明确要求高清、高质量、更长时长或指定模型时，以用户要求为准。
- `special_offer=true` 时，创建任务前提示：“特价模型可能生成较慢、稳定性较差。”
- 即使没有运行 `--economy`，生成脚本也会为未传参数补上当前模型支持的经济规格。

## 创建任务

图片：`POST /v1/images/tasks`

- 必填：`model`、`prompt`
- 可选：`aspect_ratio`、`resolution`、`quality`、`n`、`web_search`、`external_id`

视频：`POST /v1/videos/tasks`

- 必填：`model`、`prompt`
- 可选：`route_mode`、`reference_mode`、`resolution`、`aspect_ratio`、`duration_seconds`、`audio`、`web_search`、`external_id`

音频：`POST /v1/audio/tasks`

- 必填：`model`、`prompt`
- 可选：`output_format`、`sample_rate`、`speech_rate`、`loudness_rate`、`pitch_rate`、`reference_mode`、`voice_id`、`audio_references`、`image_references`、`external_id`
- `reference_mode=audio` 时传 `voice_id` 或 `audio_references`
- `reference_mode=image` 时传 `image_references`
- 提交时预扣 10 积分，完成后的 `actual_cost` 是最终费用

## 查询任务

- `GET /v1/tasks/{task_id}`：查询单个图片、视频或音频任务。
- `GET /v1/tasks`：分页查询任务，可按 `type` 和 `status` 过滤。

任务状态包括 `queued`、`running`、`completed`、`failed`、`cancelled`。只有 `completed` 状态下的 `outputs[].url` 才是最终结果。
