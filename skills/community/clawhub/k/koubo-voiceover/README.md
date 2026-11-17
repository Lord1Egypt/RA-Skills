# 口播配音

「口播配音」是一个把口播稿一键变成本人克隆声音配音（WAV）和竖屏字幕（SRT）的 Agent 技能，适合每天更新的知识、财经、情感口播视频：音色用你的参考音频或账号里已复刻的角色，改一句只重配一句。

- 用你自己的参考音频或已复刻角色当口播音色，之后只写稿不录音
- 一条命令输出配音 WAV + 竖屏 SRT 字幕 + 逐句时间轴 JSON
- 改一句只重配一句；语气标签、语速可调；本地无需显卡

## 安装

把本文件夹 `koubo-ai-voiceover/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
