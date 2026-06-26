# 图片上传

## 工具：`get_upload_url`

获取对象存储预签名上传 URL，Agent 用此 URL 直接 PUT 文件到 COS，再把返回的 `cdn_url` 作为 `record_tool` 的 `image_url` 入参。

## 流程

1. 调用 `get_upload_url`，传入文件名和 MIME 类型
2. 使用 `scripts/put-upload.js` 执行 HTTP PUT 上传文件
3. 检查 HTTP 响应：**2xx 视为成功**，非 2xx / 超时 → 重新 `get_upload_url` 换新凭证（不要重试旧 URL）
4. 上传成功后，`cdn_url` 作为 `record_tool` 的 `image_url` 传入

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `filename` | string | 是 | 文件名含扩展名，如 `lunch.jpg` |
| `content_type` | string | 是 | MIME 类型：`image/jpeg` / `image/png` / `image/webp` / `image/heic`（全部小写） |

## 返回值

| 字段 | 说明 |
|---|---|
| `upload_url` | 预签名 PUT URL，有效期 10 分钟 |
| `cdn_url` | CDN 访问 URL，上传成功后传给 `record_tool` 的 `image_url` |
| `method` | 固定为 `PUT` |
| `headers` | 上传时需要设置的 HTTP headers（按实际返回设置，通常含 `Content-Type`） |
| `expires_in` | URL 有效期（秒） |
| `max_size` | 最大文件大小（字节，10 MB） |

## 调用示例

exec 方式：

```bash
node {baseDir}/scripts/mcp-call.js get_upload_url '{"filename":"lunch.jpg","content_type":"image/jpeg"}'
```

PUT 上传：

```bash
node {baseDir}/scripts/put-upload.js --file='<local_image_path>' --upload-url='<upload_url>' --content-type='image/jpeg'
```

可选参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `--file` | string | 是 | 源图片文件路径 |
| `--upload-url` | string | 是 | `get_upload_url` 返回的预签名 PUT URL |
| `--content-type` | string | 否 | MIME 类型；如未通过 `--headers` 传入 `Content-Type`，脚本会自动补上 |
| `--headers` | string | 否 | JSON object 字符串，透传上传需要的 headers |
| `--tmp-dir` | string | 否 | 固定目录；默认读取 `KEEP_UPLOAD_TMP_DIR`，否则使用 `~/.keepai/tmp` |
| `--keep-staged-file` | flag | 否 | 保留复制后的临时文件，便于排查上传问题 |

如果 `--file` 指向的路径不存在，脚本会按文件名继续在以下目录中依次探测：

- 原始路径所在目录
- 固定目录（默认 `~/.keepai/tmp`）
- `/tmp`
- `/var/tmp`

## 注意事项

- **URL 有效期 10 分钟**：过期或 PUT 非 2xx 需重新 `get_upload_url`，不要重试旧 URL
- **Agent 禁止**：不要把 `upload_url` 展示给用户——这是短期预签名凭证，直接在本会话里完成 PUT
- **固定临时目录**：`scripts/put-upload.js` 会先把源图片复制到固定临时目录，再执行 PUT，默认目录为 `~/.keepai/tmp`；可通过环境变量 `KEEP_UPLOAD_TMP_DIR` 或参数 `--tmp-dir` 覆盖，避免依赖不稳定的 `/tmp`
- **文件探测兜底**：如果执行器传入的临时文件路径失效，脚本会按文件名在固定目录和常见临时目录中继续查找；成功命中后仍会复制到固定临时目录再上传

## 上传相关错误码

| 错误码 | 含义 | Agent 行为 |
|---|---|---|
| `MEDIA_TOO_LARGE` | 图片超过 10 MB 上限 | 提示用户压缩后重试 |
| `MEDIA_TYPE_NOT_ALLOWED` | 不支持的 MIME 类型 | 提示支持 jpeg / png / webp / heic |
| HTTP 4xx / 5xx（PUT 阶段） | 预签名 URL 失效或对象存储异常 | 重新 `get_upload_url` 拿新凭证；不要重试旧 URL |
