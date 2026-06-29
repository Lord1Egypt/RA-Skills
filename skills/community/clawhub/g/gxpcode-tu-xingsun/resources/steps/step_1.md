# Step 1 — 检测

**目的**：从 `resources/sources.yaml` 中所有数据源拿到标题、日期、链接。

## 源类型

| type | 处理方式 | 执行方 |
|------|------|--------|
| `rss` | feedparser 解析 RSS feed | step1_rss.py |
| `web` | 浏览器自动化读列表页 | step1_web.py |

## Web 型源的 extract 配置

每个 web 源需要在 sources.yaml 中配置提取规则：

| 配置项 | 必填 | 说明 |
|------|:--:|------|
| `link_by` | ✅ | 标题和链接的对应关系：`title`（标题即链接）或 `text:xxx`（链接文字固定） |
| `date_pattern` | ❌ | 日期的位置：`行模式`（日期独立行）/ `括号内`（日期在标题末尾括号）。列表页没有则留空，S4 详情页补 |

## 输出约束

每条条目必须满足，缺一丢弃：

| 字段 | 必填 |
|------|:--:|
| `title` | ✅ |
| `url` | ✅ |
| `date` | — |
| `source` | ✅ |
| `jurisdiction` | ✅ |

## 执行流程

1. `step1_rss.py` 处理 `type: rss` 的源，feedparser 拿 title/link/date
2. `step1_web.py` 处理 `type: web` 的源：
   - 启动浏览器
   - `goto(url, wait_until='networkidle')`
   - 按 `extract.link_by` 规则绑定标题和链接
   - 按 `extract.date_pattern`（如有）提取日期
3. S1 全部条目合并后 → 送 S2
