---
name: kay-image
description: |
  AI 图片生成与理解工具 - 支持文生图、图生图、图片理解、视频理解。
  基于 KIE AI API，支持 4K 输出、多种宽高比和参考图。
  
  **所需凭证**: 需要 KIE_API_KEY 环境变量（从 https://kie.ai/ 获取）
metadata:
  openclaw:
    requires:
      env:
        - KIE_API_KEY
      bins: []
    emoji: "🎨"
---

# Kay Image - AI 图片生成与理解

基于 KIE AI API 的图片生成与理解工具。

## ⚠️ 必需凭证

使用本工具前，必须配置 API Key：

### 获取 KIE API Key

1. 访问 https://kie.ai/
2. 注册并登录账号
3. 进入控制台 → API 管理
4. 创建 API Key 并复制

### 配置环境变量

```bash
export KIE_API_KEY="your-kie-api-key-here"
```

或在 skill 目录创建 `.env` 文件：
```bash
# 创建 .env 文件
nano skills/kay-image/.env
```

.env 文件内容：
```
KIE_API_KEY=your-kie-api-key-here
```

**注意**: 没有 API Key 将无法使用本工具的任何功能。

---

## 特性

- **文生图**: 根据文本描述生成图片
- **图生图**: 基于参考图进行编辑/变换
- **图片理解**: 分析图片内容（使用 GPT-5/Gemini）
- **视频理解**: 分析视频内容（使用 Gemini）
- **多分辨率**: 支持 1K/2K/4K 输出
- **多宽高比**: 支持 1:1, 3:4, 4:3, 9:16, 16:9, 21:9 等

---

## 使用方法

### 基本文生图
```bash
kay-image --prompt "一只可爱的橘猫在草地上玩耍" --output cat.png
```

### 指定宽高比和分辨率
```bash
kay-image --prompt "上海外滩夜景" --output shanghai.png --ar 16:9 --resolution 2K
```

### 图生图
```bash
kay-image --prompt "转换成动漫风格" --input https://example.com/photo.jpg --output anime.png
```

### 图片理解
```bash
kay-image --understand --image https://example.com/photo.jpg --prompt "描述这张图片"
```

### 视频理解
```bash
kay-image --understand --video https://example.com/video.mp4 --prompt "分析这个视频"
```

---

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--prompt` | `-p` | 提示词 | - |
| `--output` | `-o` | 输出路径 | - |
| `--input` | `-i` | 参考图路径 | - |
| `--ar` | - | 宽高比 | 1:1 |
| `--resolution` | `-r` | 分辨率 | 1K |
| `--understand` | `-u` | 理解模式 | false |
| `--image` | - | 图片路径 | - |
| `--video` | - | 视频路径 | - |

---

## 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `KIE_API_KEY` | ✅ 是 | KIE AI API 密钥 |
| `KIE_UNDERSTANDING_API_KEY` | ❌ 否 | 理解功能 API 密钥（默认使用 KIE_API_KEY） |
| `LAOZHANG_API_KEY` | ❌ 否 | LaoZhang API 密钥（可选） |

---

## 价格参考

- **1K 图片**: ~$0.04
- **2K 图片**: ~$0.06
- **4K 图片**: ~$0.09
- **图片理解**: ~$0.005-0.01/张

---

## 支持的宽高比

- `1:1` - 正方形
- `3:4` - 小红书/Instagram 竖版
- `4:3` - 标准横版
- `9:16` - 手机竖屏
- `16:9` - 宽屏
- `21:9` - 超宽屏

---

## 示例

### 生成小红书封面
```bash
kay-image -p "清新风格护肤品封面，粉色渐变背景" -o cover.png --ar 3:4 -r 2K
```

### 生成头像
```bash
kay-image -p "动漫风格女生头像，粉色头发" -o avatar.png --ar 1:1
```

### 图片风格迁移
```bash
kay-image -p "转换成油画风格" -i photo.jpg -o painting.png
```

### OCR 文字提取
```bash
kay-image -u --image document.jpg --prompt "提取所有文字"
```

---

## 脚本位置

`${SKILL_DIR}/scripts/main.ts`

---

## 注意事项

- **视频理解**: 仅 Gemini 模型支持
- **图片格式**: 支持 JPG、PNG、WebP
- **视频格式**: 支持 MP4、MOV
- **文件大小**: 建议图片 < 10MB，视频 < 100MB
