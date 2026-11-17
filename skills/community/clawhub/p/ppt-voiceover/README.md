# PPT配音

「PPT配音」是一个把 PPT 或课件每一页的讲稿逐页配音、自动拼成整段旁白并输出 SRT 字幕和每页时长的 Agent 技能，配合 ffmpeg 可把导出的幻灯片图片合成讲解视频，本地无需显卡。

- 一个讲稿文件按 `=== 第1页 ===` 分页，一条命令逐页配音
- 每页 WAV + SRT，整段 narration.wav / narration.srt，每页起止时间 slides.json
- concat.txt 直接给 ffmpeg 把幻灯片图片按配音时长合成视频；改一页只重配改动的句子

## 安装

把本文件夹 `ppt-voiceover-narration/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
