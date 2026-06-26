# STATE

> 项目进度追踪。每轮任务结束后由 Agent 更新。

---

## Overview

| 字段            | 值          |
| --------------- | ----------- |
| Current Phase   | ALL DONE    |
| Last Completed  | T503        |
| Active Task     | —           |
| Next Task       | —           |
| Total Completed | 19 / 19     |

---

## Repository Baseline

- **语言**: Python 3.11+
- **爬虫框架**: Scrapy 2.11+
- **存储**: SQLite (MVP)
- **调度**: APScheduler
- **播报**: 钉钉 Webhook
- **CLI**: click
- **配置**: YAML + 环境变量
- **依赖**: requirements.txt
- **入口**: src/cli.py

---

## Blockers

> 当前阻碍推进的关键缺失。清除后移除对应条目。

（暂无）

---

## Active Task

> 全部 19 个任务已完成（Phase A–E）。项目进入可运行状态。

---

## Phase Progress

### Phase A — 基础骨架

| TODO | 描述                          | 状态    |
| ---- | ----------------------------- | ------- |
| T101 | 项目初始化                    | done |
| T102 | 数据模型                      | done |
| T103 | 配置系统                      | done |
| T104 | 站点地图模块                  | done |
| T105 | 基础爬虫框架                  | done |

### Phase B — 站点适配

| TODO | 描述                          | 状态    |
| ---- | ----------------------------- | ------- |
| T201 | Webnovel 站点配置             | done |
| T202 | Webnovel Spider               | done |
| T203 | ReelShorts 站点配置           | done |
| T204 | ReelShorts Spider             | done |

### Phase C — 调度与分级

| TODO | 描述                          | 状态    |
| ---- | ----------------------------- | ------- |
| T301 | 定时调度系统                  | done |
| T302 | 内容分级引擎                  | done |
| T303 | 增量更新与去重                | done |

### Phase D — 播报与接口

| TODO | 描述                          | 状态    |
| ---- | ----------------------------- | ------- |
| T401 | 消息模板系统                  | done |
| T402 | 钉钉机器人集成                | done |
| T403 | RSS 订阅源                    | done |
| T404 | CLI 入口                      | done |

### Phase E — 运维与健壮性

| TODO | 描述                          | 状态    |
| ---- | ----------------------------- | ------- |
| T501 | 日志与监控                    | done |
| T502 | 反爬增强                      | done |
| T503 | Docker 化部署                 | done |

---

## Completed Task Log

> 逆序记录。每条包含：任务 ID、摘要、变更文件。

- **T503** — Docker 化部署：Dockerfile + docker-compose.yaml（scheduler/crawler/rss 三服务）
- **T502** — 反爬增强：ProxyMiddleware 代理池接口 + 扩展 UA 池 + 429 降速检测
- **T501** — 日志与监控：structlog 结构化日志 + CrawlStats 统计收集器。`src/logging_config.py`
- **T404** — CLI 入口：6 个子命令（crawl/list/status/broadcast/schedule/rss）。`src/cli.py`
- **T403** — RSS 订阅源：FeedGenerator RSS/Atom 输出 + 站点/分级过滤。`src/rss.py`
- **T402** — 钉钉机器人：Markdown 消息 + HMAC-SHA256 签名 + 3 次重试。`src/broadcast/dingtalk.py`
- **T401** — 消息模板：即时/日汇总/周汇总 Jinja2 模板 + 分级策略。`src/broadcast/templates.py`
- **T303** — 增量去重：IncrementalChecker DB 级去重。`src/spiders/dupefilter.py`
- **T302** — 内容分级：更新频率 + 近期内容量 → high/medium/low。`src/classifier/grader.py`
- **T301** — 定时调度：APScheduler BackgroundScheduler + 从 YAML 自动注册。`src/scheduler/manager.py`
- **T204** — ReelShorts Spider：web/api 双模式 stub。`src/spiders/reelshorts.py`
- **T203** — ReelShorts 站点配置：API 推测 + 字段映射。`config/sites/reelshorts.yaml`
- **T202** — Webnovel Spider：排行榜 → 详情 → 章节列表 → 正文。`src/spiders/webnovel.py`
- **T201** — Webnovel 站点配置：URL/选择器/API 字段映射。`config/sites/webnovel.yaml`
- **T105** — 基础爬虫框架：BaseSpider + Item/Pipeline/Middleware 骨架，27 tests pass
- **T104** — 站点地图模块：JSON 格式 sitemap CRUD 接口。`src/sitemap/generator.py`
- **T103** — 配置系统：YAML 加载 + 环境变量覆盖 + 缓存。`src/config.py`
- **T102** — 数据模型：Novel/Chapter/Episode ORM + SQLite 初始化。`src/models/{database,novel}.py`
- **T101** — 项目初始化：目录结构 + pyproject.toml + requirements.txt + scrapy.cfg

---

## Architecture Decisions

> 关键技术决策记录。

| 决策         | 选择              | 理由                                   |
| ------------ | ----------------- | -------------------------------------- |
| 爬虫框架     | Scrapy 2.11+      | 成熟、生态完善、支持分布式             |
| 语言         | Python 3.11+      | Scrapy 生态                            |
| 存储         | SQLite (MVP)      | 轻量启动，后续可升级 PostgreSQL        |
| 定时调度     | APScheduler       | 比 Celery 轻量，MVP 够用              |
| 去重         | DupeFilter + DB   | 双层去重                               |
| 播报         | 钉钉 Webhook      | 用户指定                               |
| 配置管理     | YAML + 环境变量   | 站点规则 YAML 化                       |
