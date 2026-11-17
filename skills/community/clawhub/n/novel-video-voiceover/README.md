# 小说推文配音

「小说推文配音」是一个把小说推文文案、网文章节和故事按旁白与角色分配不同音色、一键生成整段多角色 AI 配音（WAV）和带角色名 SRT 字幕的 Agent 技能，适合小说推文视频、有声书配音和故事号，本地无需显卡。

- 旁白 + 每个角色一个音色，一条命令生成整段多角色配音
- SRT 字幕自带角色名、逐句时间轴可用来切换配图，直接做小说推文视频
- 也能做有声书配音；声音克隆固定旁白声线

## 安装

把本文件夹 `novel-video-voiceover/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
