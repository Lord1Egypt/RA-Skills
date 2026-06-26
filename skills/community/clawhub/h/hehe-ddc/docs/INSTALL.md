# ddc 安装与验证

## 📦 技能位置

```
/home/openclaw/.openclaw/workspace/skills/ddc/
```

---

## ✅ 技能结构

```
ddc/
├── SKILL.md                 # 技能主文档
├── clawhub.json             # 技能配置（ClawHub 格式）
├── config/
│   ├── default.json         # 默认配置
│   └── config.template.json # 配置模板
├── scripts/
│   └── generate.py          # 主生成脚本
├── docs/
│   ├── README.md            # 快速入门
│   ├── USAGE.md             # 完整使用指南
│   └── INSTALL.md           # 安装说明（本文件）
├── temp_images/             # 临时图片目录
└── output/                  # 输出目录
    ├── video.mp4            # 生成的视频
    ├── tts.mp3              # 配音
    ├── bgm_adjusted.mp3     # 调整后的 BGM
    └── subtitle.srt         # 字幕
```

---

## 🔧 环境要求

### Python 3.8+

```bash
python3 --version
```

### 必需包

```bash
pip3 install edge-tts aiohttp requests
```

### 系统依赖

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# 验证
ffmpeg -version
```

---

## ✅ 验证安装

### 1. 检查技能文件

```bash
ls -la /home/openclaw/.openclaw/workspace/skills/video-auto/
```

**应包含**：
- ✅ SKILL.md
- ✅ clawhub.json
- ✅ scripts/generate.py
- ✅ config/default.json
- ✅ docs/ 目录

### 2. 测试生成

```bash
cd /home/openclaw/.openclaw/workspace/skills/ddc
python3 scripts/generate.py --config config/default.json
```

**成功输出**：
```
============================================================
🎬 抖音视频生成脚本 - 融合版
============================================================
📸 找到 5 张图片
📝 使用配置文件文案
...
✅ 视频生成成功：output/video.mp4
✅ 已复制到 Windows: /mnt/f/Desktop/aima/新建文件夹/video.mp4
```

### 3. 验证视频

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output/video.mp4
```

**应输出**：视频时长（如 `16.680000`）

---

## 🚀 快速测试

### 测试 1：使用默认配置

```bash
python3 scripts/generate.py --config config/default.json
```

### 测试 2：使用命令行参数

```bash
python3 scripts/generate.py \
  --images temp_images/*.jpg \
  --voice male \
  --output test_video.mp4
```

### 测试 3：自定义文案

```bash
python3 scripts/generate.py \
  --images temp_images/*.jpg \
  --captions "文案 1" "文案 2" "文案 3" \
  --voice female \
  --output custom_video.mp4
```

---

## 🔍 故障排除

### 问题 1：找不到图片

**错误**：
```
📸 找到 0 张图片
❌ 未找到图片！
```

**解决**：
```bash
# 检查图片目录
ls temp_images/

# 添加图片
cp /path/to/images/*.jpg temp_images/
```

### 问题 2：Edge TTS 失败

**错误**：
```
⚠️ Edge TTS 失败，切换到百度 TTS...
```

**说明**：网络问题，会自动切换到百度 TTS（女声）

**解决**：
- 检查网络连接
- 或使用百度 TTS（自动切换）

### 问题 3：BGM 下载失败

**错误**：
```
❌ HTTP 错误：403
```

**说明**：Pixabay 服务器限制

**解决**：
- 自动使用本地 BGM
- 或使用已下载的网络 BGM

### 问题 4：ffmpeg 未找到

**错误**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**解决**：
```bash
sudo apt-get install ffmpeg
```

---

## 📊 技能功能清单

### 核心功能

- [x] 图片转视频
- [x] Edge TTS 男女声
- [x] 逐行字幕
- [x] 随机 BGM
- [x] 网络 BGM 下载
- [x] BGM 时长匹配
- [x] 智能时长适配
- [x] 文案安全规范
- [x] 自动复制 Windows

### 配置选项

- [x] 配置文件支持
- [x] 命令行参数
- [x] 多风格文案
- [x] 多声音选择
- [x] BGM 音量控制
- [x] 字幕样式配置
- [x] 视频规格配置

### 安全特性

- [x] 不编造价格
- [x] 不编造地址
- [x] 不编造联系方式
- [x] 自动生成安全文案
- [x] 敏感信息检测

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能主文档
- [USAGE.md](USAGE.md) - 完整使用指南
- [README.md](README.md) - 快速入门
- [config.template.json](../config/config.template.json) - 配置模板

---

## 🎯 下一步

1. ✅ 验证安装完成
2. 📖 阅读 [USAGE.md](USAGE.md) 了解详细用法
3. 🎬 尝试生成第一个视频
4. ⚙️ 根据需求调整配置

---

*Last updated: 2026-04-07*
