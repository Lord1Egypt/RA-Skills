# 大模型工具

一个功能强大的 Python 工具，集成了 () 大模型，提供图像分析、OCR 文字提取、智能文案创作和多模态对话功能。

## 特性

- 🖼️ **智能图像分析**: 深度理解图片内容、场景、情感
- 📝 **高精度 OCR**: 从图片提取文字、表格、文档
- ✍️ **文案创作**: 生成营销文案、社交媒体内容
- 💬 **多模态对话**: 支持图片+文本的交互式对话
- 🚀 **简单易用**: 直观的 CLI 和 Python API
- 🔒 **安全可靠**: 支持本地部署，保护数据隐私

## 安装

### 环境要求

- Python 3.8+
- API Key (从 https://platform./ 获取)

### 安装依赖

```bash
cd
pip install -r requirements.txt
```

## 快速开始

### 1. 配置 API Key

创建 `.env` 文件：

```bash
=
```

或设置环境变量：

```bash
export ="your_api_key_here"
```

### 2. 命令行使用

#### 图像分析

```bash
python cli.py analyze "图片路径.jpg" "分析这张图片的内容和特点"
```

#### OCR 文字提取

```bash
python cli.py ocr "文档图片.png"
```

#### 文案创作

```bash
python cli.py copywrite "产品图片.jpg" --style creative --platform wechat
```

#### 交互式对话

```bash
python cli.py chat
```

### 3. Python API 使用

```python
from

client = ()

# 图像分析
result = client.analyze_image(
    image_path="image.jpg",
    prompt="详细分析这张图片"
)
print(result)

# OCR 提取
text = client.extract_text("document.png")
print(text)

# 文案创作
copywriting = client.generate_copywriting(
    image_path="product.jpg",
    style="inspiring",
    platform="wechat"
)
print(copywriting)

# 多轮对话
conversation = client.create_conversation()
response = conversation.chat("你好", image="hello.jpg")
print(response)
```

## 功能详解

### 图像分析

支持对图片进行深度分析，包括：
- 物体识别
- 场景理解
- 情感分析
- 构图分析
- 色彩分析

```python
result = client.analyze_image(
    image_path="image.jpg",
    prompt="分析这张图片的构图和色彩搭配",
    model="",  # 可选: "", ""
    temperature=0.7
)
```

### OCR 文字提取

高精度识别图片中的文字内容：
- 中英文混合识别
- 表格结构保持
- 手写文字识别
- 多种输出格式

```python
text = client.extract_text(
    image_path="document.png",
    output_format="structured",  # text, structured, json
    language="auto"  # auto, zh, en
)
```

### 文案创作

根据图片或需求生成各种类型的文案：
- 产品描述
- 营销广告
- 社交媒体内容
- 品牌故事

```python
copywriting = client.generate_copywriting(
    image_path="product.jpg",
    prompt="创作一段吸引人的产品文案",
    style="creative",  # professional, casual, creative, inspiring
    platform="wechat",  # wechat, weibo, xiaohongshu, douyin
    length="medium"  # short, medium, long
)
```

### 多模态对话

支持图片和文本的混合输入，进行多轮对话：

```python
conversation = client.create_conversation()

# 第一轮
response1 = conversation.chat(
    message="请分析这张图片",
    image="screenshot.jpg"
)

# 第二轮（保持上下文）
response2 = conversation.chat(
    message="基于上面的分析，给出优化建议"
)
```

## 高级功能

### 批量处理

```python
images = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = client.batch_analyze(images, prompt="分析所有图片")
```

### 自定义模型参数

```python
result = client.analyze_image(
    image_path="image.jpg",
    model="",
    temperature=0.8,
    max_tokens=2000,
    top_p=0.9
)
```

### 流式输出

```python
for chunk in client.stream_analyze("image.jpg", "描述这张图片"):
    print(chunk, end="", flush=True)
```

## 项目结构

```
├── config.json          # 配置文件
├── skill.md             # 技能文档
├── prompt.md            # 提示词模板
├── README.md            # 项目说明
├── requirements.txt     # 依赖列表
├── .env.example         # 环境变量示例
├── cli.py              # 命令行接口
├── client.py           # API 客户端
├── utils.py            # 工具函数
└── examples/           # 使用示例
    ├── image_analysis.py
    ├── ocr_demo.py
    ├── copywriting.py
    └── conversation.py
```

## 配置说明

### 模型选择

- `""`: 基础模型，适合一般任务
- `""`: 长文本处理，32K 上下文
- `""`: 超长上下文，128K 上下文

### 参数调优

- `temperature`: 0-1，越高越创造性
- `max_tokens`: 最大输出长度
- `top_p`: 核采样参数
- `stream`: 是否流式输出

## 最佳实践

### 提示词编写

**好的提示词示例**：
```
"请详细分析这张产品图片，包括：
1. 产品外观和设计特点
2. 目标用户群体
3. 核心卖点
4. 适用场景
5. 营销建议"
```

### 图片预处理

- 建议使用高分辨率图片
- 支持格式：PNG, JPG, JPEG, WEBP
- 文件大小建议 < 10MB
- 避免过度压缩

### 错误处理

```python
try:
    result = client.analyze_image("image.jpg", "分析图片")
except APIError as e:
    print(f"API 错误: {e}")
except ImageError as e:
    print(f"图片错误: {e}")
```

## 常见问题

**Q: 如何获取 API Key？**
A: 访问 https://platform./ 注册并创建 API Key。

**Q: 支持哪些图片格式？**
A: 支持 PNG、JPG、JPEG、WEBP 等常见格式。

**Q: OCR 识别准确率如何？**
A: 中文识别准确率可达 95% 以上，手写文字需要较高清晰度。

**Q: 可以同时处理多张图片吗？**
A: 可以，最多支持同时处理 10 张图片。

**Q: 如何处理敏感内容？**
A: 系统会自动过滤敏感内容，请确保输入符合法律法规。

## 定价与配额

详见官网：https://platform./pricing

## 支持与反馈

- 官方文档: https://platform./docs
- 技术支持: support@
- 问题反馈: GitHub Issues

## 许可证

MIT License

## 贡献

欢迎提交 Pull Request 和 Issue！

---

Made with ❤️ by Claude Code
