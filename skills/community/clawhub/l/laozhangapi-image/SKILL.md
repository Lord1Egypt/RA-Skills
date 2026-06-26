---
name: laozhangapi-image
description: 使用老张 API 生成和编辑图片，最低 $0.01/张。支持文生图、图片编辑、多图融合、多种比例。触发词：生成图片、画图、AI作图、文生图、图片编辑、换背景、风格转换、Sora生图。
---

# 老张 API 图片生成

低成本高质量图片生成与编辑。

## 快速开始

### 1. 配置 Token

```bash
echo "sk-xxx" > ~/.laozhang_api_token
```

访问 [老张 API](https://api.laozhang.ai/register/?aff_code=lfa0) 注册获取 token。新注册自动获得 $0.5 测试额度。

### 2. 文生图

```bash
# 默认模型（sora_image，$0.01/张，返回URL）
python scripts/generate_image.py "一只可爱的猫咪在花园里"

# 指定比例（仅 sora_image 支持）
python scripts/generate_image.py "夕阳海滩" --ratio 3:2

# 保存到本地
python scripts/generate_image.py "可爱小狗" --output dog.png
```

### 3. 图片编辑

```bash
# 基础编辑（默认 gpt-4o-image，$0.01/张）
python scripts/edit_image.py "https://example.com/cat.jpg" "把毛色改成彩虹色"

# 预设风格
python scripts/edit_image.py "https://example.com/photo.jpg" --style 卡通

# 多图融合
python scripts/edit_image.py "https://a.jpg,https://b.jpg" "融合两张图"
```

## 模型选择

| 用途 | 推荐模型 | 价格 | 返回 |
|------|---------|------|------|
| 文生图（默认） | sora_image | $0.01/张 | URL |
| 图片编辑（默认） | gpt-4o-image | $0.01/张 | URL |
| 高质量/4K | gemini-3-pro-image-preview | $0.05/张 | base64 |
| 性价比 | gemini-2.5-flash-image | $0.025/张 | base64 |

详细模型对比见 [references/models.md](references/models.md)。

## 预设风格

卡通、油画、水墨、赛博朋克、素描、水彩

## 参数

### generate_image.py

```
--model, -m    模型选择（默认: sora_image）
--ratio, -r    比例：2:3/3:2/1:1（仅 sora_image）
--output, -o   保存路径
--no-save      不保存，仅显示URL
```

### edit_image.py

```
--model, -m    模型选择（默认: gpt-4o-image）
--style, -s    预设风格
--output, -o   保存路径
--no-save      不保存，仅显示URL
```

## 常见示例

见 [examples/usage.md](examples/usage.md)。

## 注意

- URL 返回的模型可直接发送到飞书
- base64 返回的模型会自动保存到本地
- 建议控制在 10 请求/分钟
