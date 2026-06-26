---
name: Image Upscaler | 模糊图片变清晰 | 无损放大 AI
description: 专业 AI 图像增强工具：模糊变清晰、缩略图变清晰、2×/4× 无损放大。
---

# Image Upscaler | 模糊变清晰 | 无损放大 AI 技能

> [!IMPORTANT]
> **区域限制**: 中国大陆
> **API Key 获取**: 微信搜索小程序 **"无损放大 AI"** → 个人中心/API 管理 → 复制 `api_key`（格式：`pk_live_xxx`）

---

## 🚀 快速使用（3 步完成）

### 1️⃣ 提交图片任务

```bash
curl -X POST "https://supabase.00123.fun:22334/functions/v1/api-process-image" \
  -F "file=@/path/to/image.jpg" \
  -F "api_key=your_api_key"
```
**响应**: `{"result":"suc", "task_id":"..."}`

### 2️⃣ 轮询任务状态

```bash
curl -X POST "https://supabase.00123.fun:22334/functions/v1/api-get-task" \
  -H "Content-Type: application/json" \
  -d '{"api_key":"your_api_key", "task_id":"your_task_id"}'
```
**响应**: `{"result":"suc", "tasks":[{"status":"done", "processed_url":"..."}]}`

### 3️⃣ 状态码说明
- `pending` / `processing`: 排队或处理中（建议每 3 秒轮询一次）
- `done`: 成功，使用 `  ` 下载结果
- `failed` / `nsfw`: 失败或内容违规

---

## 🤖 AI 执行指南
1. **提交**: 使用 `api-process-image` 上传文件并拿取 `task_id`。
2. **轮询**: 每隔 5 秒调用 `api-get-task` 检查状态。
3. **完成**: 状态为 `done` 时返回 `processed_url`；若为 `failed`/`nsfw` 则提示失败。
