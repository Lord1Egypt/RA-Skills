---
name: image-gen-cheap
description: 低成本图片生成与编辑。使用老张 API，最低 $0.01/张。支持文生图、图片编辑。触发词：生成图片、画图、AI 作图、文生图、图片编辑。
---

# Image Gen Cheap - 低成本图片生成

## 快速开始

### 1. 获取 API Token

访问 [https://api.laozhang.ai/register/?aff_code=lfa0](https://api.laozhang.ai/register/?aff_code=lfa0) 注册，在控制台获取 token。新注册自动获得 $0.5 开发测试额度。

保存 token：
```bash
echo "sk-your-token" > ~/.laozhang_api_token
```

### 2. 文生图

```bash
# 使用默认模型（sora_image，$0.01/张）
python scripts/generate_image.py "一只可爱的猫咪在花园里玩耍"

# 指定比例（2:3竖版/3:2横版/1:1正方形）
python scripts/generate_image.py "夕阳下的海滩" --ratio 3:2

# 保存到指定路径
python scripts/generate_image.py "可爱的小狗" --output dog.png

# 使用其他模型
python scripts/generate_image.py "未来城市" --model gpt-4o-image
```

### 3. 图片编辑

```bash
# 基础编辑
python scripts/edit_image.py "https://example.com/cat.jpg" "把猫咪的毛色改成彩虹色"

# 使用预设风格
python scripts/edit_image.py "https://example.com/photo.jpg" --style 卡通

# 多图融合
python scripts/edit_image.py "https://a.jpg,https://b.jpg" "将两张图片融合"
```

## 模型与价格

### 文生图模型

| 模型 | 模型ID | 价格 | 返回格式 |
|------|--------|------|---------|
| Sora Image | sora_image | **$0.01/张** | URL |
| GPT-4o Image | gpt-4o-image | **$0.01/张** | URL |
| Nano Banana | gemini-2.5-flash-image | $0.025/张 | base64 |
| Nano Banana2 | gemini-3.1-flash-image-preview | $0.03/张 | base64 |
| Nano Banana Pro | gemini-3-pro-image-preview | $0.05/张 | base64 |

### 图片编辑模型

| 模型 | 模型ID | 价格 | 返回格式 |
|------|--------|------|---------|
| GPT-4o Image | gpt-4o-image | **$0.01/张** | URL |
| Sora Image | sora_image | **$0.01/张** | URL |
| Nano Banana | gemini-2.5-flash-image | $0.025/张 | base64 |

**推荐**：默认使用 `sora_image`（文生图）和 `gpt-4o-image`（图片编辑），都是 $0.01/张且返回 URL。

## 预设风格

- 卡通 - 迪士尼卡通风格
- 油画 - 古典油画风格
- 水墨 - 中国水墨画风格
- 赛博朋克 - 霓虹灯光效果
- 素描 - 铅笔素描风格
- 水彩 - 水彩画风格

## 参数说明

### generate_image.py

```
--model, -m    使用的模型（默认: sora_image）
--ratio, -r    图片比例：2:3/3:2/1:1（仅 sora_image 支持）
--output, -o   保存图片到指定路径
--token, -t    指定 API token
--verbose, -v  显示详细信息
--json         输出完整 API 响应
--no-save      不保存图片（仅显示URL）
```

### edit_image.py

```
--model, -m    使用的模型（默认: gpt-4o-image）
--style, -s    预设风格（卡通/油画/水墨/赛博朋克/素描/水彩）
--output, -o   保存图片到指定路径
--token, -t    指定 API token
--verbose, -v  显示详细信息
--json         输出完整 API 响应
--no-save      不保存图片（仅显示URL）
```

## 依赖

```bash
pip install requests
```

## 注意事项

1. 返回 URL 的模型（sora_image / gpt-4o-image）可直接发送到飞书等平台
2. 返回 base64 的模型会自动解码保存到本地
3. 建议控制在 10 请求/分钟以内
