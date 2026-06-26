---
name: grs-image
description: GrsAI Nano Banana Pro 图片生成工具。使用 GrsAI API 生成图片，支持中文描述。适用于室内设计效果图、开工大吉海报、设计素材生成等场景。
---

# GrsAI Image Generator

GrsAI Nano Banana Pro 图片生成工具。

## 前提条件

```bash
pip install requests
export GRSAAI_API_KEY='your-api-key'
```

## API 信息

- **国内接口**: `https://grsai.dakka.com.cn`
- **海外接口**: `https://grsaiapi.com`
- **文档地址**: https://grsai.ai/zh/dashboard/documents/nano-banana

## 模型选择

| 模型 | 支持分辨率 |
|------|-----------|
| nano-banana-pro | 1K / 2K / 4K |
| nano-banana-pro-vt | 1K / 2K / 4K |
| nano-banana-pro-cl | 1K / 2K / 4K |
| nano-banana-pro-vip | 1K / 2K |
| nano-banana-pro-4k-vip | 4K |
| nano-banana-fast | 1K |
| nano-banana | 1K |
| nano-banana-2 | 1K / 2K / 4K |
| nano-banana-2-cl | 1K / 2K |
| nano-banana-2-4k-cl | 4K |

## 使用方式

### 基本用法

```bash
python skills/grs-image/scripts/grs_image.py "一只可爱的橘猫在草地上玩耍"
```

### 指定输出文件

```bash
python skills/grs-image/scripts/grs_image.py "现代简约客厅效果图" -o living_room.png
```

### 指定宽高比

```bash
# 1:1 方图
python skills/grs-image/scripts/grs_image.py "开工大吉海报" -r 1:1 -o kaigong.png

# 16:9 横图
python skills/grs-image/scripts/grs_image.py "客厅效果图" -r 16:9 -o living.png

# 9:16 竖图
python skills/grs-image/scripts/grs_image.py "阳台设计" -r 9:16 -o balcony.png
```

支持的宽高比：`auto` / `1:1` / `16:9` / `9:16` / `4:3` / `3:4` / `3:2` / `2:3` / `5:4` / `4:5` / `21:9`
额外比例（nano-banana-2系列）：`1:4` / `4:1` / `1:8` / `8:1`

### 指定分辨率

```bash
# 生成2K分辨率图片（默认1K）
python skills/grs-image/scripts/grs_image.py "高清效果图" -s 2K -o hd_design.png

# 生成4K分辨率图片
python skills/grs-image/scripts/grs_image.py "超高清晰度效果图" -s 4K -o 4k_design.png
```

### 图生图（参考图）

```bash
python skills/grs-image/scripts/grs_image.py "把这张图改成奶油风" \
  -u "https://example.com/reference.png" \
  -r 16:9 -o output.png
```

### 使用快速模型

```bash
python skills/grs-image/scripts/grs_image.py "快速草图" -m nano-banana-fast
```

## 常用场景示例

### 室内设计效果图

```bash
python skills/grs-image/scripts/grs_image.py "现代简约风格客厅效果图，浅色地板，白墙，大窗户" -r 16:9 -s 2K -o design.png
```

### 开工大吉海报

```bash
python skills/grs-image/scripts/grs_image.py "开工大吉红金配色中国传统风格设计师专属" -r 1:1 -s 2K -o kaigong.png
```

### 设计素材

```bash
python skills/grs-image/scripts/grs_image.py "大理石纹理瓷砖样品高清图片" -r 1:1 -s 2K -o tile.png
```

## 输出示例

```
正在生成图片...
Prompt: 一只可爱的橘猫在草地上玩耍
Ratio: 16:9
Size: 2K
任务ID: 3-9b0ef381-a39c-4a03-8667-298380fe1fc1
生成中... 100%
图片URL: https://file1.aitohumanize.com/file/xxx.png
已保存: output.png

完成: output.png
```

## 注意事项

- 图片生成需要 30-60 秒，分辨率越高时间越长
- 建议先测试小图，效果满意后再生成正式图
- 中文描述效果较好，英文也可以
- 图片 URL 有效期 2 小时
- 图生图的参考图支持 URL 或 Base64
