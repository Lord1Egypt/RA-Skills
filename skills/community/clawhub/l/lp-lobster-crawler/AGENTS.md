# AGENTS

完整项目规范见 `CLAUDE.md`，Codex 最小上下文见 `agent.md`。

执行前请阅读：
- `CLAUDE.md`
- `agent.md`
- `docs/TODO.md`
- `docs/STATE.md`
- `docs/FEEDBACK.md`

## 项目一句话定位

"龙虾"平台网络内容爬取技能 — 定向抓取 Webnovel/ReelShorts 等站点，沉淀站点地图，支持定时调度、内容分级与钉钉播报。

## 当前技术基线

- **Language**: Python 3.11+
- **Crawler**: Scrapy 2.11+
- **Storage**: SQLite (MVP) → PostgreSQL
- **Scheduler**: APScheduler
- **Broadcast**: DingTalk Webhook
- **CLI**: click
- **Config**: YAML + env vars
- **Pipeline**: claude_loop.sh → claude -p → JSON output
