# 🎬 ddc - 抖音视频自动生成技能

## 📋 技能概述

**ddc** 是一个完整的抖音视频自动化生成技能，可将图片 + 文案自动转换为抖音标准营销视频。

---

## ✨ 核心特性

| 特性 | 说明 | 状态 |
|------|------|------|
| **图片转视频** | 自动将图片转换为 1080x1920 竖屏视频 | ✅ |
| **Edge TTS** | 支持真正的男女声配音 | ✅ |
| **逐行字幕** | 说到哪句显示哪句，每次一行 | ✅ |
| **随机 BGM** | 11 首网络音乐 + 本地音乐随机选择 | ✅ |
| **BGM 时长匹配** | 自动裁剪/循环，确保与视频时长一致 | ✅ |
| **智能时长** | 根据文案字数自动计算视频时长 | ✅ |
| **文案安全** | 不编造价格、地址等敏感信息 | ✅ |
| **自动复制** | 生成后自动复制到 Windows 目录 | ✅ |

---

## 🚀 快速开始

### 1. 准备图片

```bash
cp /path/to/images/*.jpg /home/openclaw/.openclaw/workspace/skills/ddc/temp_images/
```

### 2. 生成视频

```bash
cd /home/openclaw/.openclaw/workspace/skills/ddc
python3 scripts/generate.py --config config/default.json
```

### 3. 查看结果

```bash
# Windows 目录
F:\Desktop\aima\新建文件夹\video.mp4

# Linux 目录
output/video.mp4
```

---

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 技能完整文档 |
| [docs/USAGE.md](docs/USAGE.md) | 详细使用指南 |
| [docs/INSTALL.md](docs/INSTALL.md) | 安装与验证 |
| [docs/README.md](docs/README.md) | 快速入门 |

---

## 🎯 使用示例

### 示例 1：品牌宣传

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --style brand \
  --voice male
```

### 示例 2：自定义文案

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --captions "文案 1" "文案 2" "文案 3" \
  --voice female
```

### 示例 3：网络 BGM

```bash
python3 scripts/generate.py --config config/default.json
```

---

## ⚙️ 配置说明

### 配置文件

```json
{
  "images": ["image1.jpg", "image2.jpg"],
  "audio": {
    "tts": {"voice": "male", "speed": 5},
    "bgm": {"from_internet": true, "volume": 0.2}
  },
  "subtitle": {"enabled": true, "maxLines": 1},
  "output": {"copyToWindows": true}
}
```

### 命令行参数

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --voice male \
  --speed 5 \
  --bgm-volume 0.2 \
  --output video.mp4
```

---

## 🎵 BGM 说明

### 网络 BGM（推荐）

- **来源**：Pixabay（免版权，可商用）
- **数量**：11 首不同风格
- **特点**：每次生成随机选择，不会重复

### 本地 BGM（备用）

- **位置**：`/home/openclaw/.openclaw/workspace-kaifa/quick-test/out/`
- **特点**：网络不可用时自动使用

### BGM 时长匹配

- BGM 太长 → 自动裁剪
- BGM 太短 → 自动循环
- 最终时长 = 视频时长 + 0.5 秒余量

---

## 🎤 配音说明

### Edge TTS 声音

**男声**：
- `male` - 温暖男声（推荐）
- `zh-CN-YunjianNeural` - 沉稳男声

**女声**：
- `female` - 温柔女声（推荐）
- `zh-CN-XiaoyiNeural` - 活泼女声

### 语速

| speed | 效果 | 适用 |
|-------|------|------|
| 4 | 较慢 | 详细说明 |
| 5 | 正常 | 标准视频（推荐） |
| 6 | 较快 | 快节奏视频 |

---

## 📝 文案安全

### 禁止编造

- ❌ 价格（除非用户提供）
- ❌ 地址
- ❌ 电话/微信/QQ
- ❌ 邮箱
- ❌ 网址链接

### 安全用语

- ✅ 安全好骑
- ✅ 续航长
- ✅ 品质可靠
- ✅ 欢迎咨询
- ✅ 到店体验

---

## 📊 输出规格

| 参数 | 值 |
|------|-----|
| 分辨率 | 1080x1920 (9:16 竖屏) |
| 帧率 | 30 fps |
| 编码 | H.264 |
| 格式 | MP4 |
| 时长 | 15-60 秒（自适应） |

---

## 🆘 常见问题

**Q: 配音失败？**  
A: 检查网络，会自动切换到百度 TTS

**Q: BGM 下载失败？**  
A: 自动使用本地 BGM，不影响生成

**Q: 字幕不显示？**  
A: 检查 `subtitle.enabled: true`

**Q: 如何切换男声/女声？**  
A: 使用 `--voice male` 或 `--voice female`

---

## 📁 技能结构

```
ddc/
├── SKILL.md                 # 技能主文档
├── clawhub.json             # ClawHub 配置
├── config/                  # 配置文件
│   ├── default.json         # 默认配置
│   └── config.template.json # 配置模板
├── scripts/                 # 脚本
│   └── generate.py          # 主生成脚本
├── docs/                    # 文档
│   ├── README.md            # 快速入门
│   ├── USAGE.md             # 使用指南
│   └── INSTALL.md           # 安装说明
├── temp_images/             # 临时图片
└── output/                  # 输出目录
```

---

## 🔗 相关链接

- [SKILL.md](SKILL.md) - 完整技能文档
- [docs/USAGE.md](docs/USAGE.md) - 详细使用指南
- [docs/INSTALL.md](docs/INSTALL.md) - 安装验证

---

**版本**: 1.0.0  
**作者**: openclaw  
**许可**: MIT

---

*Last updated: 2026-04-07*
