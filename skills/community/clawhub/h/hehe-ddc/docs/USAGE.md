# ddc 完整使用指南

## 🎯 技能概述

**ddc** 是一个完整的抖音视频自动化生成技能，支持：

- 📸 图片 → 视频自动转换
- 🎤 Edge TTS 男女声配音
- 📝 逐行字幕（说到哪句显示哪句）
- 🎵 随机 BGM（11 首网络音乐 + 本地音乐）
- ⏱️ 智能时长适配
- 📱 抖音标准规格（1080x1920）
- 💾 自动复制到 Windows

---

## 🚀 快速开始

### 1️⃣ 准备图片

将图片放入 `temp_images/` 目录：

```bash
cp /path/to/your/images/*.jpg /home/openclaw/.openclaw/workspace/skills/ddc/temp_images/
```

### 2️⃣ 修改配置

编辑 `config/default.json`：

```json
{
  "images": [
    "/path/to/image1.jpg",
    "/path/to/image2.jpg"
  ],
  "script": {
    "content": "你的营销文案"
  },
  "audio": {
    "tts": {
      "voice": "male"
    },
    "bgm": {
      "from_internet": true
    }
  }
}
```

### 3️⃣ 生成视频

```bash
cd /home/openclaw/.openclaw/workspace/skills/ddc
python3 scripts/generate.py --config config/default.json
```

### 4️⃣ 查看结果

- **Linux**: `output/video.mp4`
- **Windows**: `F:\Desktop\aima\新建文件夹\video.mp4`

---

## 📋 完整参数说明

### 命令行参数

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg image3.jpg \
  --output video.mp4 \
  --config config/custom.json \
  --captions "文案 1" "文案 2" "文案 3" \
  --style brand \
  --voice male \
  --speed 5 \
  --duration 0 \
  --bgm-volume 0.2 \
  --random-bgm true
```

### 参数详解

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--images` | list | 必填 | 图片路径列表 |
| `--output` | str | video.mp4 | 输出文件名 |
| `--config` | str | null | 配置文件路径 |
| `--captions` | list | null | 自定义字幕（逐行） |
| `--style` | str | brand | 文案风格 |
| `--voice` | str | male | 配音声音 |
| `--speed` | int | 5 | 语速 (4-6) |
| `--duration` | int | 0 | 视频时长 (0=自适应) |
| `--bgm-volume` | float | 0.2 | BGM 音量 (0-1) |
| `--random-bgm` | bool | true | 随机 BGM |

---

## 🎨 文案配置

### 方式 1：提供完整文案

```json
{
  "script": {
    "autoGenerate": false,
    "content": "惠水县爱玛店庆大促！72V 六块大电池，爱玛爱朵惊爆价 2399！"
  }
}
```

### 方式 2：自动生成（品牌宣传）

```json
{
  "script": {
    "autoGenerate": true,
    "industry": "电动车"
  }
}
```

### 方式 3：命令行提供

```bash
--captions "文案 1" "文案 2" "文案 3"
```

---

## 🎤 配音配置

### Edge TTS 声音

**男声**：
- `male` 或 `zh-CN-YunxiNeural` - 温暖男声（推荐）
- `zh-CN-YunjianNeural` - 沉稳男声

**女声**：
- `female` 或 `zh-CN-XiaoxiaoNeural` - 温柔女声（推荐）
- `zh-CN-XiaoyiNeural` - 活泼女声

### 语速配置

```json
{
  "audio": {
    "tts": {
      "voice": "male",
      "speed": 5
    }
  }
}
```

| speed | 效果 | 适用场景 |
|-------|------|---------|
| 4 | 较慢 | 详细说明 |
| 5 | 正常 | 标准视频（推荐） |
| 6 | 较快 | 快节奏视频 |

---

## 🎵 BGM 配置

### 网络 BGM（推荐）

```json
{
  "audio": {
    "bgm": {
      "from_internet": true,
      "random": true,
      "match_duration": true
    }
  }
}
```

**支持的来源**：
- Pixabay（11 首不同风格，免版权）
- 随机选择，每次生成可能不同

### 本地 BGM

```json
{
  "audio": {
    "bgm": {
      "from_internet": false
    }
  }
}
```

**BGM 文件位置**：
```
/home/openclaw/.openclaw/workspace-kaifa/quick-test/out/
```

### BGM 音量

```json
{
  "audio": {
    "bgm": {
      "volume": 0.2
    }
  }
}
```

| 音量 | 效果 |
|------|------|
| 0.1 | 很轻，几乎听不到 |
| 0.2 | 轻柔，不盖过配音（推荐） |
| 0.3 | 清晰，但不影响配音 |
| 0.5+ | 太大，可能盖过配音 |

---

## 📝 字幕配置

### 逐行字幕

```json
{
  "subtitle": {
    "enabled": true,
    "fontSize": 24,
    "fontFamily": "Microsoft YaHei",
    "marginV": 50,
    "maxLines": 1
  }
}
```

**特点**：
- ✅ 说到哪句显示哪句
- ✅ 每次只显示一行
- ✅ 字体大小自动适配
- ✅ 底部 50px 安全区
- ✅ 白字黑边，半透明背景

### 禁用字幕

```json
{
  "subtitle": {
    "enabled": false
  }
}
```

---

## 🎬 视频规格

### 抖音标准

```json
{
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "crf": 20
  }
}
```

| 参数 | 值 | 说明 |
|------|-----|------|
| 分辨率 | 1080x1920 | 9:16 竖屏 |
| 帧率 | 30 fps | 标准帧率 |
| 编码 | H.264 | 兼容性最好 |
| 格式 | MP4 | 通用格式 |
| CRF | 20 | 高质量（0-51，越小越好） |

### 智能时长

```json
{
  "duration": {
    "mode": "auto",
    "minSeconds": 15,
    "maxSeconds": 60
  }
}
```

**自动计算逻辑**：
```
时长 (秒) = 脚本文字数 ÷ 语速 (5.5 字/秒)
每张图片展示时长 = 视频总时长 ÷ 图片数量
```

---

## 💾 输出配置

### 自动复制到 Windows

```json
{
  "output": {
    "copyToWindows": true,
    "windowsPath": "/mnt/f/Desktop/aima/新建文件夹"
  }
}
```

### 禁用自动复制

```json
{
  "output": {
    "copyToWindows": false
  }
}
```

---

## 📚 使用示例

### 示例 1：品牌宣传视频

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg image3.jpg \
  --style brand \
  --voice male \
  --output brand_video.mp4
```

**效果**：自动生成安全版营销文案 + 男声配音

---

### 示例 2：促销视频

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --captions "店庆大促" "惊爆价 2399" "截止 4 月 30 日" \
  --voice female \
  --speed 6 \
  --output promo_video.mp4
```

**效果**：按提供的文案逐行显示字幕

---

### 示例 3：网络 BGM 视频

```json
{
  "audio": {
    "tts": {
      "voice": "male"
    },
    "bgm": {
      "from_internet": true,
      "volume": 0.2
    }
  }
}
```

**效果**：随机下载网络 BGM + 自动裁剪时长

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

## ⚠️ 注意事项

### 文案安全

**禁止编造**：
- ❌ 价格（除非用户提供）
- ❌ 促销活动（除非用户提供）
- ❌ 联系方式（除非用户提供）
- ❌ 地址（除非用户提供）
- ❌ 链接/网址

**安全用语**：
- ✅ "欢迎咨询"
- ✅ "了解更多"
- ✅ "到店体验"
- ✅ "关注我们"

### 图片要求

- 格式：JPG/PNG
- 数量：5-20 张（推荐）
- 方向：横竖皆可（自动适配）

### 性能参考

| 图片数 | 时长 | 渲染时间 |
|--------|------|---------|
| 5 张 | 15-20 秒 | ~30 秒 |
| 10 张 | 20-30 秒 | ~45 秒 |
| 15 张 | 30-45 秒 | ~60 秒 |

---

## 🆘 常见问题

### Q: 配音失败？
A: 检查网络连接，Edge TTS 需要访问微软服务。网络不好时会自动切换到百度 TTS。

### Q: 字幕不显示？
A: 检查 `subtitle.enabled: true`，确认 SRT 文件存在。

### Q: BGM 声音太小？
A: 调整 `bgm_volume` 到 0.25-0.3。

### Q: 如何切换男声/女声？
A: 使用 `--voice male` 或 `--voice female`。

### Q: 如何禁用随机 BGM？
A: 使用 `--random-bgm false`。

### Q: 网络 BGM 下载失败？
A: 会自动切换到本地 BGM，不影响视频生成。

---

## 🔗 相关文档

- [SKILL.md](../SKILL.md) - 技能主文档
- [README.md](README.md) - 快速入门
- [config.template.json](../config/config.template.json) - 配置模板

---

**Skill 名称**: ddc  
**版本**: 1.0.0

---

*Last updated: 2026-04-07*
