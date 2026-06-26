# ddc 使用指南

## 🚀 快速开始

### 1. 准备图片

将图片放入 `temp_images/` 目录：

```bash
cp /path/to/images/*.jpg /home/openclaw/.openclaw/workspace/skills/ddc/temp_images/
```

### 2. 修改配置

编辑 `config/default.json`：

```json
{
  "images": ["/path/to/image1.jpg", ...],
  "script": {
    "content": "你的文案"
  },
  "audio": {
    "tts": {
      "voice": "male"
    }
  }
}
```

### 3. 生成视频

```bash
cd /home/openclaw/.openclaw/workspace/skills/ddc
python3 scripts/generate.py --config config/default.json
```

### 4. 查看结果

- Linux: `output/video.mp4`
- Windows: `F:\Desktop\aima\新建文件夹\video.mp4`

---

## 📋 完整参数

```bash
python3 scripts/generate.py \
  --images image1.jpg image2.jpg \
  --output video.mp4 \
  --captions "文案 1" "文案 2" \
  --style brand \
  --voice male \
  --speed 5 \
  --bgm-volume 0.2
```

---

## 🎤 配音说明

**Edge TTS**（优先）：
- 男声：`male` 或 `zh-CN-YunxiNeural`
- 女声：`female` 或 `zh-CN-XiaoxiaoNeural`

**百度 TTS**（备用）：
- 只有女声
- 网络不好时自动切换

---

## 📝 文案规范

**安全用语**：
- ✅ 安全好骑
- ✅ 续航长
- ✅ 品质可靠

**禁止编造**：
- ❌ 价格（除非提供 `--price`）
- ❌ 地址
- ❌ 电话/微信

---

*Last updated: 2026-04-07*
