# TODO

> 唯一任务源。每轮只允许处理一个任务。

## Phase A — 基础骨架

- [x] T101: 项目初始化 — Python 项目结构、pyproject.toml、requirements.txt、Scrapy 配置、src/ 包结构创建
- [x] T102: 数据模型 — Novel/Chapter/Episode 模型（SQLAlchemy ORM）、SQLite 存储层、数据库初始化脚本
- [x] T103: 配置系统 — YAML 配置加载器、settings.yaml 全局配置、站点配置目录结构（config/sites/）
- [x] T104: 站点地图模块 — sitemap JSON 格式定义、生成/更新/查询接口（src/sitemap/generator.py）
- [x] T105: 基础爬虫框架 — Spider 基类（src/spiders/base.py）、Item/Pipeline/Middleware 骨架、请求管理

## Phase B — 站点适配

- [x] T201: Webnovel 站点配置 — config/sites/webnovel.yaml 规则文件、URL 模式、字段映射
- [x] T202: Webnovel Spider — 书籍列表/章节列表/章节内容抓取、增量检测（src/spiders/webnovel.py）
- [x] T203: ReelShorts 站点配置 — config/sites/reelshorts.yaml 规则文件、API 接口分析
- [x] T204: ReelShorts Spider — 剧集列表/视频信息抓取或标记为需 App 抓包的 stub（src/spiders/reelshorts.py）

## Phase C — 调度与分级

- [x] T301: 定时调度系统 — APScheduler 集成、cron 表达式配置、任务生命周期管理（src/scheduler/manager.py）
- [x] T302: 内容分级引擎 — 更新频率分析、热度评分、三级分类（高/中/低）（src/classifier/grader.py）
- [x] T303: 增量更新与去重 — 基于 last_updated/chapter_id 的增量抓取、Scrapy DupeFilter 配置

## Phase D — 播报与接口

- [x] T401: 消息模板系统 — Jinja2 模板、分级播报策略（即时/日汇总/周汇总）（src/broadcast/templates.py）
- [x] T402: 钉钉机器人集成 — Webhook 对接、Markdown 消息、签名验证、失败重试（src/broadcast/dingtalk.py）
- [x] T403: RSS 订阅源 — Atom/RSS feed XML 输出、按分类/站点过滤
- [x] T404: CLI 入口 — click 命令行工具（crawl/list/status/broadcast 子命令）（src/cli.py）

## Phase E — 运维与健壮性

- [x] T501: 日志与监控 — structlog 结构化日志、爬取统计仪表盘数据、异常钉钉告警
- [x] T502: 反爬增强 — 随机 UA、请求限速、代理池接口预留、Cloudflare 绕过策略
- [x] T503: Docker 化部署 — Dockerfile、docker-compose.yaml、.env 管理、cron 容器调度
