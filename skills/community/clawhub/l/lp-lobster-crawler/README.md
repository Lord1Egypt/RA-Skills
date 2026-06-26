# lobster-crawler-skill

龙虾平台网络内容爬取技能 — 定向抓取 Webnovel、ReelShorts 等网站的书籍/短剧内容。

## 功能

- 定向爬取目标站点的结构化内容（小说章节、短剧剧集）
- 站点地图沉淀与增量更新
- 内容分级（高/中/低优先级）
- 钉钉机器人定时播报
- RSS 订阅源输出

## 技术栈

- Python 3.11+
- Scrapy 2.11+（爬虫框架）
- SQLite / SQLAlchemy（数据存储）
- APScheduler（定时调度）
- click（CLI）

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 查看 CLI 帮助
python -m src.cli --help

# 运行爬虫（待 Phase B 实现）
# lobster crawl webnovel
```

## 配置

- 全局配置：`config/settings.yaml`
- 站点规则：`config/sites/*.yaml`
- 环境变量：复制 `.env.example` 为 `.env` 并填写

## 项目结构

```
src/
├── models/       — 数据模型 (ORM)
├── spiders/      — Scrapy 爬虫
├── sitemap/      — 站点地图
├── scheduler/    — 定时调度
├── classifier/   — 内容分级
├── broadcast/    — 钉钉播报
└── cli.py        — CLI 入口
config/
├── settings.yaml — 全局配置
└── sites/        — 站点规则
```

## 开发

```bash
# 运行测试
pytest

# claude loop 持续开发
bash scripts/claude_loop.sh
```
