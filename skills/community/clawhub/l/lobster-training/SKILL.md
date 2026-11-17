---
name: image-gen
description: AI图像生成与编辑。支持文生图、图+文生图、风格转换。当用户要求画图、生成图片、编辑图片、图片风格转换时使用此 skill。支持多种比例（1:1、3:2、16:9、21:9 等）和分辨率（标准、2K、4K）。
---

# AI 图像生成

通过执行脚本调用 Gemini Flash Image API 生成图片。

## 环境变量

脚本通过以下环境变量获取 API 配置：

- `IMAGE_GEN_API_KEY` — API 密钥
- `IMAGE_GEN_BASE_URL` — API 基础地址（默认：https://code.newcli.com/gemini）

## 使用方法

### 生成图片

执行脚本生成图片：

```bash
export IMAGE_GEN_API_KEY="your-api-key"
export IMAGE_GEN_BASE_URL="https://code.newcli.com/gemini"

python3 scripts/generate_image.py "你的提示词" --model gemini-3.1-flash-image-2k-16x9 --output output.png
```

### 参数说明

- `prompt`（必填）：图片描述提示词
- `--model, -m`：模型名称，默认 `gemini-3.1-flash-image-2k-16x9`
- `--output, -o`：输出文件路径，默认当前目录 `generated_image.png`

## 可用模型

默认模型：`gemini-3.1-flash-image-2k-16x9`（2K 分辨率，16:9 横屏）

### 基础模型（标准分辨率）

| 模型 ID | 比例 | 适用场景 |
|---------|------|----------|
| gemini-3.1-flash-image | 1:1 | 社交媒体头像 |
| gemini-3.1-flash-image-3x2 | 3:2 | 横版照片 |
| gemini-3.1-flash-image-2x3 | 2:3 | 竖版海报 |
| gemini-3.1-flash-image-3x4 | 3:4 | 竖版海报 |
| gemini-3.1-flash-image-4x3 | 4:3 | 传统比例 |
| gemini-3.1-flash-image-4x5 | 4:5 | Instagram |
| gemini-3.1-flash-image-5x4 | 5:4 | 传统横版 |
| gemini-3.1-flash-image-9x16 | 9:16 | 手机壁纸/短视频 |
| gemini-3.1-flash-image-16x9 | 16:9 | 电脑壁纸/视频 |
| gemini-3.1-flash-image-21x9 | 21:9 | 超宽屏 |

### 2K 分辨率（推荐）

| 模型 ID | 比例 |
|---------|------|
| gemini-3.1-flash-image-2k | 1:1 |
| gemini-3.1-flash-image-2k-3x2 | 3:2 |
| gemini-3.1-flash-image-2k-2x3 | 2:3 |
| gemini-3.1-flash-image-2k-3x4 | 3:4 |
| gemini-3.1-flash-image-2k-4x3 | 4:3 |
| gemini-3.1-flash-image-2k-4x5 | 4:5 |
| gemini-3.1-flash-image-2k-5x4 | 5:4 |
| gemini-3.1-flash-image-2k-9x16 | 9:16 |
| gemini-3.1-flash-image-2k-16x9 | 16:9 |
| gemini-3.1-flash-image-2k-21x9 | 21:9 |

### 4K 分辨率

| 模型 ID | 比例 |
|---------|------|
| gemini-3.1-flash-image-4k | 1:1 |
| gemini-3.1-flash-image-4k-3x2 | 3:2 |
| gemini-3.1-flash-image-4k-2x3 | 2:3 |
| gemini-3.1-flash-image-4k-3x4 | 3:4 |
| gemini-3.1-flash-image-4k-4x3 | 4:3 |
| gemini-3.1-flash-image-4k-4x5 | 4:5 |
| gemini-3.1-flash-image-4k-5x4 | 5:4 |
| gemini-3.1-flash-image-4k-9x16 | 9:16 |
| gemini-3.1-flash-image-4k-16x9 | 16:9 |

## 工作流程

1. **理解需求**：分析用户的图片需求，确定比例和分辨率
2. **选择模型**：根据用途选择合适的模型（默认 2K-16x9）
3. **优化提示词**：将用户描述扩展为详细的图片提示词
4. **执行脚本**：调用 `scripts/generate_image.py` 生成图片
5. **展示结果**：读取生成的图片展示给用户

## 提示词技巧

- **具体描述**：主体、场景、光线、风格、色调
- **风格参考**：水彩、油画、赛博朋克、吉卜力、写实摄影、中国工笔等
- **构图说明**：视角（俯视/仰视）、景深、焦点
- **色彩指定**：主色调、配色方案

## 示例

生成中国风后羿射日图：

```bash
python3 scripts/generate_image.py \
  "一位英勇的古代射手后羿站在险峻的高山之巅，身披金色战甲，肌肉紧绷，拉开巨大的神弓，一支燃烧着神圣光芒的箭矢对准天空中炽热的太阳。天空中有多个太阳同时燃烧，火焰倾泻而下。背景是翻滚的云海和龟裂的大地，远山在热浪中扭曲。中国传统工笔重彩风格，水墨与金箔点缀，色彩以深红、金色、墨黑、靛蓝为主，画面气势磅礴，具有敦煌壁画的厚重感。16:9 宽幅构图。" \
  --model gemini-3.1-flash-image-2k-16x9 \
  --output houyi.png
```
