---
slug: "logo-design-guide-free"
name: "logo-design-guide-free"
version: 1.0.1
displayName: "Logo设计指南(免费版)"
summary: "提供包含覆盖辨识度设计、多格式交付、多平台适配、色彩字体系统与一致性规范.(免费版).从辨识度设计到多平台交付的Logo设计全流程:三大辨识要素、多格式 输出(PNG/JPG/SVG/ICO/Web"
summary_zh: "覆盖辨识度设计、多格式交付、多平台适配、色彩字体系统与一致性规范。(免费版)。从辨识度设计到多平台交付的Logo设计全流程:三大辨识要素、多格式 输出(PNG/JPG/SVG/ICO/Web"
license: "MIT"
description: "|-. 适用于需要logo design guide相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  从辨识度设计到多平台交付的Logo设计全流程:三大辨识要素、多格式
  输出(PNG/JPG/SVG/ICO/WebP)、多平台适配(Favicon/App/PWA/Social)、
  色彩与字体系统、矢量优先与一致性规范。适用于独立开发者、企业团队
  和自动化工作流场景.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 创意设计
  - logo
  - design
  - guide
  - automation
  - 设计
  - UI/UX
  - 创意
  - png
  - size
category: "Creative"
pricing_tier: free
---
# Logo设计指南(免费版)

从辨识度设计到多平台交付的Logo设计全流程,确保Logo在任何尺寸、任何背景、任何平台下都清晰可辨且一致.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Logo设计指南(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 核心能力

### 1. 辨识度设计三大要素
- 简单:能在5秒内被记住,删除所有非必要细节
- 易记:有独特视觉钩子(形状、色彩、负空间)
- 易复述:能用语言描述给他人(如"一个咬了一口的苹果")
- 测试:缩到16x16像素仍可辨认核心特征

### 2. 多格式交付
| 格式 | 用途 | 特征 |
|:-----|:-----|:-----|
| SVG | 矢量源文件、网页 | 无损缩放,文件小,可编辑 |
| PNG | 透明背景位图 | 支持Alpha通道,通用 |
| JPG | 摄影背景用 | 不支持透明,有损压缩 |
| ICO | 浏览器favicon | 多尺寸打包(16/32/48) |
| WebP | 现代网页 | 比PNG小26%,支持透明 |

### 3. 多平台适配尺寸
- Favicon:`16x16`、`32x32`、`48x48` 像素,打包为 `favicon.ico`
- Apple Touch Icon:`180x180` 像素,圆角自动应用
- PWA图标:`192x192`、`512x512` 像素,`manifest.json` 引用
- 社交分享:`1200x630` 像素,Open Graph 与 Twitter Card
- App图标:`1024x1024` 像素,应用商店提交
- 安全区:图标内容需在80%安全区内,留padding

### 4. 色彩系统
- 品牌主色:1个主色 + 1个辅色,RGB与HEX双标注
- 单色版:纯黑、纯白版本,用于单色印刷与深色背景
- 深色背景版:反色或调整对比度,确保可读性
- 色彩无障碍:前景与背景对比度 ≥ 4.5:1(WCAG AA)
- 渐变处理:提供明暗两端HEX值与渐变方向

### 输出格式

完成响应以Markdown格式返回,包含任务状态(成功/失败)、解析摘要和具体输出数据。失败时返回错误码和错误信息,便于定位问题。- 验证返回数据的完整性和格式正确性
- 参考`输出格式`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---:|---:|---:|
| Logo设计 | 品牌名+行业+风格 | 辨识度设计建议+视觉钩子 |
| 多平台交付 | SVG源文件 | Favicon/Apple/PWA/Social全尺寸 |
| 色彩系统 | 品牌主色 | 主色+单色版+深色背景版+对比度 |

不适用于:复杂插画设计、3D建模、动态Logo动画、商标法律合规审查.
## 使用流程

1. 确认品牌名、行业、调性,设计三大辨识要素
2. 用AI生成草图,矢量化为SVG源文件
3. 从SVG导出多平台尺寸(Favicon/PWA/Social)
4. 定义色彩系统:主色、单色版、深色背景版
5. 打包交付:SVG源 + 各格式位图 + 指南文档

## 示例

### 示例:Favicon多尺寸
```
输入: logo.svg
输出:
  favicon-16x16.png    // 浏览器标签
  favicon-32x32.png    // 高分屏标签
  favicon-48x48.png    // Windows站点图标
  favicon.ico          // 打包16/32/48
  apple-touch-icon.png // 180x180 iOS添加到主屏
```

## 代码示例

### 使用 ImageMagick 从 SVG 批量生成多尺寸图标

```bash
#!/bin/bash
# 从 SVG 源文件生成全平台图标
# 依赖: ImageMagick 7.x (brew install imagemagick / apt install imagemagick)

SOURCE="logo.svg"
OUTPUT_DIR="./icons"
mkdir -p "$OUTPUT_DIR"

# Favicon 多尺寸 PNG
for size in 16 32 48; do
  convert -background none "$SOURCE" \
    -resize "${size}x${size}" \
    -gravity center -extent "${size}x${size}" \
    "$OUTPUT_DIR/favicon-${size}x${size}.png"
done

# 打包为 favicon.ico（含16/32/48三尺寸）
convert "$OUTPUT_DIR/favicon-16x16.png" \
        "$OUTPUT_DIR/favicon-32x32.png" \
        "$OUTPUT_DIR/favicon-48x48.png" \
        "$OUTPUT_DIR/favicon.ico"

# Apple Touch Icon (180x180, 白色圆角背景)
convert -background white "$SOURCE" \
  -resize 144x144 -gravity center -extent 180x180 \
  "$OUTPUT_DIR/apple-touch-icon.png"

# PWA 图标 (192x192, 512x512)
for size in 192 512; do
  convert -background none "$SOURCE" \
    -resize "${size}x${size}" \
    "$OUTPUT_DIR/pwa-${size}x${size}.png"
done

# 社交分享图 (1200x630, 居中放置Logo)
convert -background "#1a1a2e" "$SOURCE" \
  -resize 400x400 -gravity center -extent 1200x630 \
  "$OUTPUT_DIR/social-share.png"

echo "图标生成完成: $(ls -1 $OUTPUT_DIR | wc -l) 个文件"
```

### 使用 Python 生成 PWA manifest.json

```python
import json

# 生成 PWA manifest.json，引用所有必要尺寸图标
manifest = {
    "name": "My Brand App",
    "short_name": "MyBrand",
    "description": "品牌PWA应用",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#1a1a2e",
    "theme_color": "#0f3460",
    "icons": [
        {
            "src": "/icons/pwa-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "/icons/pwa-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ]
}

with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("manifest.json 已生成")
```

### 使用 Python 验证色彩对比度（WCAG AA）

```python
def hex_to_rgb(hex_color):
    """将HEX颜色转为RGB元组"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    """计算WCAG相对亮度"""
    def adjust(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [adjust(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(fg_hex, bg_hex):
    """计算前景色与背景色的对比度比值"""
    fg_lum = relative_luminance(hex_to_rgb(fg_hex))
    bg_lum = relative_luminance(hex_to_rgb(bg_hex))
    lighter = max(fg_lum, bg_lum)
    darker = min(fg_lum, bg_lum)
    return (lighter + 0.05) / (darker + 0.05)

# 验证品牌主色在白色背景上的对比度
brand_color = "#0F3460"  # 品牌深蓝
bg_color = "#FFFFFF"     # 白色背景
ratio = contrast_ratio(brand_color, bg_color)
print(f"对比度: {ratio:.2f}:1")
print(f"WCAG AA (正常文字 ≥4.5:1): {'通过' if ratio >= 4.5 else '不通过'}")
print(f"WCAG AA (大文字 ≥3.0:1): {'通过' if ratio >= 3.0 else '不通过'}")
```

### 使用 rsvg-convert 进行高质量SVG转PNG

```bash
# 使用 librsvg 进行高质量SVG渲染（比ImageMagick更精确）
# 依赖: librsvg (brew install librsvg / apt install librsvg2-bin)

# 生成 App Store 图标 (1024x1024)
rsvg-convert -w 1024 -h 1024 -b white logo.svg -o app-icon-1024.png

# 生成不同密度的Android图标
for density in mdpi:48 hdpi:72 xhdpi:96 xxhdpi:144 demohdpi:192; do
  name="${density%%:*}"
  size="${density##*:}"
  rsvg-convert -w $size -h $size -b none logo.svg -o "android-${name}-${size}.png"
done

# 批量导出WebP格式（比PNG小26%）
for size in 16 32 48 192 512; do
  rsvg-convert -w $size -h $size logo.svg -o "temp-${size}.png"
  cwebp -q 90 "temp-${size}.png" -o "logo-${size}.webp"
  rm "temp-${size}.png"
done
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 16x16 favicon 模糊不可辨 | 细节过多 | 简化为图标版,删除文字与小细节,只保留核心轮廓 |
| SVG 矢量化后丢失渐变 | 描摹工具不支持渐变 | 手动重建渐变,提供明暗两端HEX与渐变方向 |
| 深色背景上Logo不可见 | 仅设计了浅色版 | 提供反色版(纯白)与深色背景专用版,对比度≥4.5:1 |
| PWA 安装后图标缺失 | manifest.json 未引用512x512 | 确认 `icons` 数组含 192x192 与 512x512 两项,type为image/png |

## 常见问题

### Q1: 辨识度设计的"5秒记忆测试"如何执行?
A: 展示Logo 5秒后遮挡,让测试者画出核心特征。若多数人能画出主轮廓,辨识度达标;若画不出或画错,说明细节过多或钩子不明确。缩小到16x16像素仍可辨认是最严格测试.
### Q2: Favicon为何需要16/32/48多尺寸打包?
A: 不同场景使用不同尺寸:16x16用于旧浏览器标签,32x32用于高分屏标签,48x48用于Windows站点图标。打包为 `favicon.ico` 让浏览器自动选择合适尺寸,避免模糊.
### Q3: PWA图标192x192与512x512有何区别?
A: 192x192用于主屏图标显示,512x512用于应用启动屏(splash screen)与更高分辨率设备。`manifest.json` 的 `icons` 数组必须同时包含两者,否则PWA安装会报错或图标缺失.
## 已知限制

- 需要LLM支持生成设计建议,实际绘图需配合理图工具
- AI生成的位图需手动矢量化,无法直接输出生产级SVG
- 商标法律合规需专业律师审查,本指南不覆盖

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
本Skill无需额外API Key（LLM能力由Agent平台内置提供）

### 可用性分类
- **分类**: MD+EXEC（）

## 升级提示

本免费版提供基础功能。升级到完整版 logo-design-guide 获取全部能力和高级特性.