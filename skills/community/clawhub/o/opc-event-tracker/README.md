# OPC赛事活动追踪 · WorkBuddy Skill

追踪 OPC/AI/独立开发者相关赛事活动。从信息源抓取 → 提取结构化信息 → 提交到 OPC 公共赛事池。安装时引导用户获取 API Key。触发词：赛事、比赛、hackathon、活动、OPC赛事、AI比赛、独立开发者大赛、收录赛事、加到OPC

## 特性

- 🔍 多平台赛事信息源抓取（TRAE、Kaggle、Devpost 等）
- 🧠 智能字段推断（type/region/deadline 自动识别）
- 🌐 一键提交到 OPC 公共赛事池
- ⏰ 支持定时任务自动追踪
- 📊 本地 Markdown 记录 + 结构化 JSON 历史

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「OPC赛事活动追踪」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/workbuddy-event-tracker.git \
  ~/.workbuddy/skills/OPC赛事活动追踪
```

## 使用

```bash
# 手动运行赛事追踪（需先通过对话引导设置 API Key）
python3 scripts/track_events.py
```

首次安装后，在 WorkBuddy 中对 AI 说「收录赛事」或提供赛事链接，AI 会自动提取信息并提交到 OPC 公共赛事池。

## 输出

运行后在 `scripts/data/赛事记录.md` 中查看结构化赛事记录，或在 `scripts/events_history.json` 中查看完整 JSON 数据。

## 项目结构

```
.gitignore
LICENSE
SKILL.md
references
references/api-spec.md
references/platform-spec.md
references/sources-mgmt.md
references/templates.md
scripts
scripts/data
scripts/data/赛事记录.md
scripts/events_history.json
scripts/last_run_summary.json
scripts/sources.json
scripts/track_events.py
scripts/user_config.json
```

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」|
| 💬 公众号 | 微信搜「桂皮AI实战」|
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) — AI工具 · 创作 · 产品 · 流量 · 变现 |
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意）|

## License

MIT License — 详见 [LICENSE](./LICENSE)
