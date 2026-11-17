# 电影解说配音

「电影解说配音」是一个把影视解说稿一键生成“解说旁白 + 多角色台词”多音色配音（WAV）、SRT 字幕和逐句时间轴的 Agent 技能，适合电影解说、短剧解说、影视解说号批量更新，本地无需显卡。

- 旁白 + 多个角色各用不同音色，一条命令出整段解说音轨
- 同时输出 SRT 字幕和逐句时间轴 JSON，剪映里按时间对画面
- 账号已有角色或参考音频声音克隆，解说号声线固定

## 安装

把本文件夹 `movie-recap-ai-voiceover/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
