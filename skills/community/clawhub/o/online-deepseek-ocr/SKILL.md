# Online DeepSeek OCR Skill

使用 SiliconFlow 免费的 DeepSeek-OCR 模型进行云端 OCR 识别。

## 功能

- 支持 PNG、JPG、JPEG、WEBP 格式
- 支持多语言
- 免费使用 SiliconFlow API
- OCR 前图像预处理：智能缩放、去噪、灰度转换、对比度增强、锐化、二值化

## 使用

```bash
online-deepseek-ocr <image_path_or_url> [--json]
```

示例：
```bash
online-deepseek-ocr test/image.png
online-deepseek-ocr https://example.com/screenshot.png --json
```

## 输出格式

```json
{
  "success": true,
  "text": "识别的完整文本",
  "engine": "deepseek-ocr",
  "model": "deepseek-ai/DeepSeek-OCR",
  "usage": {
    "prompt_tokens": 701,
    "completion_tokens": 304,
    "total_tokens": 1005
  }
}
```

## 限制

- 图片大小不超过 10MB
- 免费 API 有速率限制
- 需要网络连接
- 预处理功能需要安装 Pillow 和 numpy 库

## 安装依赖

```bash
cd skills/online-deepseek-ocr
pip install -r requirements.txt
```

## 快速开始

1. 获取 SiliconFlow API key（访问 https://siliconflow.cn）
2. 在技能目录下创建 `config.json`，填入 API key：
   ```bash
   cd skills/online-deepseek-ocr
   echo '{"apiKey": "your-api-key-here"}' > config.json
   ```
3. 运行 OCR：
   ```bash
   online-deepseek-ocr your-image.png
   ```

## 故障排除

- 配置文件不存在：创建 `skills/online-deepseek-ocr/config.json`
- 未找到 API key：确保 config.json 中的 apiKey 字段已填写且不为空
- 安装依赖失败：运行 `pip install -r requirements.txt`
- 图像预处理失败：检查 Pillow 和 numpy 是否正确安装
- API 认证失败：检查 API key 是否正确，是否已过期
