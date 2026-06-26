---
name: new-year-fortune
description: 生成 2026 马年新年签运视频。主输出为 MP4，HTML 仅作为视频截图和预览的中间资产。
dependency:
  python:
    - imageio-ffmpeg>=0.5.0
    - requests>=2.28.0
    - imgkit>=1.2.0
    - selenium>=4.0.0
    - webdriver-manager>=4.0.0
    - playwright>=1.40.0
---

# 新年签运视频生成 Skill

## 任务目标

本 Skill 用于根据用户输入的姓名、性别、出生日期、性格、祈愿等信息，生成一条可分享的 **2026 马年新年签运 MP4 视频**。

核心能力包括：

- AI 运势推演
- 新年祈福金榜 HTML 页面生成，作为视频画面素材
- 新春插画背景生成
- TTS 语音解说生成
- 背景音乐混音
- 签运 MP4 视频合成

> 注意：本 Skill 的主输出是 `new_year_blessing_video.mp4`。  
> `new_year_blessing.html` 是中间文件 / 预览文件，不是最终主结果。

适合在用户提出以下需求时触发：

- “帮我抽一个新年签，并生成视频”
- “生成一个新年祈福视频”
- “根据我的信息推一下 2026 年运势，做成可分享视频”
- “做一个新年签运短视频”

---

## 文件结构

```text
new-year-fortune/
├── SKILL.md
├── scripts/
│   └── happynewyear.py
└── assets/
    ├── chinese-new-year.mp3
    └── new-year.mp3