# MinerU 精准解析 API —— 关键字段速查

来源：https://mineru.net/apiManage/docs （2026-11 核对）

## 限制

- 单文件：大小 ≤ 200MB，页数 ≤ 200 页。
- 每账号每天 1000 页「最高优先级」额度，超出部分降优先级。
- 批量申请上传链接：单次 ≤ 50 个；批量任务单 batch ≤ 200 个文件。
- 上传链接有效期 24 小时；上传完成后系统自动扫描并提交解析，无需调用提交接口。

## 接口

### 1) 批量申请上传链接（本地文件）
`POST https://mineru.net/api/v4/file-urls/batch`
Header: `Authorization: Bearer <token>`, `Content-Type: application/json`
Body:
```json
{
  "model_version": "vlm",
  "language": "ch",
  "enable_formula": true,
  "enable_table": true,
  "files": [{"name": "book__0001.pdf", "data_id": "book__0001", "is_ocr": false}]
}
```
返回：
```json
{"code":0,"data":{"batch_id":"...","file_urls":["https://..."]}}
```

### 2) 上传
`PUT <file_urls[i]>`，body 为文件二进制。**不要设置 Content-Type 头。**
（curl 示例：`curl -X PUT -T /path/file.pdf '<url>'`）

### 3) 轮询批量结果
`GET https://mineru.net/api/v4/extract-results/batch/{batch_id}`
Header: `Authorization: Bearer <token>`
返回 `data.extract_result` 列表，每项含：
`file_name`, `state`(pending/running/converting/done/failed), `full_zip_url`, `err_msg`, 可能含 `data_id`。

### 4) 单个文件任务（URL 方式，备用）
`POST /api/v4/extract/task` body `{"url":"...","model_version":"vlm"}`
`GET /api/v4/extract/task/{task_id}`

## 结果 zip 内容

- `full.md`：Markdown 解析结果。
- `images/`：图片资源（md 中以 `images/xxx.jpg` 相对路径引用）。
- 其他：`*_content_list.json`、`*_middle.json`、`*_model.json` 等。

## 参数

- `model_version`: `pipeline`(默认) / `vlm`(推荐) / `MinerU-HTML`（仅 html）
- `is_ocr`: 是否启用 OCR（默认 false），扫描件需 true
- `enable_formula` / `enable_table`: 默认 true
- `language`: 默认 `ch`
- `page_ranges`: 页码范围，如 `1-200`（单文件任务/URL 批量可用）
- `data_id`: 自定义业务 ID（字母/数字/_ - .，≤128 字符）

## 状态码

- `code == 0` 表示成功；否则读 `msg`。
