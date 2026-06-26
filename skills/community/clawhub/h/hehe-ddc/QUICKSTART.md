# ddc 技能 - 快速使用卡片

## 📦 技能名称

**ddc** (原 video-auto)

---

## 📍 技能位置

```
/home/openclaw/.openclaw/workspace/skills/ddc/
```

---

## 🚀 快速使用

### 方式 1：配置文件（推荐）

```bash
cd /home/openclaw/.openclaw/workspace/skills/ddc
python3 scripts/generate.py --config config/default.json
```

### 方式 2：命令行

```bash
python3 scripts/generate.py \
  --images /path/to/images/*.jpg \
  --voice male \
  --output video.mp4
```

---

## ⚙️ 配置说明

### 必须修改的配置

编辑 `config/default.json`：

```json
{
  "images": [
    "/path/to/image1.jpg",  // ← 改成你的图片路径
    "/path/to/image2.jpg"
  ]
}
```

### 可选配置

```json
{
  "audio": {
    "tts": {"voice": "male"},    // male 或 female
    "bgm": {"volume": 0.2}       // BGM 音量 0-1
  },
  "subtitle": {"enabled": true}, // 是否启用字幕
  "output": {"copyToWindows": true}
}
```

---

## 📁 输出位置

- **Linux**: `output/video.mp4`
- **Windows**: `F:\Desktop\aima\新建文件夹\video.mp4`

---

## 🎯 核心功能

- ✅ 图片转视频（1080x1920 竖屏）
- ✅ Edge TTS 男女声
- ✅ 逐行字幕
- ✅ 随机 BGM（11 首网络音乐）
- ✅ BGM 时长自动匹配
- ✅ 智能时长适配
- ✅ 文案安全规范

---

## 📚 完整文档

- [SKILL.md](SKILL.md) - 技能完整文档
- [README.md](README.md) - 快速入门
- [docs/USAGE.md](docs/USAGE.md) - 详细使用指南
- [docs/INSTALL.md](docs/INSTALL.md) - 安装验证

---

## 💡 使用示例

```bash
# 1. 准备图片
cp /path/to/images/*.jpg temp_images/

# 2. 修改配置
# 编辑 config/default.json 中的 images 数组

# 3. 生成视频
python3 scripts/generate.py --config config/default.json

# 4. 查看结果
ls -lh output/video.mp4
```

---

**版本**: 1.0.0  
**名称**: ddc  
**作者**: openclaw
