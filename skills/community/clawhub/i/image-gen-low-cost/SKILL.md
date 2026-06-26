---
name: image-gen-low-cost
description: 低成本 AI 图片生成 CLI 工具。支持文生图、图片编辑。触发词：生成图片、画图、AI 作图、文生图、图片编辑、imgen。
---

# Image Gen Low Cost - AI 图片生成 CLI

统一的命令行图片生成工具，支持任何 OpenAI 兼容的 API 端点。

## 快速开始

### 1. 获取 API Token

访问 [https://api.laozhang.ai/register/?aff_code=lfa0](https://api.laozhang.ai/register/?aff_code=lfa0) 注册，在控制台获取 token。新注册自动获得 $0.5 开发测试额度。

### 2. 配置 Token

```bash
# 使用 imgen config 命令（推荐）
imgen config --token YOUR_API_TOKEN

# 或使用环境变量
export IMGEN_TOKEN=YOUR_API_TOKEN
```

### 2. 文生图

```bash
# 生成图片
imgen "一只可爱的猫咪在花园里玩耍"

# 指定输出路径
imgen "夕阳下的海滩" -o beach.png

# 只显示 URL 不保存
imgen "未来城市" --no-save

# 使用不同模型
imgen "可爱的小狗" -m fast
```

### 3. 图片编辑

```bash
# 编辑图片
imgen edit "https://example.com/cat.jpg" "把猫咪的毛色改成彩虹色"

# 使用预设风格
imgen edit "https://example.com/photo.jpg" --style cartoon

# 多图融合
imgen edit "https://a.jpg,https://b.jpg" "将两张图片融合"
```

## 命令参考

```
imgen "prompt"                     文生图
imgen edit <url> "prompt"          图片编辑
imgen config --token <token>       配置 API Token
imgen models                       列出可用模型
```

### 选项

| 选项 | 说明 |
|------|------|
| `-m, --model <name>` | 模型选择 (cheap/fast/quality) |
| `-o, --output <path>` | 保存到指定路径 |
| `--size <size>` | 图片尺寸 (1024x1024 等) |
| `--no-save` | 不保存，只打印 URL |
| `-s, --style <style>` | 预设风格 |
| `-v, --verbose` | 详细输出 |

## 模型

| 别名 | 模型 ID | 价格 | 说明 |
|------|---------|------|------|
| sora | sora_image | $0.01/张 | **默认**， Sora Image， URL 返回 |
| gpt4o | gpt-4o-image | $0.01/张 | GPT-4o Image， URL 返回 |
| cheap | gemini-2.5-flash-image | $0.025/张 | Nano Banana, base64, 1K 固定 |
| fast | gemini-3.1-flash-image-preview | $0.045/张 | Nano Banana2, base64, 4K 支持 |
| quality | gemini-3-pro-image-preview | $0.05/张 | Nano Banana Pro, base64, 4K + 高级特性 |

> 💡 **默认使用 sora 模型 ($0.01/张)**，如 鍗  鍘- 追求极致性价比： 选 **sora** 或 **- 追求高质量稳定： 选 **cheap** |
 **- 追求 4K + 性价比： 选 **fast** |
 **- 追求最高质量 + 复杂指令： 选 **quality** |

## 预设风格

- `cartoon` - 迪士尼卡通风格
- `oil` - 古典油画风格
- `ink` - 中国水墨画风格
- `cyberpunk` - 赛博朋克霓虹风格
- `sketch` - 铅笔素描风格
- `watercolor` - 水彩画风格

## API 端点

默认使用老张 API (`https://api.laozhang.ai/v1/chat/completions`)。

```bash
# 切换到其他 OpenAI 兼容端点
export IMGEN_API_URL=https://api.openai.com/v1/chat/completions

# 使用其他兼容服务
export IMGEN_API_URL=https://your-api-endpoint.com/v1/chat/completions
```

> ⚠️ **重要**：如果你使用非老张 API 的 token，请确保设置对应的 `IMGEN_API_URL`，否则 token 会发送到错误的端点。

## 安装

```bash
# 克隆或下载 skill 后
chmod +x scripts/imgen.js

# 添加到 PATH（可选）
ln -s $(pwd)/scripts/imgen.js /usr/local/bin/imgen
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `IMGEN_TOKEN` | API Token |
| `IMGEN_API_URL` | 自定义 API 端点 |

## 注意事项

1. 返回的图片 URL 通常是临时的，建议及时保存
2. 默认保存到当前目录的 `generated-images/` 文件夹
3. Token 存储在 `~/.imgen/token`，权限为 600

## 与 image-gen-cheap 的区别

| 特性 | image-gen-cheap | image-gen-low-cost |
|------|-----------------|---------------------|
| 实现 | Python 脚本 | Node.js CLI |
| 依赖 | requests | 无外部依赖 |
| API | 固定老张 API | 任意 OpenAI 兼容 |
| 配置 | 独立 token 文件 | 统一 imgen config |
