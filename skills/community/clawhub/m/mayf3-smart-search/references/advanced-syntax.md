# 高级搜索语法实测

## Bing CN 关键词碰撞问题

Bing CN（和 Bing INT）有一个**系统性缺陷**：当搜索包含某些常见英文词时，上下文会自动偏向中文教育/百科内容，导致搜索结果完全跑偏。

### 实测失败案例（2026-05-14）

| 搜索词 | 预期 | 实际结果 |
|--------|------|---------|
| `"smart search" AI agent site:github.com` | GitHub 项目 | smart 汽车（品牌被劫持） |
| `"free search API" tavily` | Tavily API | "free" 的词典释义 |
| `"test search engine" API` | 搜索 API 信息 | Speedtest 网速测试 |
| `"web scraping" best practices` | 爬虫技巧 | WWW 万维网百科 |
| `"searchfree.site" API` | 免费 API 介绍 | 豆包 AI（完全无关） |

### 原因

- 中文分词会把 `free` 匹配到"免费"→ 返回词典结果
- `smart` 在中文搜索中约 80% 指代 smart 汽车
- `test` 优先匹配到 speed test

### 解决方案

| 场景 | 推荐方案 |
|------|---------|
| 英文技术搜索 | ✅ 优先用 **360**（英文搜索质量意外好） |
| 英文精确搜索 | ✅ 用 **searchfree.site API**（无中文干扰） |
| Bing CN 英文搜索 | ❌ 接受偏差，或加 `-smart -car` 排除词 |

## 高级语法实测结论

| 语法 | Bing CN | 360 | Sogou | 说明 |
|------|---------|-----|-------|------|
| `site:` | ✅ 有效 | ✅ 有效 | ⚠️ 部分 | 最可靠的操作符 |
| `filetype:` | ⚠️ 不严格 | ⚠️ 不严格 | ❌ 无效 | 只倾向展示指定类型 |
| `""` 精确匹配 | ✅ 有效 | ✅ 有效 | ✅ 有效 | 强烈推荐 |
| `-` 排除 | ✅ 有效 | ✅ 有效 | ⚠️ 部分 | `-site:xxx` 排除噪音源 |
| `intitle:` | ✅ 有效 | ⚠️ 部分 | ❌ 无效 | 标题限定 |
| `after:` / `before:` | ✅ **有效** | ❓ 待测 | ❓ 待测 | 日期过滤生效 |
| `-site:` 排除域名 | ✅ 有效 | ✅ 有效 | ⚠️ 部分 | 排除噪音源 |
| `tbs=qdr:` 时间过滤 | ⚠️ 不稳定 | ❌ 无效 | ❌ 无效 | 不推荐，用 `after:` 代替 |

### 组合示例

```
"AI agent framework" after:2026-01-01 -site:medium.com -site:pinterest.com
intitle:"deep research" site:github.com
"行业报告" filetype:pdf site:gov.cn
"LLM benchmark" after:2025-06-01 site:arxiv.org OR site:paperswithcode.com
```
