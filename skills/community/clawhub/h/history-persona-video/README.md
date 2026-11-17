# history-persona-video 🎬

历史人物 AI 复原竖版短视频完整制作流程（OpenClaw Skill）

把历史人物从画像里"拉到现实中"——AI 生图 + 磁性配音 + 史诗 BGM + 大气字体卡片 + ffmpeg 合成，45-60s 竖版短视频。

已用《AI还原曹操》实测验证（v2 成品：56s / 1080×1920 / 7.8MB）。

## 功能

- 🔍 史料与古画像调研（正史线索 + Wikimedia 公有领域画像）
- 🎨 AI 生图：最终还原像 / 氛围图 / 初稿 / 诗意图（9:16 竖版 2K）
- 🎙️ TTS 磁性男声配音（MiniMax speech-2.8-hd，`male-qn-qingse`）
- 🎵 低沉史诗 BGM（music-2.5，混音压到 16%）
- 🃏 PIL 大气字体卡片（方正粗黑宋简体，3 张）
- 🎬 ffmpeg 合成：8 段时间轴 + zoompan 动效 + drawtext 字幕 + concat + 混音
- ✅ 三步质量验证（ffprobe / PIL 亮度 / volumedetect）

## 安装

```powershell
# 复制到 OpenClaw skills 目录
Copy-Item -Recurse history-persona-video ~\.openclaw\workspace\skills\
```

依赖：ffmpeg、Python 3 + Pillow、RunningHub 技能（本仓库 `skills/runninghub/`，**不附带任何 API Key**）

> ⚠️ **RunningHub API Key 需自行生成**：打开 https://www.runninghub.cn 注册账号 → 「企业API / API 管理」创建 Key → 充值 → 将 Key 配置到 `~/.openclaw/openclaw.json` 的 `skills.entries.runninghub.apiKey`（详见 `skills/runninghub/references/api-key-setup.md`）。本技能不使用、不附带任何现成或共享 Key。

## 使用

对 AI 说：**"做一期《AI还原武则天》"** 或 **"用历史人物复原流程做秦始皇"**。

## 成本参考

约 ¥0.3/条（配音 ¥0.025 + BGM ¥0.12 + 图片 4×¥0.015）

## 完整流程

见 `SKILL.md`：素材准备 → 卡片制作 → 视频合成 → 质量验证 → 交付。
