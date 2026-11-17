# 可购物视频大文件分片上传方案（Shoppable Video Large File Upload）

- **来源文档**：[Shoppable Video Large File Upload Solution（Lark）](https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d)
- **Partner Center**：[shoppable-video-large-file-upload](https://partner.tiktokshop.com/docv2/page/shoppable-video-large-file-upload)（需登录）
- **适用场景**：可购物视频文件 **> 10MB**（≤ 10MB 仍可用 §4 直传 `video_files`）
- **替代关系**：取代旧版「请求头特殊参数」大文件方案；旧方案已于 **2026-01-31** 停止支持

## 方案概述

通过 **文件网关分片上传（chunked upload via file gateway）**：

1. 客户端将 **> 10MB** 的文件按 chunk 切分；
2. 携带 `upload_token` **顺序**上传各分片至 `upload_url`；
3. 服务端合并分片还原原文件；
4. **Bind Business Resource** 将文件绑定到可购物视频业务资源，得到与直传等价的 `file_id`。

≤ 10MB 的文件继续使用 **Upload Shoppable Video File**（`POST .../videos/video_files`）。

## 三步流程

```
Step 1  Initialize Upload     →  upload_url + upload_token
Step 2  Upload Chunks & Merge →  PUT 分片至 upload_url（不经 LinkFox 网关）
Step 3  Bind Business Resource →  file_id（供后续发布；可选预检）
```

| 步骤 | 调用方 | 经 LinkFox `/tiktokVideo/developerProxy` |
|------|--------|------------------------------------------|
| 1 Initialize | JSON POST | **可能**（path 须白名单放行，见下） |
| 2 Upload Chunks | 二进制 PUT | **否** — 直连 Step 1 返回的 `upload_url` |
| 3 Bind | JSON POST | **可能**（同 Step 1 路径前缀约束） |

---

## Step 1：初始化上传（Initialize Upload）

获取分片上传所需的 `upload_url` 与 `upload_token`。

| 项 | 说明 |
|----|------|
| Method | `POST` |
| 上游 Path | `/open/{version}/file/init`（`:version` 如 `202505`，**以 Lark / Partner 文档为准**） |
| 经 proxy 的 path 示例 | `open/202505/file/init` |

### Query 参数（紫鸟自动注入）

| 参数 | 说明 |
|------|------|
| access_token | 即 creator `access_token` / `ttsAccessToken` |
| app_key | 紫鸟注入 |
| timestamp | 紫鸟注入 |
| sign | 紫鸟注入 |

### 请求体（JSON）

> Lark 文档中 Request Body 字段需以官方最新版为准。常见初始化字段如下（**调用前请对照 Lark 核对**）：

| 字段 | 类型 | 说明 |
|------|------|------|
| file_size | int64 | 文件总字节数 |
| chunk_size | int64 | 分片大小（字节） |
| file_name | string | 文件名（如 `video.mp4`） |
| content_type | string | MIME，如 `video/mp4` |

### 成功响应

```json
{
  "upload_url": "{uploader_url}",
  "upload_token": "{your_unique_upload_token}"
}
```

| 字段 | 说明 |
|------|------|
| upload_url | 分片上传目标 URL（Step 2 使用，**完整 URL 含 query**） |
| upload_token | 本次上传会话 token（Step 2/3 使用） |

---

## Step 2：上传分片并合并（Upload Chunks & Merge）

将视频二进制 **顺序** PUT 到 Step 1 返回的 **`upload_url`**（文件网关域名，**不经过** LinkFox 网关）。

### 请求要点

| Header | 说明 |
|--------|------|
| Content-Type | 视频 MIME，如 `video/mp4` |
| Content-Length | **当前分片**字节长度 |
| Content-Range | `bytes {first}-{last}/{total}` |

### 分片规则（参考 TikTok 媒体传输惯例，与 Lark 一致方向）

| 规则 | 说明 |
|------|------|
| 顺序 | 分片须 **按序** 上传 |
| 分片大小 | 单分片建议 **5MB ~ 64MB**；最后一片可含剩余字节（可略大于 chunk_size） |
| 小文件 | 总大小 < 5MB 时通常整文件一片上传 |
| 分片数量 | 最少 1 片，最多约 **1000** 片 |
| chunk 计算 | `total_chunk_count = floor(file_size / chunk_size)`，末片包含余数 |

### PUT 示例（单片 / 末片）

```bash
curl --location --request PUT '{upload_url}' \
  --header 'Content-Type: video/mp4' \
  --header 'Content-Range: bytes 0-9999999/50000000' \
  --header 'Content-Length: 10000000' \
  --data-binary '@/path/to/chunk.bin'
```

> 使用 Step 1 返回的 **完整** `upload_url`（含 query 参数）。上传完成后由文件网关 **自动合并** 分片。

---

## Step 3：绑定业务资源（Bind Business Resource）

将已合并的文件绑定到 **可购物视频（Shoppable Video）** 业务资源，取得与直传 `video_files` 等价的 **`file_id`**（`data.video_file.id`）。

| 项 | 说明 |
|----|------|
| Method | `POST` |
| 上游 Path | `/open/{version}/file/bind`（**path 名称以 Lark Step 3 为准**，也可能是 `complete` / `commit` 等） |
| 经 proxy 的 path 示例 | `open/202505/file/bind` |

### 请求体（JSON，字段以 Lark 为准）

| 字段 | 类型 | 说明 |
|------|------|------|
| upload_token | string | Step 1 返回的 `upload_token` |
| resource_type / biz_type | string | 业务资源类型（可购物视频场景，见官方枚举） |

### 成功响应（结构以官方为准）

预期返回可购物视频文件 id，供后续 **Post Shoppable Video / Pre-check** 使用：

```json
{
  "code": 0,
  "data": {
    "video_file": {
      "id": "123123123123",
      "md5": "..."
    }
  },
  "message": "success"
}
```

---

## LinkFox 集成现状

### 路径白名单

当前 `tiktok-video.developer-proxy.allowed-path-prefixes` 仅含：

- `affiliate_creator`
- `video`
- `creator`

Step 1 / Step 3 文档路径为 **`open/{version}/file/...`**，**不在现网白名单内**，经 `/tiktokVideo/developerProxy` 调用会返回 **errcode 1005**。需后端扩展白名单或确认紫鸟映射后的 `affiliate_creator/...` 等价 path 后再启用脚本。

### 脚本支持

| 脚本 | 状态 |
|------|------|
| `large_file_upload.py --help` | 流程说明 |
| `large_file_upload_init.py` | 文档入口（暂不可实际调用） |
| `large_file_upload_bind.py` | 文档入口（暂不可实际调用） |
| Step 2 分片 PUT | 须客户端直连 `upload_url`，暂无 skill 封装 |

---

## 与直传方案的选择

| 文件大小 | 推荐方案 |
|----------|----------|
| ≤ 10MB | §4 `upload_shoppable_video_file`（multipart 直传，网关 multipart 待支持） |
| > 10MB | 本节大文件分片三步流程 |

## 在发布链路中的位置

```
选品 → [大文件分片上传 或 直传] → file_id → （可选）预检 → 发布 → 查状态
```

> 选品请使用 **`linkfox-tiktok-video-products`**。预检为可选步骤；上传获得 `file_id` 后可直接发布。
