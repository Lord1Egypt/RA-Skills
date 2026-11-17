# 架构参考 — 行业雷达 Industry Radar

## 数据流水线（七阶段）

```
subscription(行业词×技术词)
   │
   ▼
① collector.py   14 内置源 + 自定义源 RSS 并行采集（每源上限 15 条）
   │
   ▼
② cleaner.py     HTML 清洗 + 全文抽取（BeautifulSoup/lxml）
   │
   ▼
③ dedup.py       URL 哈希 + simhash（汉明距离≤3）去重
   │
   ▼
④ relevance.py   行业信号相关性打分（行业词/技术词加权命中）
   │
   ▼
⑤ summarizer.py  摘要生成：LLM 在线（OpenAI 兼容协议）
   │              或离线降级（抽取式摘要 + 规则洞察）
   ▼
⑥ generator.py   主题聚类（Jaccard 兜底）+ 编排 + 成稿
   │              两种风格：standard 标准周报 / curated 编辑精选
   ▼
⑦ store.py       SQLite 落库 + Markdown 落盘（data/briefings/）
```

## 模块职责

| 模块          | 职责                                                       |
| ------------- | ---------------------------------------------------------- |
| main.py       | FastAPI 入口；REST API + 前端静态托管（frontend/）         |
| config.py     | 全部环境变量集中读取（见 config-reference.md）             |
| sources.py    | 14 个数据源的注册表（id/名称/RSS URL/语言/启用开关）       |
| collector.py  | RSS 拉取与解析（feedparser）；内置源与自定义源共用，自定义源强制 RSS/Atom 校验 |
| cleaner.py    | 正文抽取与清洗                                             |
| dedup.py      | simhash 去重                                               |
| relevance.py  | 关键词相关性打分                                           |
| summarizer.py | LLM / 降级摘要                                             |
| generator.py  | 流水线编排与 Markdown 成稿（编辑精选式排版在此实现）       |
| store.py      | SQLite 访问层（8 张表：user/subscription/source/custom_source/article/briefing/briefing_section/push_log） |

## 数据表关系

```
user 1─N subscription 1─N article
                          1─N briefing 1─N briefing_section
user 1─N custom_source        （订阅通过 sources_json 里的 "cs:<id>" 引用）
```

## 云端部署对应关系（华为云）

| 本地组件          | 云端方案                          |
| ----------------- | --------------------------------- |
| FastAPI 路由      | APIG + FunctionGraph              |
| store.py (SQLite) | RDS MySQL                         |
| data/briefings/   | OBS 对象存储                      |
| 手动 run          | FunctionGraph TIMER 触发器        |
| LLM               | ModelArts Studio（OpenAI 兼容）   |

## 前端

`app/frontend/` 为免构建 Vue 3 静态页（vue.global.prod.js 本地引入，无 CDN 依赖），
由 FastAPI `StaticFiles(html=True)` 挂载在 `/`，浏览器直接访问服务地址即用。
