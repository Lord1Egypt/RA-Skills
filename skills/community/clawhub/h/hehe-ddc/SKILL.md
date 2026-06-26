---
name: ddc
version: 1.0.0
description: "抖音视频自动生成 - 图片 + 文案→视频，支持 Edge TTS 男女声、逐行字幕、随机 BGM、智能时长适配"
author: openclaw
tags: ["video", "douyin", "tiktok", "automation", "tts", "ffmpeg", "ddc"]
---

# 视频自动化技能 (Video Auto Skill)

## 🎯 功能概述

一键生成抖音标准营销视频：

```
图片 + 文案 → 视频生成 → 自动发布
```

**核心特性**：
- ✅ 有脚本按脚本，无脚本自动生成
- ✅ Edge TTS 男女声可选（真正男声/女声）
- ✅ 逐行字幕（说到哪句显示哪句）
- ✅ 字幕大小自动适配视频尺寸
- ✅ 随机 BGM（不固定同一首）
- ✅ 智能时长适配（根据脚本/图片自动计算）
- ✅ 文案安全规范（不编造敏感信息）
- ✅ 自动复制到 Windows

---

## 🚀 快速开始

### 方式 1：命令行调用

```bash
cd /home/openclaw/.openclaw/workspace/skills/ddc
python3 scripts/generate.py --images image1.jpg image2.jpg --output video.mp4
```

### 方式 2：配置文件调用

```bash
python3 scripts/generate.py --config config/custom.json
```

### 方式 3：代码参数调用

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg image3.jpg \
  --captions "文案 1" "文案 2" "文案 3" \
  --style brand \
  --voice male \
  --duration 15 \
  --output video.mp4
```

---

## 📋 参数说明

### 必填参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `--images` | list | 图片路径列表 | `image1.jpg image2.jpg` |
| `--output` | str | 输出文件路径 | `video.mp4` |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--config` | str | null | 配置文件路径 |
| `--captions` | list | null | 自定义字幕（逐行） |
| `--style` | str | "brand" | 文案风格 |
| `--voice` | str | "male" | 配音声音 |
| `--speed` | int | 5 | 语速 (4-6) |
| `--duration` | int | 0 | 视频时长 (0=自适应) |
| `--bgm-volume` | float | 0.2 | BGM 音量 (0-1) |
| `--random-bgm` | bool | true | 随机 BGM |

---

## 🎨 文案风格

### style="brand"（品牌宣传）

**特点**：无敏感信息，安全合规，自动生成行业营销用语

**电动车行业示例**：
```
安全好骑，续航长久
动力强劲，品质可靠
舒适耐用，性价比高
欢迎到店咨询体验
```

### style="promo"（促销推广）

**需要用户提供**：
- `--price` 价格
- `--promotion` 促销活动
- `--contact` 联系方式

**示例**：
```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --style promo \
  --price "2399 元" \
  --promotion "店庆大促" \
  --contact "惠水县爱玛店" \
  --captions "72V 六块大电池" "爱玛爱朵惊爆价 2399" "活动截止 4 月 30 日"
```

---

## 🎤 配音选项

### Edge TTS 声音列表

**男声**：
- `male` 或 `zh-CN-YunxiNeural` - 温暖男声（推荐）
- `zh-CN-YunjianNeural` - 沉稳男声

**女声**：
- `female` 或 `zh-CN-XiaoxiaoNeural` - 温柔女声（推荐）
- `zh-CN-XiaoyiNeural` - 活泼女声

### 语速配置

| speed | 效果 | 适用场景 |
|-------|------|---------|
| 4 | 较慢 | 详细说明 |
| 5 | 正常 | 标准视频（推荐） |
| 6 | 较快 | 快节奏视频 |

---

## 📝 字幕规范

### 逐行显示模式

**特点**：
- ✅ 说到哪句显示哪句
- ✅ 每次只显示一行
- ✅ 字体大小自动适配视频宽度
- ✅ 底部 50px 安全区
- ✅ 白字黑边，半透明背景

### 字幕配置

```json
{
  "subtitle": {
    "enabled": true,
    "fontSize": 24,
    "fontFamily": "Microsoft YaHei",
    "marginV": 50,
    "maxLines": 1,
    "position": "bottom"
  }
}
```

---

## 🎬 视频规格

### 抖音标准

| 参数 | 值 |
|------|-----|
| 分辨率 | 1080x1920 (9:16 竖屏) |
| 帧率 | 30 fps |
| 编码 | H.264 |
| 格式 | MP4 |
| 时长 | 15-60 秒（自适应） |

### 智能时长适配

**根据脚本字数自动计算**：
```
时长 (秒) = 脚本文字数 ÷ 语速 (5.5 字/秒)
```

**根据图片数量自动分配**：
```
每张图片展示时长 = 视频总时长 ÷ 图片数量
```

**示例**：
- 76 字文案 ÷ 5.5 = 约 14 秒
- 12 张图片 → 每张 1.17 秒

---

## 🎵 背景音乐

### 随机 BGM

**配置**：
```json
{
  "audio": {
    "bgm": {
      "enabled": true,
      "volume": 0.2,
      "random": true
    }
  }
}
```

### 网络 BGM

**从 Pixabay 下载免费音乐（11 首不同风格）**：
```json
{
  "audio": {
    "bgm": {
      "from_internet": true
    }
  }
}
```

**支持的来源**：
- Pixabay（免版权，可商用）

**随机选择的风格**：
- 🎵 轻快/愉悦（3 首）
- 🎵 激励/积极（2 首）
- 🎵 流行/时尚（2 首）
- 🎵 电子/动感（2 首）
- 🎵 温馨/柔和（2 首）

**每次生成都随机选择，不会重复！**

### BGM 时长匹配

**自动裁剪或循环以匹配视频时长**：
```json
{
  "audio": {
    "bgm": {
      "match_duration": true
    }
  }
}
```

**效果**：
- BGM 太长 → 自动裁剪
- BGM 太短 → 自动循环
- 最终时长 = 视频时长

### BGM 文件位置

```
/home/openclaw/.openclaw/workspace-kaifa/quick-test/out/
```

**要求**：
- MP3 格式
- 排除 TTS 文件（自动）

---

## 🚫 敏感信息规范

### 禁止自动生成的内容

- ❌ 价格（除非用户提供 `--price`）
- ❌ 地址（除非用户提供 `--address`）
- ❌ 电话/微信/QQ（除非用户提供）
- ❌ 邮箱
- ❌ 网址链接

### 安全营销用语

**电动车行业示例**：
- ✅ 安全好骑
- ✅ 续航长
- ✅ 动力强
- ✅ 品质可靠
- ✅ 性价比高
- ✅ 舒适耐用
- ✅ 欢迎咨询
- ✅ 到店体验

---

## 📁 配置文件示例

### config/default.json

```json
{
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "crf": 20
  },
  "subtitle": {
    "enabled": true,
    "fontSize": 24,
    "fontFamily": "Microsoft YaHei",
    "marginV": 50,
    "maxLines": 1
  },
  "audio": {
    "tts": {
      "voice": "male",
      "speed": 5
    },
    "bgm": {
      "enabled": true,
      "volume": 0.2,
      "random": true
    }
  },
  "script": {
    "autoGenerate": true,
    "industry": "电动车"
  },
  "output": {
    "copyToWindows": true,
    "windowsPath": "/mnt/f/Desktop/aima/新建文件夹"
  }
}
```

---

## 📚 使用示例

### 示例 1：品牌宣传（无脚本）

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg image3.jpg \
  --style brand \
  --voice male \
  --output brand_video.mp4
```

**效果**：自动生成安全版营销文案 + 男声配音

---

### 示例 2：自定义文案（有脚本）

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --captions "惠水县爱玛店庆大促" "72V 爱玛爱朵 2399 元" "截止 4 月 30 日" \
  --voice female \
  --speed 6 \
  --output promo_video.mp4
```

**效果**：按提供的文案逐行显示字幕

---

### 示例 3：促销视频（提供敏感信息）

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg image3.jpg \
  --style promo \
  --price "2399 元" \
  --promotion "店庆大促" \
  --contact "惠水县爱玛店" \
  --captions "72V 六块大电池" "爱玛爱朵惊爆价" "活动截止 4 月 30 日" \
  --voice male \
  --bgm-volume 0.25 \
  --output aima_video.mp4
```

**效果**：包含用户提供的所有信息

---

### 示例 4：配置文件调用

```bash
python3 scripts/generate.py --config config/custom.json
```

**config/custom.json**：
```json
{
  "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],
  "style": "brand",
  "voice": "male",
  "speed": 5,
  "bgm_volume": 0.2,
  "output": "video.mp4"
}
```

---

## 🔧 完整工作流

```
1. 读取参数/配置文件
   ↓
2. 生成/优化文案
   ├─ 有 captions → 使用提供的文案
   ├─ style=brand → 生成安全版营销文案
   └─ style=promo → 需要用户提供敏感信息
   ↓
3. 优化脚本字数
   └─ 根据目标时长自动增减（不改变原意）
   ↓
4. 生成 TTS 配音
   └─ Edge TTS（男声/女声可选）
   ↓
5. 生成逐行字幕
   └─ SRT 格式，一句一条
   ↓
6. 选择随机 BGM
   └─ 从指定文件夹随机选择
   ↓
7. 生成视频
   ├─ 图片处理（1080x1920）
   ├─ 字幕合成（逐行显示）
   ├─ 音频混合（TTS + BGM）
   └─ 输出 MP4
   ↓
8. 复制到 Windows（可选）
   └─ 自动复制到指定目录
```

---

## ⚠️ 注意事项

### 文案安全

**禁止编造**：
- ❌ 价格（除非 `--price`）
- ❌ 促销活动（除非 `--promotion`）
- ❌ 联系方式（除非 `--contact`）
- ❌ 地址（除非 `--address`）
- ❌ 链接/网址

**安全用语**：
- ✅ "欢迎咨询"
- ✅ "了解更多"
- ✅ "到店体验"
- ✅ "关注我们"

### 性能参考

| 时长 | 图片数 | 渲染时间 |
|------|--------|---------|
| 15 秒 | 8-12 张 | ~30 秒 |
| 20 秒 | 12-15 张 | ~45 秒 |
| 30 秒 | 15-20 张 | ~60 秒 |

### 图片要求

- 格式：JPG/PNG
- 数量：8-20 张（推荐）
- 方向：横竖皆可（自动适配）

---

## 📊 输出说明

### 生成文件

| 文件 | 说明 |
|------|------|
| `video.mp4` | 最终视频 |
| `tts.mp3` | 配音音频 |
| `subtitle.srt` | 字幕文件 |

### 输出位置

- Linux: `/home/openclaw/.openclaw/workspace/skills/video-auto/output/`
- Windows: `F:\Desktop\aima\新建文件夹\`（自动复制）

---

## 🆘 常见问题

### Q: 配音失败？
A: 检查网络连接，Edge TTS 需要访问微软服务

### Q: 字幕不显示？
A: 检查 `subtitle.enabled: true`，确认 SRT 文件存在

### Q: BGM 声音太小？
A: 调整 `--bgm-volume 0.25`

### Q: 如何切换男声/女声？
A: 使用 `--voice male` 或 `--voice female`

### Q: 如何禁用随机 BGM？
A: 使用 `--random-bgm false`

---

## 🔗 相关文档

- [配置指南](docs/config-guide.md)
- [文案安全规范](docs/safety-guide.md)
- [发布指南](docs/publish-guide.md)

---

*Last updated: 2026-04-07*
