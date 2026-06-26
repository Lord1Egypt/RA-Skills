# AA（AnimateAnyone Gen2）API 参考

官方文档：
- 图像检测：https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api
- 动作模板生成：https://help.aliyun.com/zh/model-studio/animate-anyone-template-api
- 视频生成：https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api

## 重要说明
- **Region 固定为北京**：`dashscope.aliyuncs.com`，API Key 必须是北京地域的
- 全流程三步，Step 1 同步，Step 2/3 异步（轮询 task_id）

---

## 三步流水线

```
Step 1: aa-detect     (同步)  → check_pass=true / 否则报错
Step 2: aa-template   (异步)  → template_id
Step 3: aa-generate   (异步)  → video_url
```

---

## Step 1: 图像检测（同步）

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/aa-detect
```

| 字段 | 说明 |
|------|------|
| `model` | `animate-anyone-detect-gen2` |
| `input.image_url` | 公网 HTTP/HTTPS URL，jpg/jpeg/png/bmp，<5MB，最大边≤4096 |

响应：
```json
{
  "output": {
    "check_pass": true,
    "bodystyle": "full"  // "full"=全身, "half"=半身
  }
}
```

图片要求（检测通过条件）：
- 单人，正面或近似正面，无大角度侧身
- 面部清晰，无遮挡
- 全身或腰部以上完整露出
- 背景尽量简洁，无复杂遮挡

---

## Step 2: 动作模板生成（异步）

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/aa-template-generation/
Header: X-DashScope-Async: enable
```

| 字段 | 说明 |
|------|------|
| `model` | `animate-anyone-template-gen2` |
| `input.video_url` | 公网 URL，mp4/avi/mov，H.264/H.265，fps≥24，2~60s，≤200MB |

视频要求：
- 全身入镜，一镜到底，无场景切换
- 首帧正面朝镜头
- 人物从首帧开始出现

响应（轮询 `GET /api/v1/tasks/{task_id}`）：
```json
{
  "output": {
    "task_status": "SUCCEEDED",
    "template_id": "AACT.xxx.xxx-xxx.xxx"
  }
}
```

---

## Step 3: 视频生成（异步）

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/
Header: X-DashScope-Async: enable
```

| 字段 | 说明 |
|------|------|
| `model` | `animate-anyone-gen2` |
| `input.image_url` | 经 Step 1 检测通过的图片 URL |
| `input.template_id` | Step 2 得到的 template_id |
| `parameters.use_ref_img_bg` | `false`(默认，用视频背景) / `true`(用图片背景) |
| `parameters.video_ratio` | `"9:16"` 或 `"3:4"`（仅 use_ref_img_bg=true 时有效） |

响应（轮询）：
```json
{
  "output": {
    "task_status": "SUCCEEDED",
    "video_url": "https://xxx/output.mp4"
  }
}
```

> ⚠️ video_url 仅在任务完成后 **24小时内有效**，请及时下载。

---

## 输入格式转换（ffmpeg）

| 输入类型 | 不支持格式 | 转换目标 | 转换命令 |
|---------|----------|---------|---------|
| 图片 | webp, heic, tif, bmp | jpg | `ffmpeg -i input.webp -q:v 2 output.jpg` |
| 视频 | webm, mkv, flv, wmv | mp4 (H.264) | `ffmpeg -i input.webm -c:v libx264 -crf 22 -c:a aac output.mp4` |
| 视频 fps<24 | — | fps=24 | `ffmpeg -i input.mp4 -vf fps=24 -c:v libx264 output.mp4` |

脚本 `animate_anyone.py` 自动检测并转换，无需手动处理。

---

## 完整调用示例

```bash
# 本地文件（自动转换+上传 OSS）
python scripts/animate_anyone.py \
  --image ./portrait.jpg \
  --video ./dance.webm \
  --download --output result.mp4

# 已有 URL
python scripts/animate_anyone.py \
  --image-url "https://oss.../portrait.jpg?..." \
  --video-url "https://oss.../dance.mp4?..." \
  --download

# 已有 template_id（跳过 Step 2）
python scripts/animate_anyone.py \
  --image ./portrait.jpg \
  --template-id "AACT.xxx.xxx" \
  --download

# 以图片为背景生成
python scripts/animate_anyone.py \
  --image ./portrait.jpg --video ./dance.mp4 \
  --use-ref-img-bg --video-ratio 9:16 --download
```
