# MS-ai (ModelScope AI)

ModelScope AI 技能：生图、改图、析图、生文。遇到限速自动轮换模型。

## 功能

- 🎨 **文生图** — 文字描述生成图片
- 🖼️ **图生图** — 上传图片进行修改
- 👁️ **视觉理解** — 分析图片内容、OCR
- 💬 **文本生成** — 多模型对话

## 配置

在 `~/.openclaw/openclaw.json` 中设置 API Key：

```json
{
  "skills": {
    "entries": {
      "ms-ai": {
        "enabled": true,
        "env": {
          "MODELSCOPE_API_KEY": "your-key"
        }
      }
    }
  }
}
```

## 快速使用

```bash
# 生图
python3 scripts/generate.py --prompt "一只金色的猫" --output cat.jpg

# 析图
python3 scripts/vision.py --image photo.jpg --prompt "描述这张图片"
```

## 安装

```bash
npx clawhub install ms-ai
```

## 许可证

MIT
