# MiniMax AI 音乐生成技能

使用 MiniMax API 生成歌词、合成歌曲的 AI Agent 技能，支持纯音乐和人声歌曲。

## 功能

- 🎵 **歌词生成** — 输入主题，自动生成带结构的完整歌词
- 🎶 **歌曲合成** — 歌词+风格描述 → 完整歌曲 MP3
- 🎹 **纯音乐生成** — 钢琴、电子、国风、史诗等纯音乐
- 🔗 **批量合并** — FFmpeg 合并多首生成长曲目
- 🖼️ **封面图生成** — 同步使用 image-01 模型生成商品封面

## 快速开始

### 前置条件

- MiniMax API Key（Token Plan 用户可用 `sk-cp-F-...` Key）
- Python 3.x + `requests`
- `ffmpeg`（用于合并曲目）

### 安装

```bash
# 克隆仓库
git clone https://github.com/838997125/minimax-music-skill.git
cd minimax-music-skill

# 安装依赖
pip install requests
```

### 使用

```bash
# 生成纯音乐
python scripts/generate.py --prompt "欢快的流行音乐" --name "01_欢快" --save "./output"

# 生成带歌词歌曲（自动先歌词后歌曲）
python scripts/generate.py --lyrics-prompt "给朋友加油打气的励志歌曲" --song-title "加油歌" --prompt "流行励志" --name "加油歌" --save "./output"

# 合并多首曲目
python scripts/generate.py --merge "song1.mp3" "song2.mp3" "song3.mp3" --output "merged.mp3"
```

## API 文档

详见 [references/api.md](references/api.md)

## 支持的风格

| 类型 | 示例关键词 |
|------|-----------|
| 中文 | 古风、摇滚、流行、爵士、电子、民谣、抒情 |
| 情绪 | 欢快、治愈、热血、史诗、梦幻、轻松、励志、浪漫 |
| 英文 | Mandopop, Rock, Jazz, Ambient, Chill, Dreamy, Anthemic |

## 适用场景

- 短视频 BGM 定制
- 个人/商用音乐创作
- 有声内容制作
- 催眠/氛围音乐生成
- 歌词歌曲创作

## 文件结构

```
minimax-music/
├── SKILL.md              # OpenClaw 技能入口
├── scripts/
│   └── generate.py       # 可执行脚本
└── references/
    └── api.md            # API 参考文档
```

## 注意事项

- 音乐生成 API 单次上限约 5 分钟（157-200 秒），超时建议设为 600 秒
- 音频下载 URL 有效期 **24 小时**，生成后请及时下载
- Token Plan 每 5 小时刷新 100 次额度

## License

MIT
