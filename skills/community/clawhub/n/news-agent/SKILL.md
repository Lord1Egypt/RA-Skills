---
name: news-agent
description: 新闻智能体系统 API 集成。支持查询新闻、触发采集/分析任务、获取仪表盘数据、趋势分析等。使用场景：新闻数据管理、采集任务自动化、趋势分析、词云生成。
metadata:
  openclaw:
    requires:
      env:
        - NEWS_API_BASE_URL
---

# News Agent Skill

通过新闻智能体后端 API 管理新闻数据、触发任务、查看分析结果。

## 前置条件

1. 新闻智能体后端服务已启动（默认端口 `8030`）
2. **设置环境变量**（可选，默认连接本地服务）：
   ```bash
   export NEWS_API_BASE_URL="http://localhost:8030/api/v1"
   ```

## 功能脚本

### 查询新闻列表

```bash
# 查询最新新闻
python3 scripts/get_articles.py

# 按关键词搜索
python3 scripts/get_articles.py --keyword "医药"

# 按分类筛选
python3 scripts/get_articles.py --category_id 1

# 按日期范围
python3 scripts/get_articles.py --start_date 2026-03-01 --end_date 2026-03-17

# JSON 格式输出
python3 scripts/get_articles.py --json

# 限制返回数量
python3 scripts/get_articles.py --limit 10
```

输出示例：
```
📰 新闻列表 (共 156 条，显示前 20 条)

1. 🟢 [ID:42] 某药企获批新药上市
   分类: 行业动态 | 来源: 医药网 | 2026-03-17 10:30
   摘要: 该药企研发的创新药获得国家药监局批准...
   关键词: 新药, 上市, 药监局

2. 🔵 [ID:41] 2026年医药行业趋势报告
   分类: 研究报告 | 来源: 中国医药报 | 2026-03-16 14:20
   摘要: 报告指出未来三年生物医药将迎来...
```

### 获取仪表盘数据

```bash
# 获取仪表盘概览
python3 scripts/get_dashboard.py

# JSON 格式输出
python3 scripts/get_dashboard.py --json
```

输出示例：
```
📊 新闻智能体仪表盘

📈 数据概览
  新闻总数: 156
  今日新增: 12
  分类数量: 6
  热门关键词: 8

📁 分类分布
  行业动态: 45 篇
  政策法规: 32 篇
  研究报告: 28 篇

🔥 热词 TOP10
  1. 创新药 (23次)
  2. 集采 (18次)
  3. 生物医药 (15次)
```

### 触发采集/分析任务

```bash
# 触发新闻采集
python3 scripts/trigger_task.py crawl

# 触发新闻分析（LLM 摘要/分类/关键词）
python3 scripts/trigger_task.py analyze

# 触发趋势统计
python3 scripts/trigger_task.py trend

# 查看任务状态
python3 scripts/trigger_task.py status
```

输出示例：
```
✅ 采集任务已触发

📋 任务状态
  采集: 空闲 | 上次运行: 2026-03-17 08:00:00 | 处理: 12 篇
  分析: 空闲 | 上次运行: 2026-03-17 08:10:00 | 处理: 8 篇
```

### 趋势分析

```bash
# 热词排行（默认7天 TOP20）
python3 scripts/get_trends.py hot

# 自定义天数和数量
python3 scripts/get_trends.py hot --days 30 --top 10

# 查询特定关键词趋势
python3 scripts/get_trends.py keyword --keyword "创新药" --days 30

# 分类趋势
python3 scripts/get_trends.py category --days 15

# JSON 输出
python3 scripts/get_trends.py hot --json
```

输出示例：
```
🔥 热词排行 TOP20 (近7天)

 1. 创新药        ████████████████████ 23
 2. 集采          ███████████████     18
 3. 生物医药      ████████████        15
 4. CDE           ██████████          12
```

## API 参考

详见 [references/api_docs.md](references/api_docs.md)

## 常用 API 端点

| 功能 | 方法 | 端点 |
|------|------|------|
| 新闻列表 | GET | `/articles` |
| 新闻详情 | GET | `/articles/{id}` |
| 分类列表 | GET | `/categories` |
| 仪表盘 | GET | `/dashboard` |
| 词云生成 | GET | `/wordcloud/generate` |
| 关键词趋势 | GET | `/trends/keyword` |
| 热词排行 | GET | `/trends/hot` |
| 分类趋势 | GET | `/trends/category` |
| 触发采集 | POST | `/tasks/crawl` |
| 触发分析 | POST | `/tasks/analyze` |
| 触发趋势 | POST | `/tasks/trend` |
| 任务状态 | GET | `/tasks/status` |
| 当前用户 | GET | `/auth/me` |

## 项目结构

| 组件 | 路径 | 技术栈 |
|------|------|--------|
| 前端 | `news_vue3_pharmablock/` | Vue 3 + Vite + Element Plus + ECharts |
| 后端 | `news_python_pharmablock/` | FastAPI + SQLAlchemy + PostgreSQL |
| 网关 | `gateway_node_pharmablock/` | Node.js + Express（SSO 鉴权） |

## 注意事项

1. **鉴权方式**：生产环境通过网关 SSO Cookie 认证；开发环境使用 `Bearer PharmaBlock Gateway` 绕过
2. **后端端口**：默认 `8030`，通过 Vite 代理 `/api` → 网关 `3009` → 后端
3. **数据库**：PostgreSQL，异步驱动 asyncpg
4. **LLM**：使用阿里云 DashScope（qwen-plus）进行文章分析
5. **定时任务**：APScheduler，采集间隔可配置，趋势统计每日凌晨 1:00
