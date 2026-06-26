# AI 火宝

🔥 火山引擎 AI 生图 Skill。支持多种模型。

## 环境变量

```bash
export HUOBAO_API_KEY="<your-api-key>"
```

或使用 `--api-key` 参数传入。

## 支持的模型

| 模型 | 说明 |
|------|------|
| `gemini-2.5-flash-image` | Gemini 2.5 Flash Image |
| `gemini-2.5-flash-image-preview` | Gemini 2.5 Flash Image Preview |
| `nano-banana` | Nano Banana |
| `nano-banana-pro` | Nano Banana Pro |
| `nano-banana-pro_4k` | Nano Banana Pro 4K |
| `doubao-seedream-4-5-251128` | 豆包 Seedream 4.5 |

## 支持的尺寸

| 尺寸 | 说明 |
|------|------|
| `1x1` | 正方形 |
| `16x9` | 宽屏 |
| `9x16` | 竖屏 |
| `3x4` | 竖屏 |
| `4x3` | 宽屏 |

## 功能

### 文生图 (text2image)

```bash
python3 scripts/t2i.py "提示词" --model nano-banana-pro --size 1x1
```

### 图生图 (image2image)

```bash
python3 scripts/i2i.py --image <图片URL> --prompt "描述" --model nano-banana-pro
```

## 参数

| 参数 | 说明 |
|------|------|
| `prompt` | 提示词（必填） |
| `--model` | 模型名称（默认: nano-banana-pro） |
| `--size` | 尺寸（默认: 1x1） |
| `--count` | 生成数量 1-4 (默认: 1) |
| `--watermark` | 是否添加水印 (默认: true) |
| `--api-key` | API Key（必填） |
| `--debug` | 调试模式 |

## 示例

```bash
# 文生图 - Nano Banana Pro
python3 scripts/t2i.py "一只可爱的猫咪" --model nano-banana-pro --size 1x1 --api-key "sk-xxx"

# 文生图 - Gemini 2.5 Flash
python3 scripts/t2i.py "风景画" --model gemini-2.5-flash-image --size 16x9 --api-key "sk-xxx"

# 图生图
python3 scripts/i2i.py --image "https://example.com/img.jpg" --prompt "动漫风格" --model nano-banana-pro --api-key "sk-xxx"
```

## 输出格式

成功返回 JSON：
```json
{
  "success": true,
  "prompt": "...",
  "model": "nano-banana-pro",
  "size": "1x1",
  "count": 1,
  "images": [{"url": "..."}],
  "usage": {...}
}
```
