---
name: image-generator-custom
description: 调用第三方图像生成API生成图片；当用户需要通过自定义服务商API生成图像时使用
dependency:
  python:
    - Pillow>=10.0.0
---

# 图像生成器

## 任务目标
- 本 Skill 用于：通过调用第三方图像生成 API 生成图片
- 能力包含：支持 OpenAI 兼容格式 API、自定义服务商配置、参数化图像生成
- 触发条件：用户需要使用特定服务商的 API 生成图像

## 前置准备
- 消费者变量配置：
  在使用前，必须配置以下消费者变量（环境变量）：
  ```bash
  export IMAGE_API_URL="https://your-api-provider.com/v1/images/generations"
  export IMAGE_API_KEY="your-api-key-here"
  export IMAGE_MODEL_ID="your-model-id"
  ```
  
  说明：
  - `IMAGE_API_URL`: 图像生成 API 的完整 URL（需遵循 OpenAI 图像生成接口格式）
  - `IMAGE_API_KEY`: API 认证密钥
  - `IMAGE_MODEL_ID`: 模型 ID（可选，如果未设置则需要通过 --model 参数提供）

- 依赖说明：
  ```
  Pillow>=10.0.0
  coze_workload_identity  # 系统预装，包含 requests 库
  ```

## 操作步骤
- 标准流程：
  1. **配置消费者变量**：设置 `IMAGE_API_URL`、`IMAGE_API_KEY` 和 `IMAGE_MODEL_ID`
  2. **构建提示词**：准备描述图像的提示词
  3. **调用脚本**：执行 `python scripts/image_generator.py` 传递参数
  4. **查看结果**：检查生成的图片文件

- 调用方式（使用环境变量中的模型ID）：
  ```bash
  python scripts/image_generator.py \
    --prompt "一只可爱的猫咪" \
    --size "1024x1024" \
    --n 1
  ```

- 调用方式（覆盖模型ID）：
  ```bash
  python scripts/image_generator.py \
    --prompt "一只可爱的猫咪" \
    --model "override-model-id" \
    --size "1024x1024" \
    --n 1
  ```

## 资源索引
- 必要脚本：见 [scripts/image_generator.py](scripts/image_generator.py)（调用第三方图像生成 API）

## 参数说明

### 必需参数
- `--prompt`: 提示词，描述要生成的图像内容

### 可选参数
- `--model`: 模型名称（默认：使用消费者变量 `IMAGE_MODEL_ID`，如果消费者变量未设置则由 API 服务商决定）
- `--size`: 图片尺寸（默认：1024x1024，常见值：256x256, 512x512, 1024x1024, 1792x1024）
- `--n`: 生成数量（默认：1，范围：1-10）
- `--quality`: 图像质量（默认：standard，可选值：standard, hd）
- `--output`: 输出文件名前缀（默认：auto-generated）

## API 兼容性说明

本脚本假设第三方 API 遵循 OpenAI 图像生成接口格式：

### 请求格式
- **方法**: POST
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {API_KEY}
- **请求体**:
  ```json
  {
    "model": "model-name",
    "prompt": "image description",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard"
  }
  ```

### 响应格式
- **成功响应**:
  ```json
  {
    "data": [
      {
        "b64_json": "base64-encoded-image-data"
      }
    ]
  }
  ```
  或
  ```json
  {
    "data": [
      {
        "url": "https://example.com/image.png"
      }
    ]
  }
  ```

### 支持的服务商示例
- OpenAI DALL-E: `https://api.openai.com/v1/images/generations`
- Azure OpenAI: `https://your-resource.openai.azure.com/openai/deployments/your-deployment/images/generations?api-version=2023-06-01-preview`
- 其他兼容 OpenAI 格式的 API 服务商

## 注意事项
- 使用前必须正确配置消费者变量，否则脚本会报错
- 确保 API 服务商支持 OpenAI 图像生成接口格式
- 不同服务商支持的模型和参数可能不同，请参考服务商文档
- 生成的图片默认保存在当前目录下
- 如果 API 返回 URL 格式，脚本会自动下载并保存为 PNG 文件

## 使用示例

### 示例1：基础用法
```bash
python scripts/image_generator.py \
  --prompt "一只穿着宇航服的猫在月球上"
```

### 示例2：使用消费者变量中的模型ID
```bash
python scripts/image_generator.py \
  --prompt "赛博朋克风格的未来城市" \
  --size "1024x1024"
```

### 示例3：覆盖模型ID
```bash
python scripts/image_generator.py \
  --prompt "赛博朋克风格的未来城市" \
  --model "dall-e-3" \
  --size "1024x1024"
```

### 示例4：生成多张图片
```bash
python scripts/image_generator.py \
  --prompt "各种风格的山水画" \
  --size "1024x1024" \
  --n 4
```

### 示例5：高质量生成
```bash
python scripts/image_generator.py \
  --prompt "梦幻森林中的精灵城堡" \
  --size "1792x1024" \
  --quality "hd" \
  --n 1
```

### 示例6：自定义输出文件名
```bash
python scripts/image_generator.py \
  --prompt "写实风格的人像" \
  --output "portrait"
```

## 常见问题

### Q: 如何知道我的 API_URL 是什么？
A: 请咨询你的 API 服务商，确认图像生成接口的完整 URL。OpenAI DALL-E 的 URL 是 `https://api.openai.com/v1/images/generations`

### Q: 支持哪些模型？
A: 模型名称取决于你的 API 服务商。你可以通过消费者变量 `IMAGE_MODEL_ID` 设置默认模型，或通过 `--model` 参数指定。常见的有：dall-e-2、dall-e-3、stable-diffusion 等

### Q: 如何获取 API_KEY？
A: 请访问你的 API 服务商的控制台，在 API Keys 或类似的页面创建新的密钥

### Q: 脚本支持哪些图片尺寸？
A: 支持的尺寸取决于你的 API 服务商。常见的有：256x256、512x512、1024x1024、1792x1024 等

### Q: 为什么脚本报错"缺少环境变量"？
A: 请确保已正确配置消费者变量 IMAGE_API_URL 和 IMAGE_API_KEY。IMAGE_MODEL_ID 是可选的，如果未设置可以通过 --model 参数提供

### Q: 支持非 OpenAI 格式的 API 吗？
A: 目前仅支持 OpenAI 兼容格式的 API。如果需要支持其他格式，需要修改脚本

## 错误处理

脚本在以下情况会报错：
- 消费者变量 IMAGE_API_URL 未设置
- 消费者变量 IMAGE_API_KEY 未设置
- API 调用失败（网络错误、认证失败等）
- API 返回格式不符合预期
- 无法下载图片（当 API 返回 URL 时）
- 无法保存图片到文件

遇到错误时，请检查：
1. 消费者变量是否正确配置
2. API_URL 和 API_KEY 是否有效
3. API 服务商是否正常运行
4. 参数是否符合服务商要求
