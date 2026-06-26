# Search Playbook — 搜索策略手册

在构造搜索查询时参考此手册，确保时效性和覆盖度。

---

## 时间约束（铁律）

**每条搜索必须带日期。** 以下是各工具的日期写法：

| 工具 | 日期约束写法 | 示例 |
|------|------------|------|
| Web Search | 关键词中加年月 | `"Jensen Huang AI april 2026"` |
| Web Search (site) | 关键词 + site: | `"OpenClaw plugin 2026" site:github.com` |
| HN Algolia API | `numericFilters=created_at_i>{unix_ts}` | `created_at_i>1743206400` |
| GitHub API | `created:>{YYYY-MM-DD}` | `q=AI+agent+created:>2026-03-30` |
| arXiv | `date_from` 参数 | `date_from: "2026-03-30"` |

### Unix 时间戳速查

```python
# 获取 N 天前的 unix 时间戳
import time; print(int(time.time()) - N * 86400)
```

或者让 Agent 用 shell：
```bash
python3 -c "import time; print(int(time.time()) - 7 * 86400)"
```

---

## 模式 A（广角扫描）搜索矩阵

| 类别 | 查询 1 | 查询 2 | 查询 3 |
|------|--------|--------|--------|
| Tools | `AI tools launch {月} {年}` | `AI IDE agent platform {年}` site:news.ycombinator.com | `MCP plugin {年}` site:github.com |
| Models | `LLM release {月} {年}` | `new AI model benchmark {年}` | `arxiv_search: LLM reasoning {date}` |
| Business | `AI funding acquisition {月} {年}` | `AI startup IPO {年}` | `AI partnership deal {年}` |
| Voices | `{人名} AI interview {年}` site:youtube.com | `{人名} keynote {月} {年}` | `{人名} {年}` site:x.com |
| Technical | `AI agent architecture {年}` | `RAG retrieval augmented {月} {年}` | `arxiv_search: multimodal reasoning {date}` |
| Policy | `AI regulation {月} {年}` | `AI safety policy {年}` | `AI act enforcement {年}` |

---

## 模式 B（实体追踪）搜索矩阵

### 人物追踪

```
"{人名}" AI {月} {年}
"{人名}" interview OR keynote {月} {年}
"{人名}" {年} site:youtube.com
"{人名}" {年} site:x.com
"{人名}" statement OR announcement {月} {年}
```

### 公司追踪

```
"{公司名}" AI {月} {年}
"{公司名}" launch OR release {月} {年}
"{公司名}" funding OR partnership {月} {年}
"{公司名}" {年} site:github.com
"{公司名}" {年} site:x.com
HN API: query="{公司名}"&numericFilters=created_at_i>{ts}
```

---

## 模式 C（产品发现）搜索矩阵

```
"{平台名}" best plugin OR extension {年}
"{平台名}" trending OR popular {年}
"{平台名}" awesome list site:github.com
"{平台名}" site:producthunt.com {年}
"{平台名}" site:news.ycombinator.com {年}
GitHub API: q={平台名}+created:>{date}&sort=stars
```

---

## 搜索结果日期验证

搜到结果后，**逐条检查发布日期**：

1. 网页有明确日期 → 用该日期
2. HN/GitHub 有 `created_at` 字段 → 用 API 返回的日期
3. 网页无日期 → 尝试从 URL 中提取（如 `/2026/04/...`）
4. 仍然无法确定日期 → 标注 "⚠️ 日期未知"，不放入时间线

**早于时间窗口的结果 → 直接丢弃。**
