# PDF 全文下载入口 — 分门别类模板

> 适用：meta-analysis（A4 下载/抽取）、ct-literature（PDF 批量下载）、ct-registry
> （publisher_pdf 节点）的"如何从一篇文献拿到 PDF"决策参考。
> 本文把真实世界的下载入口归成 **几大类框架**，每类给"识别特征 + URL/API 模板 +
> 落地代码映射"。所有模板均来自代码内已验证模式或本机实测（2026-09-05 复核）。
>
> ⚠️ 反爬边界（v7.8 权威结论）：数据中心 IP + headless 下，CF 保护站与
> ScienceDirect 等为**结构性拦截**（人机验证/CPE00001），不要在此类上反复重试；
> 归入"需浏览器/人工"类，用书签或用户已登录浏览器下载。

---

## 总览：五类框架

| 类 | 名称 | 识别特征 | 自动化友好度 | 典型平台 |
|----|------|---------|-------------|---------|
| **A** | 聚合 API 直链 | 一个 API 调用返回 PDF 链接 | ⭐⭐⭐⭐⭐ 首选 | Unpaywall / Europe PMC core / OpenAlex |
| **B** | OA 仓储模板 URL | DOI 或 PMCID 已知，URL 可拼 | ⭐⭐⭐⭐⭐ 首选 | PMC / Europe PMC / bioRxiv·medRxiv·arXiv / MDPI(全OA) |
| **C** | 出版商文章页内找链接 | 需打开文章页，在 DOM 里找 PDF 按钮 | ⭐⭐⭐ 半自动 | 各出版商文章页（ACS/RSC/Elsevier OA…） |
| **D** | 签名直链提取 | PDF 由对象存储签名 URL 提供 | ⭐⭐ 需登录/浏览器 | ScienceDirect(X-Amz) / Wiley / Springer |
| **E** | 付费墙 + 人工/登录态 | 无 OA，仅订阅可下 | ⭐ 人工 | 订阅制期刊正文 |

优先级恒为 **A → B → C → D → E**：先用 API/模板零成本拿到，再考虑抓页面；
不要一上来就开浏览器。下文每类给出可直接照抄的模板。

---

## A 类：聚合 API 直链（首选，零页面分析）

### A1. Unpaywall（DOI → PDF）— 代码已验证
```
GET https://api.unpaywall.org/v2/{doi}?email={你的邮箱}
→ json.best_oa_location.url_for_pdf（无则 .url）
```
- 免费、无密钥；要求合法 email。
- 落地：`meta-analysis/adapters/pdf_fetch.py::_unpaywall_pdf()`。
- 覆盖：绝大多数 OA / Hybrid OA / 作者自存档；含 MDPI、PMC 等多源回退。

### A2. Europe PMC core API（DOI/PMID/PMCID → 多形态全文链接）
```
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={DOI|EXT_ID:{id}}&resultType=core&format=json
→ result.fullTextUrlList.fullTextUrl[]  每条含 availability/documentStyle/site/url
```
**documentStyle 语义**（2026-09-05 PMC3253961 实测）：
| documentStyle | 含义 | 用例 |
|---------------|------|------|
| `html` | HTML 全文页 | site=Unpaywall / Europe_PMC → 期刊页 |
| `pdf` | **PDF 直链** | site=Europe_PMC → `europepmc.org/articles/{PMCID}?pdf=render` |
| `doi` | 出版商 DOI 落地页 | 需再走 A/B/C |
- 另有轻量字段：`hasPDF:Y/N`、`isOpenAccess`、`pmcid` —— 先看 hasPDF 再决定要不要取 PDF。
- 落地：`ct-registry`（检索）、`meta-analysis pdf_fetch` 的 PMID→PMC 链路同源。

### A3. OpenAlex（work → OA 链接）
```
GET https://api.openalex.org/works/doi:{doi}
→ open_access.oa_url（best） / best_oa_location.pdf_url（若有）
```
- 落地：`ct-literature/adapters/fetch_openalex.py`。

---

## B 类：OA 仓储模板 URL（ID 已知即可拼，零请求找链接）

### B1. PMC 全文 PDF — 代码已验证 + 用户实例 ✓
用户实例：PMC 文章页右侧 **"PDF (789.4 KB)"** 按钮（PMC3253961 = VITAL 设计论文）。
该按钮 href 即以下模板（NCBI 统一格式）：
```
https://www.ncbi.nlm.nih.gov/pmc/articles/{PMCID}/pdf/
例: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3253961/pdf/
```
- PMCID 来源：DOI→PMC 用 A2（Europe PMC core 返回 pmcid），或 PMID→PMC 用 E-utilities
  `elink.fcgi?dbfrom=pubmed&db=pmc&id={pmid}&retmode=json`。
- 落地：`pdf_fetch.py::doi_to_pmc_pdf()` / `_pmid_pmc_pdf()`。
- 变体：Europe PMC 镜像同文 `https://europepmc.org/articles/{PMCID}?pdf=render`（A2 的 pdf 条）。

### B2. 预印本全文 — 代码已验证
```
bioRxiv/medRxiv: https://www.{server}.org/content/{doi}v{version}.full.pdf
                 例 https://www.biorxiv.org/content/10.1101/2024.01.01.000001v1.full.pdf
arXiv:          https://arxiv.org/pdf/{arxiv_id}
```
- 版本号经 `api.biorxiv.org` 解析；bioRxiv 对无头客户端放行（200 application/pdf，2026-09-04 实测）。
- 落地：`pdf_fetch.py::_biorxiv_pdf()` 等；**⚠️ 预印本非发表版，须作者级校验**（同篇校验）。

### B3. MDPI（全 OA，无墙）— 代码验证命中用户实例 ✓
用户实例：摘要上方 **Download 下拉 → Download PDF**。实测记录（.merged.json 中
`10.3390/nu13072421`）：
```
https://www.mdpi.com/{issn}/{vol}/{issue}/{articleno}/pdf?version={timestamp}
例: https://www.mdpi.com/2072-6643/13/7/2421/pdf?version=1626337299
```
- MDPI 全部 OA，`/pdf` 去掉 version 也可下（version 仅缓存指纹）。
- 落地：A1 Unpaywall 即会返回此链接（best_oa_location）。
- ⚠️ 反爬：mdpi.com 域在 `pdf_fetch._ANTI_SCRAPE_HOSTS` 名单内，个别路径走 coze 节点下载。

---

## C 类：出版商文章页内找 PDF（打开页面 → DOM 找链接）

适用：非 OA 仓储平台，但文章页公开（摘要页可访问）且正文 OA/免费期。

### 识别特征（代码已验证规则，pdf_cf_guard.py）
1. 页面含 `<a href>` / `<iframe>` 指向 `.pdf` 扩展名、`/pdf` 路径段、`showPdf`、`pdfdownload` 关键字；
2. 平台 URL 模板：
   - Elsevier 系（含其 OA 子刊 / 免费期）：`https://{平台域}/article/{PII}/pdf`（与 OA 直链同构）；
   - 通用兜底：landing URL 尾补 `/pdf`。
3. **CF 保护判断**：响应为 CF 挑战页（非 PDF）时，标 `cf_challenge`，绝不把挑战页当 PDF 落盘
   （`_reject_chromium_pdf`：拦截 Chromium print 伪 PDF，特征 Producer=Skia/PDF 等）。

### 落地代码
- `ct-registry/adapters/coze/src/graphs/nodes/pdf_cf_guard.py`（共享防护原语库）
- `publisher_pdf_batch_node.py`（直下探测 → 浏览器+S3 兜底，B 路径默认关闭，
  需 `CT_ENABLE_BROWSER_PDF_DOWNLOAD=1` 显式启用）

---

## D 类：签名直链提取（ScienceDirect X-Amz 等）

### 用户提供的"SD抓PDF"书签（手动可用，自动化边界明确）
```
在 ScienceDirect 文章/PDF 页执行：
  遍历 iframe/embed/object/a → 收集含 X-Amz|.pdf 的 URL → 打开第一个
```
- **规律**：SD 的 PDF 由 Elsevier 对象存储签名 URL 提供，形如
  `pdf.sciencedirectassets.com/.../main.pdf?X-Amz-...`；页面上的
  iframe（PDF 阅读器）或 a 标签持有该直链。
- **结构性边界（2026-09-05 实测结论）**：
  | 场景 | 结果 |
  |------|------|
  | headless + 数据中心 IP（coze 云） | CPE00001 拒绝页 / CF "Are you a robot?" captcha → **不可行** |
  | 用户已登录真实浏览器 | 可行：书签或 CDP `/eval` 提取直链 → Ctrl+S/下载 |
  | 本机 CDP 自动化（Chrome CDP 9222 + 独立 profile） | 文章页可达时 JS 可执行；订阅内容仍需登录态 |
- 自动化管线（coze B 方案）若指云端 headless：**维持封存**。书签/CDP 的价值场景是
  **用户本机浏览器**。CDP 落地点：Node WebSocket 直连 `ws://127.0.0.1:9222` 注意
  unset 代理 + 显式 127.0.0.1 + 动态取 UUID（脚本见 workbench 侧 cdp_sd_test.mjs 范式）。

### Wiley / Springer 同类
- 同为签名 URL / 登录墙混合；OA 走 A1（Unpaywall）优先，订阅走 E 类人工。

---

## E 类：付费墙（无 OA）→ 人工 / 登录态

- 判定：A1/A2/A3 全空且非 OA → 标记 `needs_upload`，不硬闯。
- 工作台行为：A4 面板标红「待上传 PDF」，用户手头有 PDF 直接上传（DOI/标题自动匹配）。
- 书签/Ctrl+P 另存为 PDF 仅作人工兜底（学术合理使用范围内）。

---

## 决策速查（一张表走天下）

| 手头有什么 | 第一步 | 模板/API | 失败回退 |
|-----------|--------|---------|---------|
| DOI | A1 Unpaywall | `api.unpaywall.org/v2/{doi}?email=` | A2 Europe PMC core → B/C |
| DOI（确认 PMC 有） | A2 core API | 取 `pmcid` + documentStyle=pdf 条 | B1 PMC /pdf/ 模板 |
| PMID | E-utilities elink→PMC | `elink.fcgi?dbfrom=pubmed&db=pmc&id=` | A2 core |
| PMCID | B1 直拼 | `ncbi.nlm.nih.gov/pmc/articles/{PMCID}/pdf/` | Europe PMC `?pdf=render` |
| arXiv/bioRxiv ID | B2 直拼 | `.full.pdf` / `arxiv.org/pdf/` | 页面找（C） |
| 文章页 URL（OA） | C DOM 找 | 见 pdf_cf_guard 规则 | 反爬名单 → D/E |
| 文章页 URL（SD/订阅） | D/E | 书签/CDP 直链 / 人工上传 | — |

---

## 维护约定

- 新增"平台 → PDF 入口"经验时：先在 A1/A2 实测能否拿到（多数能），**不要默认开浏览器**；
  确认反爬/结构边界后再入 D/E 类。
- 本文是"分类模板"，单站点详细操作经验（选择器、URL 结构）按 web-access 惯例存
  `references/site-patterns/{domain}.md`。
