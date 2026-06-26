# Project Onboarding Checklist

Use this checklist when bootstrapping a new content-pipeline project. Work through items in order. Complete each before moving to the next.

---

## Pre-flight (Human Tasks — Before Skill Runs)

- [ ] 确定项目方向和目标（内容类型、数据来源）
- [ ] 准备 Telegram Bot Token（从 @BotFather 获取）
- [ ] 创建或确认 Telegram 项目群，获取 chat_id
- [ ] 在项目中创建几个基础 Thread，获取 thread IDs
- [ ] 确认数据来源（YouTube channel IDs / RSS URLs / API endpoints）
- [ ] 确认是否需要微信发布（若是，准备 Clash 节点配置）

---

## Stage 1: Skill Trigger

- [ ] 调用 `content-pipeline` skill
- [ ] 填写问卷（project_key, bot_token, chat_id, thread_ids, sources, cron schedule）
- [ ] 确认所有必填项已填写

---

## Stage 2: Project Structure Generation

The bootstrap script creates:

- [ ] `PROJECT.md` — 项目定义文档
- [ ] `AGENTS.md` — Agent 角色（Chief, Download/Content Bot, Publish Bot）
- [ ] `IDENTITY.md` — 项目身份
- [ ] `USER.md` — 用户角色
- [ ] `SOUL.md` — 项目叙事风格（影响内容改写 tone）
- [ ] `TOOLS.md` — 工具配置（yt-dlp / curl / ffmpeg 等）
- [ ] `HEARTBEAT.md` — 心跳监控配置
- [ ] `WORKFLOW.md` — 工作流步骤定义
- [ ] `BOOTSTRAP.md` — 本清单

---

## Stage 3: Data & Source Configuration

- [ ] `sources.json` — 确认来源列表（channel IDs / URLs）
- [ ] `brand_map.json` — 品牌映射（中文名、英文名、别名）
- [ ] `style-guide.md` — 内容风格指南（影响 rewrite 输出质量）

---

## Stage 4: Routing & Delivery Config

- [ ] `config/project_routing.json` — 新增 routing 条目（chat_id, thread_id mapping, syncToMain）
- [ ] 确认 shared `config/project_routing.json` 已更新
- [ ] 在 Telegram 项目群里 @Bot 发一条消息，确认 bot 能正常收发

---

## Stage 5: Scripts Verification

- [ ] 跑 `python3 scripts/<project>_bot.py` — 确认数据能抓取
- [ ] 跑 `python3 scripts/run_pipeline.sh` — 确认全链能跑通
- [ ] 跑 `python3 scripts/pipeline_reporter.py` — 确认报告能发送到正确 thread
- [ ] 跑 `bash scripts/telegram_broadcast_smoke_test.py` — 烟雾测试

---

## Stage 6: Cron Registration

- [ ] 确认 cron job 已注册（`openclaw cron list` 查看）
- [ ] 确认 cron schedule 正确（`0 9 * * *` 等）
- [ ] 确认 cron delivery 目标为项目群 chat_id，不是主人主 chat

---

## Stage 7: Error & Edge Case Planning

- [ ] 数据源 404 或内容 gone — 是否需要 cache/fallback？
- [ ] Bot Token 失效 — 是否有监控？
- [ ] Thread ID 过期（Telegram group → supergroup）— 预案是？
- [ ] WeChat IP 白名单变化 — 预案是？
- [ ] 连续失败超过 N 次 — 是否需要 escalation？

---

## Stage 8: Memory & Knowledge

- [ ] 在 `MEMORY.md` 新增项目条目
- [ ] 在 `AGENTS.md` 新增项目到团队结构
- [ ] 通知主人项目已初始化完成，等待首次 cron 运行验证

---

## Post-Init（首次 Cron 运行后）

- [ ] 检查 `logs/latest_run_summary.json` 是否生成
- [ ] 检查 Telegram 项目群 thread 是否有报告送达
- [ ] 若有问题：查看 `logs/daily_pipeline.log` 定位
- [ ] 若正常：在 `memory/YYYY-MM-DD.md` 记录本次初始化经验

---

## Stage 9: Infrastructure Scripts Verification

After bootstrapping, verify all infrastructure scripts exist and are functional:

- [ ] `scripts/run_pipeline.sh` — contains `finish()` trap
- [ ] `scripts/self_check.py` — run with `python3 scripts/self_check.py`, should pass all checks
- [ ] `scripts/upgrade_project.py` — run with `python3 scripts/upgrade_project.py --dry-run` to verify upgrade path
- [ ] `scripts/update_memory.py` — run to scaffold today's memory entry
- [ ] `scripts/pipeline_reporter.py` — sends to correct thread (check routing config)

## Stage 10: Upgrade Path

When the project-factory skill is updated (new conventions, new scripts), upgrade existing projects:

```bash
python3 scripts/upgrade_project.py
python3 scripts/upgrade_project.py --dry-run  # preview changes first
```

Always run with `--dry-run` first to see what would change.
