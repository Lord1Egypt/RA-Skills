# Image Gen Low Cost

统一命令行 AI 图片生成工具。支持文生图、图片编辑，兼容任何 OpenAI API 端点。

## 安装

```bash
npm install -g image-gen-low-cost
```

## 快速开始

```bash
# 1. 获取 token：访问 https://api.laozhang.ai/register/?aff_code=lfa0 注册

# 2. 配置 token
imgen config --token YOUR_API_TOKEN

# 3. 生成图片
imgen "一只可爱的猫咪在花园里玩耍"
```

## 命令

```bash
# 文生图
imgen "prompt"

# 图片编辑
imgen edit <image_url> "edit prompt"
imgen edit <image_url> --style cartoon

# 查看模型
imgen models
```

## 选项

| 选项 | 说明 |
|------|------|
| `-m, --model` | 模型 (cheap/fast/quality) |
| `-o, --output` | 输出路径 |
| `--no-save` | 只打印 URL |
| `-s, --style` | 预设风格 |

## 自定义 API

```bash
export IMGEN_API_URL=https://your-api.com/v1/chat/completions
```

## License

MIT
