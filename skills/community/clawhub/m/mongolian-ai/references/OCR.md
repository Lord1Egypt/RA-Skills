# 图片 OCR

POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/ocr

上传使用 multipart/form-data；恰好一个 file 或 image_base64，两者互斥，解码后最大 5 MB，格式 JPG/JPEG/PNG/BMP/WebP/TIFF。Base64 不带 Data URL 前缀；也可通过 JSON 提交 image_base64。平台验证真实 MIME、图片尺寸及像素预算，不接受图片 URL。language 可选，支持 mw/mn/zh/en，默认 mn。成功只提取 data.text。

用户只要识别时直接展示原文；要求识别后翻译时将已识别文字送至 /translation，先确认文字方向。保存首次返回的内容，重放响应不包含识别正文。
