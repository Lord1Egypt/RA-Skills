# REFERENCE.md — Paid Database Access 参考手册

按功能索引，每个 `###` 章节 ≤ 50 行。配合 SKILL.md 使用。
> 🚀 首次使用？先看 [QUICKSTART.md](QUICKSTART.md)。

---

## 快速验证

```bash
python scripts/pipeline/setup.py --check          # 环境检查
browser.start(profile="openclaw")         # 启动浏览器
browser.open(profile="openclaw",         # IEEE 零配置测试
  url="https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=machine+learning")
read extractors/ieee.js
browser.act(profile="openclaw", kind="evaluate", fn=<script>)
```

---

## 数据库搜索

### IEEE Xplore
- **登录:** 搜索无需登录，下载需机构订阅
- **URL模板:** `https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={query}&ranges={year1}_{year2}_Year`
- **提取:** `evaluate extractors/ieee.js` → `{totalResults, papers: [{title, authors, year, venue, type, citations, doi, link, isOA, hasAbstract}]}`
- **翻页:** `&pageNumber=2,3,...`
- **详情页:** `https://ieeexplore.ieee.org/document/{arnumber}` + `extractors/ieee_detail.js`
- **选择器:** `xpl-result-item` 或 `.List-results-items > div[class*="result"]`
- **citations:** 4 级回退 regex（主 `Cited by: Papers (N)` → `Citations: N` → body text → 数字模式匹配）

### Scopus
- **登录:** 需 Elsevier API Key（注册 https://dev.elsevier.com，需机构邮箱）
- **API:** `python scripts/pipeline/scopus_search.py -q "TITLE-ABS-KEY({query}) AND PUBYEAR > 2022" -k <key> --count 25 -o memory/scopus.json`
- **详情页:** 浏览器 `https://www.scopus.com/record/display.uri?eid={eid}` + `extractors/scopus_detail.js`
- **速率:** API ~9 次/秒（标准 Key），9k 次/秒（InstToken）
- **已知坑:** 403 = 不在机构 IP（需 VPN）。API Key 非 InstToken 时 view=FULL 可能受限

### ACM Digital Library
- **登录:** 搜索无需登录，详情页 Cloudflare（已登录豁免），PDF 需机构订阅
- **URL模板:** `https://dl.acm.org/action/doSearch?AllField={query}&pageSize=25&AfterYear={year}`
- **提取:** `evaluate extractors/acm.js` → `{totalResults, papers: [{...citations, doi, link, isOA, pdfUrl}]}`
- **翻页:** `&startPage=0,1,2...`（0-indexed）
- **详情页:** DOI URL + `extractors/acm_detail.js`（已登录时可用）
- **选择器:** `li.search__item`，标题 `.issue-item__title a`
- **type:** 标题含 survey/review → 自动标 Review。venue 含 conf/proceed/sympos → Conference Paper

### Engineering Village (Compendex)
- **登录:** 需机构登录（浏览器窗口手动或 cookie 持久化）
- **搜索:** `act type` 填搜索框 → `act click` 搜索 → wait 3s → `evaluate extractors/engineering_village.js`
- **提取:** `{totalResults, papers: [{title, authors, year, venue, doi, link, citations, isOA, docId}]}`
- **翻页:** click `#next-page-top`
- **详情页:** `https://www.engineeringvillage.com/app/doc/?docid={docId}` + `extractors/engineering_village_detail.js`
- **摘要标记:** `\nAbstract\nBack to ToC\n` 之间，成熟可用（测试 1,592 字符完整摘要）
- **已知坑:** SPA 渲染 2-3s。SEARCHID 可能过期 → 回退填表搜索

---

## 查询构建

```bash
python scripts/pipeline/query_builder.py -c memory/search_concept.json --format commands
```

概念 JSON 格式（写入 `memory/search_concept.json`）：
```json
{
  "core_concepts": ["主题词"],
  "synonyms": {"缩写": ["全称1", "全称2"]},
  "sub_topics": ["子方向"],
  "exclude": ["排除词"],
  "year_range": "2023-2026",
  "databases": ["ieee", "scopus", "acm", "engineering_village"]
}
```

---

## 摘要补全

```bash
python scripts/pipeline/enrich_abstracts.py -i memory/merged.json -o memory/enriched.json -k <scopus_api_key>
```

四层回退：

| Tier | 来源 | 成本 |
|---|---|---|
| 0 | 本地缓存 `paper-abstracts/<DOI>.txt` | 0 |
| 1a | Semantic Scholar API（1.5s/req，DOI + 标题交叉验证 ≥60%） | 免费 |
| 1b | OpenAlex API（SS 失败时回退，inverted index 解码） | 免费 |
| 2 | 🔒 子代理浏览器详情页 `_detail.js` | ~2K token/篇 |
| 3 | 失败记录到 `enrich_failures.json` | — |

🛑 **检查:** 缺失率 > 15% → 触发 Tier 2（详见 SKILL.md 检查点 B）。

---

## 详情页提取器

| DB | Extractors | 摘要方式 |
|---|---|---|
| IEEE | `ieee_detail.js` | `.abstract-text` |
| Scopus | `scopus_detail.js` | `#abstractSection` |
| ACM | `acm_detail.js` | `.issue-item__abstract` + 10+ 种 Read More 按钮 |
| EV | `engineering_village_detail.js` | `\nAbstract\n` 标记之间 |

---

## 评分与输出

```bash
# 机器粗筛（token 重叠，快但粗糙）
python scripts/pipeline/paper_ranker.py -i memory/enriched.json -o memory/ranked.json --keywords "<词>" --mode balanced

# AI 语义 rerank（推荐，独立 API 调用）
python scripts/pipeline/ai_rerank.py -i memory/enriched.json -o memory/ai_ranked.json -t "<研究主题>"

# 中文简述（Top 15，独立 API 调用）
python scripts/pipeline/ai_summarize.py -i memory/ai_ranked.json -o memory/summarized.json --top 15

# 安全读取（不含摘要正文）
python scripts/extra/strip_abstracts.py -i memory/ai_ranked.json --summary --top 15

# BibTeX 导出
python scripts/pipeline/export_citations.py -i memory/ai_ranked.json --top 15 -o memory/results.bib

# merge_results 已内置 type 归一化：
#   research-article/journal article/Article → Journal Article
#   conference-paper/conference article/Proceedings → Conference Paper
#   survey/review-article → Review
#   等 40+ 映射
```

---

## 提取器调试

evaluate 返回 `count: 0` 或字段为空 → 前端变更，选择器失效。

**探路诊断 JS（在 evaluate 执行）：**
```javascript
() => { return {
    url: window.location.href,
    title: document.title,
    candidates: (() => {
        const s = ['div[class*=result]', 'li[class*=result]', 'article',
            '[class*=search-result]', '.List-results-items > *'];
        const f = {};
        for (const sel of s) {
            try { const n = document.querySelectorAll(sel).length; if (n >= 3) f[sel] = n; } catch(e) {}
        }
        return f;
    })(),
    sampleHTML: (() => {
        for (const sel of ['div[class*=result]', 'li[class*=result]', 'article']) {
            const el = document.querySelector(sel);
            if (el) return el.outerHTML.substring(0, 2000);
        }
        return 'no match';
    })(),
};}
```

**修复流程:** 跑诊断 → 查 sampleHTML 找新选择器 → 更新 `extractors/<db>.js` 的 `querySelector` → evaluate 验证 `count > 0` 且字段正确。

**不自动修的场景:** 页面架构重写 / 需重新登录 / 连续 3 次失败 → 告知用户介入。

---

## 故障速查

| 症状 | 原因 | 操作 |
|---|---|---|
| evaluate → count: 0 | 选择器失效 | 跑探路诊断 → 修 extractor |
| evaluate → Execution context destroyed | SPA 渲染中 | 等 2-3s 重试 |
| Scopus API 403 | 不在机构 IP | 连 VPN |
| Scopus API 401 | Key 无效 | 检查 config.yaml |
| ACM 详情页 503/Cloudflare | 未登录 | 浏览器手动登录 ACM 一次 |
| EV SEARCHID 404 | 搜索历史过期 | 回退填表搜索 |
| browser.start 失败 | 缺 Chrome | 安装 Chrome 或等 Playwright 下载 |
| enrich SS API 429 | 限流 | 内置 1.5s delay + OpenAlex 回退，等即可 |
| cookie_bridge import error | 缺依赖 | `pip install pywin32 pycryptodome` |

---

## 已知限制

- 浏览器必需 Chrome/Edge（可见窗口，非 headless）
- SSO 会话有时效性
- 选择器随数据库改版脆弱（但内置诊断修复机制）
- Scopus 需 API Key + 机构 IP/VPN
- WoS/CNKI 模板级（未完整实测）
- cookie_bridge 仅 Windows（pywin32 依赖）
- PDF 仅自动匹配免费版（arXiv/Semantic Scholar/Unpaywall），付费版需手动下载
