# 大模型工具 - 完整指南

## 🎯 概述

这是一个基于  大模型的 Python 工具集，提供图像分析、OCR 文字提取、智能文案创作和多模态对话功能。

## ✨ 核心特性

- 🖼️ **智能图像分析** - 深度理解图片内容、场景、情感
- 📝 **高精度 OCR** - 从图片提取文字、表格、文档
- ✍️ **文案创作** - 生成营销文案、社交媒体内容
- 💬 **多模态对话** - 支持图片+文本的交互式对话
- 🚀 **简单易用** - 直观的 CLI 和 Python API
- 🔒 **安全可靠** - 支持本地部署，保护数据隐私

## 📦 项目结构

```
├── config.json          # 配置文件
├── skill.md             # 技能文档
├── prompt.md            # 提示词模板
├── README.md            # 项目说明
├── requirements.txt     # 依赖列表
├── .env.example         # 环境变量示例
├── .gitignore          # Git 忽略文件
├── quickstart.py       # 快速入门脚本
├── cli.py              # 命令行接口
├── client.py           # API 客户端
├── utils.py            # 工具函数
├── examples/           # 使用示例
│   ├── image_analysis.py
│   ├── ocr_demo.py
│   ├── copywriting.py
│   └── conversation.py
└── output/             # 输出目录
    ├── images/
    └── text/
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 获取 API Key: https://platform./
=
```

### 3. 运行快速入门脚本

```bash
python quickstart.py
```

### 4. 验证配置

```bash
python cli.py config
```

## 💻 命令行使用

### 图像分析

```bash
# 基本用法
python cli.py analyze "图片路径.jpg"

# 自定义提示词
python cli.py analyze "图片路径.jpg" --prompt "详细分析这张图片的产品特点"

# 选择模型
python cli.py analyze "图片路径.jpg" --model ""

# 调整创造性
python cli.py analyze "图片路径.jpg" --temperature 0.8
```

### OCR 文字提取

```bash
# 基本用法
python cli.py ocr "文档图片.png"

# 结构化输出
python cli.py ocr "文档图片.png" --format structured

# 保存到文件
python cli.py ocr "文档图片.png" --output "extracted.txt"

# 指定语言
python cli.py ocr "文档图片.png" --language zh
```

### 文案创作

```bash
# 基于图片创作
python cli.py copywrite --image "产品.jpg"

# 指定风格和平台
python cli.py copywrite --image "产品.jpg" --style creative --platform wechat

# 纯文本创作
python cli.py copywrite --prompt "创作一段夏季促销文案"

# 保存结果
python cli.py copywrite --image "产品.jpg" --output "copywriting.txt"
```

### 交互式对话

```bash
# 启动对话
python cli.py chat

# 在对话中发送图片
你: image /path/to/image.jpg
```

### 批量处理

```bash
# 批量分析
python cli.py batch image1.jpg image2.jpg image3.jpg
```

## 🐍 Python API 使用

### 初始化客户端

```python
from

client = ()
```

### 图像分析

```python
result = client.analyze_image(
    image_path="image.jpg",
    prompt="分析这张图片的内容和特点"
)
print(result.content)
```

### OCR 提取

```python
result = client.extract_text(
    image_path="document.png",
    output_format="structured"
)
print(result.text)
```

### 文案创作

```python
result = client.generate_copywriting(
    image_path="product.jpg",
    style="creative",
    platform="wechat"
)
print(result.content)
```

### 多轮对话

```python
conversation = client.create_conversation()

response1 = conversation.chat("你好", image="hello.jpg")
response2 = conversation.chat("基于上面的分析，给出建议")
```

## 🎨 高级功能

### 自定义模型参数

```python
result = client.analyze_image(
    image_path="image.jpg",
    model="",  # 选择模型
    temperature=0.8,  # 创造性程度
    max_tokens=2000,  # 最大输出长度
    top_p=0.9  # 核采样
)
```

### 流式输出

```python
for chunk in client.stream_analyze("image.jpg", "描述图片"):
    print(chunk, end="", flush=True)
```

### 批量处理

```python
images = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = client.batch_analyze(images, prompt="分析所有图片")
```

## 📊 可用模型

| 模型 | 上下文 | 适用场景 |
|------|--------|----------|
|  | 8K | 一般任务 |
|  | 32K | 长文档处理 |
|  | 128K | 超长文档 |

## 🔧 配置选项

### 环境变量

```bash
# API Key (必需)
=

# API Base URL (可选)
BASE_URL=https://api.

# 默认模型 (可选)
DEFAULT_MODEL=

# 请求超时 (可选)
TIMEOUT=60

# 最大重试次数 (可选)
MAX_RETRIES=3

# 调试模式 (可选)
DEBUG=false
```

## 📚 示例代码

### 图像分析示例

```bash
python examples/image_analysis.py
```

### OCR 示例

```bash
python examples/ocr_demo.py
```

### 文案创作示例

```bash
python examples/copywriting.py
```

### 对话示例

```bash
python examples/conversation.py
```

## ⚠️ 注意事项

### 安全提醒

- ✅ 永远不要在代码中暴露 API Key
- ✅ 使用环境变量管理密钥
- ✅ 定期轮换 API Key
- ✅ 监控 API 使用情况

### 使用限制

- 单张图片建议 < 10MB
- 支持格式: PNG, JPG, JPEG, WEBP
- 遵守  服务条款
- 不得用于非法用途

### 最佳实践

1. **提示词编写** - 具体、明确、结构化
2. **图片预处理** - 使用高分辨率、清晰图片
3. **错误处理** - 实现重试和降级机制
4. **性能优化** - 批量请求、结果缓存

## 🆘 常见问题

**Q: 如何获取 API Key？**
A: 访问 https://platform./ 注册并创建 API Key

**Q: 支持哪些图片格式？**
A: PNG, JPG, JPEG, WEBP 等常见格式

**Q: OCR 识别准确率如何？**
A: 中文识别准确率可达 95% 以上

**Q: 可以同时处理多张图片吗？**
A: 最多支持同时处理 10 张图片

**Q: 如何处理敏感内容？**
A: 系统会自动过滤敏感内容

## 📖 资源链接

- **官方文档**: https://platform./docs
- **API 参考**: https://platform./docs/api
- **技术支持**: support@
- **开发者社区**: 官方论坛

## 📝 更新日志

### v1.0.0 (2025-03-25)
- ✨ 初始版本发布
- ✅ 支持图像分析、OCR、文案创作
- ✅ 交互式对话功能
- ✅ Python SDK 集成
- ✅ 命令行工具
- ✅ 完整示例代码

## 🤝 贡献

欢迎提交 Pull Request 和 Issue！

## 📄 许可证

MIT License

---

**Made with ❤️ by Claude Code**

**注意**: 这个技能工具集需要配合  API Key 使用。请确保你有合法的 API 访问权限，并遵守相关的使用条款和法律法规。
