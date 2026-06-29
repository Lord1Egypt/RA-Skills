---
name: paid-db-access
description: >
  AI 接入付费学术数据库（IEEE/Scopus/EV/ACM）的权限桥接层。
  通过浏览器 CDP 借用用户登录态，搜索→提取→去重→补摘要→评分→输出。
  Zero-token abstract handling.
---

# Paid Database Access

> 🚀 **新用户？** 先看 [QUICKSTART.md](QUICKSTART.md) 10 分钟跑通第一条结果。

通过 OpenClaw 浏览器 CDP 承载用户的机构登录会话，让 AI 能搜索 IEEE Xplore、Scopus、Engineering Village、ACM Digital Library 等付费数据库——这些数据库不向 AI 开放 API，但用户已付费订阅。附带摘要隔离机制，确保大量摘要文本不污染对话上下文。

---

## 🛑 铁律（违反即不合格）

1. **禁止 snapshot 搜索结果页。** 用 `browser.act evaluate` 注入 JS 提取器，token 差距 30×（~500 vs ~15,000）。
2. **禁止摘要进入主对话上下文。** 摘要全部走文件持久化，JSON 只存 `_abstract_file` 引用。详情页提取走子代理隔离。
3. **🛑 三个硬性检查点不可跳过：** 搜索覆盖 | 摘要完整性(≤5%缺失) | 输出格式

---

## ⚠️ IEEE 特殊处理

### DOI 缺失
IEEE 搜索列表页**不含 DOI**，详情页通常有但部分论文（如 SC Workshop 论文集）可能没有 DOI 元数据。

**不管有没有 DOI，处理流程不变：**
1. `ieee.js` 从搜索结果提取 `docId`（从 `/document/XXXXX/` URL）
2. 缓存匹配优先用 `docId` → `ieee_doc_{docId}.txt`（比 DOI 更可靠）
3. Tier 2 子代理打开详情页，`ieee_detail.js` 同时提取 DOI 和摘要
4. **有 DOI → 写回 JSON；无 DOI → 留空，不影响摘要提取**
5. BibTeX 输出中无 DOI 的条目省略 `doi` 字段，不影响可用性

### 摘要截断
搜索列表页的摘要预览以 `...` 截断。完整摘要**只在详情页**。本管道设计为搜索阶段不抓摘要，全部由 enrich 步骤补全。

### 缓存键
IEEE 论文统一用 `docId` 做缓存键。`docId` 是 IEEE 内部唯一标识（DOI 末尾数字段 = docId），比标题哈希稳定得多。

---

## 管道清单（每步必须执行，不可跳过）

### 0. 前置检查
- [ ] `python scripts/pipeline/setup.py --check`（检测并自动更新 config.yaml 缓存，确保环境状态准确）
- [ ] `browser.status → running: true`（否则 `browser.start(profile="openclaw")`）
- [ ] `config.yaml → scopus.api_key` 有值（无则跳过 Scopus）

### 0.5 免费预检（OpenAlex — 纯 HTTP，不开浏览器）
```bash
python scripts/pipeline/free_precheck.py -c memory/search_concept.json --json
```

| 信号 | 命中数 | 操作 |
|---|---|---|
| `narrow` | ≤ 3 | ⚠️ **禁止继续。** 反馈 AI 调整 search_concept.json（放宽 core_concepts / 减少 AND 条件 / 去掉部分 exclude）后重新预检 |
| `good` | 3-2000 | ✅ 继续进入正式搜索 |
| `broad` | > 2000 | ⚠️ **禁止继续。** 反馈 AI 收紧概念（加 core_concepts 约束 / 增加 exclude / 缩小年份范围）后重新预检 |
| `skip` | — | ⚠️ API 不可用，跳过预检继续管道（不阻塞） |

**设计原理：** OpenAlex 免费、无限速、覆盖全学科。用 100ms HTTP GET 确认查询合理，避免用付费库浏览器抓取零结果或 800 页。OpenAlex 的绝对命中数不准，但方向性判断（0 / 合理 / 海量）完全够用。

### 1. 搜索（4 库并行）
```bash
# 概念拆解 → 查询生成
python scripts/pipeline/query_builder.py -c memory/search_concept.json --format commands

# 各库并行执行，每库 >= 10 篇
# 🛑 检查点 A: 每库 >= 3 篇结果？不够 → 放宽查询或标记失败
```

| 数据库 | 命令 | 提取器 |
|---|---|---|
| IEEE | `browser.open(url=...)` → wait 3s → `evaluate extractors/ieee.js` | `ieee.js` |
| Scopus | `python scripts/pipeline/scopus_search.py -q "..." -k <key> --count 15 -o memory/scopus.json` | API |
| ACM | `browser.open(url=...)` → wait 3s → `evaluate extractors/acm.js` | `acm.js` |
| EV | `act type` 填搜索框 → `act click` 搜索 → wait 3s → `evaluate extractors/engineering_village.js` | `engineering_village.js` |

结果写 `memory/<db>_results.json`。每个库失败不阻断全局。

### 2. 合并 + 补摘要
```bash
python scripts/pipeline/merge_results.py --files memory/ieee.json memory/scopus.json memory/acm.json memory/ev.json -o memory/merged.json
python scripts/pipeline/enrich_abstracts.py -i memory/merged.json -o memory/enriched.json
```

💡 **Tier 0 缓存：** `memory/paper-abstracts/` 目录持久化所有已获取的摘要。同一篇论文第二次搜索时 enrich 直接从缓存读取，零 API 调用。搜索前先 `ls memory/paper-abstracts/` 确认缓存规模——缓存越多，enrich 越快。

### 🛑 检查点 B: 摘要完整性（带降级保护）

```bash
python scripts/pipeline/check_abstracts.py
# 检查 _abstract_file 引用 + 文件内容 ≥ 80 字符
```

| 缺失率 | 操作 |
|---|---|
| ≤ 5% | ✅ 继续。缺失的标注 `[摘要缺失]` |
| > 5%（第 1 次） | 🛑 触发 Tier 2 详情页提取（见下节），补到 ≤5% |
| > 5%（第 2 次） | 🛑 Tier 2 重试（换浏览器 profile / 重新登录后重跑） |
| > 5%（第 3 次仍失败） | ⚠️ **自动降级。** 标记所有缺失论文为 `[摘要缺失-已尝试恢复]`，允许管道继续。**禁止继续重试。** |

**降级逻辑：** Tier 2 重试 2 次（即最多跑 3 次富化尝试：初始 enrich + Tier 2 #1 + Tier 2 #2）后，若缺失率仍然 > 5%，则不再阻断。此时检查点 B 视为"降级通过"——缺失的摘要不阻塞后续评分和输出，只在最终结果中明确标注来源可信度下降。

### 3. 评分 + 输出
```bash
python scripts/pipeline/paper_ranker.py -i memory/enriched.json -o memory/ranked.json -k "<关键词>" --mode balanced
python scripts/pipeline/ai_rerank.py -i memory/ranked.json -o memory/ai_ranked.json -t "<完整研究主题描述>"
python scripts/pipeline/ai_summarize.py -i memory/ai_ranked.json -o memory/summarized.json --top 15
python scripts/pipeline/theme_cluster.py -i memory/summarized.json --top 15 -o memory/themed.json -t "<研究主题>"
python scripts/pipeline/make_output.py -i memory/themed.json -o memory/final_results.md --top 15 --tier-mode percentile
python scripts/pipeline/export_citations.py --bibtex --files memory/themed.json -o memory/results.bib
```

### 🛑 检查点 C: 输出格式
- [ ] 每篇标注 `_source_db` 来源库标签
- [ ] 按 🟢🟡🟠 × 主题自动分组（`make_output.py` 输出 `final_results.md`）
- [ ] 中文摘要 + 原文链接 + BibTeX 文件

### 🔍 Schema 校验（管道每步自动执行）
- [ ] 每步出口在 `stderr` 打印 `[validate:<stage>] N errors, M warnings → pipeline_issues.json`
- [ ] 有 issue 时检查 `memory/pipeline_issues.json`，决定是否回退重跑
- [ ] 最终输出 JSON 顶层带有 `_pipeline_version` 和 `_pipeline_stage` 标记

---

## Tier 2 详情页提取（🛑 强制子代理 — 禁止主会话逐篇提取）

缺失率 > 5% 时触发。**最多重试 2 次 Tier 2**（即 enrich 总共跑 3 轮：初始 + Tier 2 #1 + Tier 2 #2）。超过后自动降级，见检查点 B。

```
1. 主会话: 写 tier2_task.json（缺摘要论文列表 + 对应 detail.js 路径）+ tier2_attempt 计数器
2. 主会话: spawn 子代理，task=见下方模板
3. 子代理: 并发打开所有 tab → 并行等待渲染 → 逐 tab evaluate → write tier2_result.json → 销毁
4. 主会话: 读 tier2_result.json → merge_tier2.py 合并 → 重新跑检查点 B
5. 若还是 > 5% 且 tier2_attempt < 2：回步骤 1，tier2_attempt += 1
6. 若 tier2_attempt >= 2 且仍 > 5%：⚠️ 自动降级，继续管道
```

🛑 **禁止主会话执行单个 navigate+evaluate。** 子代理并发 tab 模式，6 篇 ~30s（vs 串行 3min / 主会话手动 12min）。子代理销毁时摘要污染随会话释放。

### Tier 2 失败诊断（第 2 次重试前必做）

第 1 次 Tier 2 失败后、启动第 2 次前，检查失败原因：
- `tier2_result.json` 中 status: "failed" 的 reason 字段
- 大量 login_required / 403 → 浏览器登录态过期，手动刷新登录后再重试
- 大量 selector_not_found → 页面结构变化，检查对应的 `*_detail.js` 选择器
- 大量 timeout → 网络/SPA 渲染问题，换 `profile="chrome"` 重试

子代理 task 模板（错峰分批并发 + 直接写缓存）：

```
═══════════════════════════════════════════════════════════
🛑 此任务只能通过 sessions_spawn 子代理执行。
   禁止主会话逐篇 navigate+evaluate。
═══════════════════════════════════════════════════════════

Phase 0 — 准备工作：
  1. Read memory/tier2_task.json → 提取 papers 数组
  2. Read each unique detail extractor JS file ONCE (extractors/<db>_detail.js)
     将 extractor 代码存为字符串，后续 evaluate 复用

Phase 1 — 错峰分批：
  按论文数 N 决定批次大小：

  |  N   | 单批上限 | 批次数 |
  |------|---------|--------|
  | ≤7   | N       | 1      |
  | 8-14 | 7       | 2      |
  | 15-20| 7       | 3      |

  每批执行：
    a. 错峰打开 tab（间隔 0.5s，不显式 wait——连续调用 browser.open 即可，
       浏览器工具本身的调用间隔已足够分散请求）:
    b. 从最后一个 open 算起等 4-5s
    c. browser.tabs → 按 URL 匹配本批论文到 tab
    d. 逐 tab evaluate + 立即写缓存:
       For each matched paper+tab:
         result = browser.act(targetId=<id>, kind="evaluate", fn=<extractor JS>)
         result 包含: {docId, doi, title, abstract, authors, venue, year}
         如果 abstract 非空且 ≥80 字符:
           ✅ 写入缓存文件 → memory/paper-abstracts/ieee_doc_{docId}.txt
              格式: Title / Authors / Year / Venue / DOI / Citations + Abstract 正文
           ✅ 记录到结果数组: {docId, ...result, status:"ok"}
         如果 abstract 为空:
           ❌ 记录: {docId, title, status:"failed", reason:"empty_abstract"}
    e. 关闭本批所有 tab
    f. 下一批前等 2s

Phase 2 — 写入汇总文件：
  memory/tier2_result.json（JSON array，包含所有论文的完整 evaluate 返回 + status）

Phase 3 — 收尾 + 回报状态：
  关闭多余 tab（只留 1 个）。
  回报主会话: "Tier 2: N ok, M failed. docId 失败列表: [...]"
```

🛑 **关键约束：**
- 🛑 此模板仅限 sessions_spawn 子代理使用，禁止主会话执行
- Phase 0 的 extractor JS 代码必须以字符串形式传入 `evaluate` 的 `fn` 参数
- Phase 1d: evaluate 成功后**立即写缓存文件**，不等到所有 evaluate 完成
  - 缓存文件名: `memory/paper-abstracts/ieee_doc_{docId}.txt`（IEEE）或其他库对应格式
  - 缓存内容: evaluate 返回的所有字段（Title/Authors/Year/Venue/DOI/Abstract）
- 单批 ≤7 个 tab（错峰打开 + 反爬安全余量）
- 错峰间隔 0.5s（模拟人类操作，不被反爬识别）
- Phase 3 只回报状态行，不做表格、不做格式化

---

## 输出格式（theme_cluster.py 自动生成）

```markdown
## 🔬 主题 · 精选 N 篇（来源: IEEE/Scopus/ACM/EV）

### 🟢 一、{自动识别的主题名}（N 篇）
**1. 标题** [来源库]
👤 作者 · 📅 年份 · 📊 引用 N · 🏛️ 期刊/会议
🔗 原文链接
💡 中文摘要（200-300字）

### 🟡 二、{自动识别的主题名}（N 篇）
...

### 🟠 三、{自动识别的主题名}（N 篇）
...

---
📊 统计: 检索总量 | 各库分布 | BibTeX: memory/results.bib


---

## ⏱️ 各环节耗时 & Token 参考（38 篇论文，deepseek-v4-pro）

| 环节 | 耗时 | Token 消耗 | 瓶颈 |
|---|---|---|---|
| 0.5 免费预检 (OpenAlex) | < 1s | 0 | 纯 HTTP |
| 1a. IEEE 搜索 (浏览器) | ~10s | ~500 | 页面加载 |
| 1b. Scopus 搜索 (API) | ~5s | 0 | API 延迟 |
| 1c. ACM 搜索 (浏览器) | ~10s | ~500 | 页面加载 |
| 1d. EV 搜索 (浏览器) | ~15s | ~500 | SPA 渲染 |
| 2a. 合并 + 去重 | < 1s | 0 | 本地计算 |
| 2b. enrich Tier 0-1 (缓存+免费API) | ~30s（~38篇） | ~800 | SS/OpenAlex API 限速 3s/req |
| 2c. enrich Tier 2 (子代理, 6篇 IEEE) | ~45s | ~10k | 错峰 open → 并行渲染 → 串行 evaluate |
| 3a. 评分 (paper_ranker) | < 1s | 0 | 本地计算 |
| 3b. AI 重排 (ai_rerank, 38篇) | ~65s | ~15k | LLM API 并发8 |
| 3c. AI 中文摘要 (ai_summarize, 38篇) | ~30s | ~9k | LLM API 并发8 |
| 3d. 主题聚类 | < 2s | 0 | 本地 |
| 3e. 输出 Markdown + BibTeX | < 2s | 0 | 本地 |
| **总计** | **~3.5 min** | **~70k** | |

### 加速建议

| 问题 | 方案 |
|---|---|
| ~~Tier 2 子代理慢（3min/6篇）~~ | ✅ **已解决：** 子代理并发打开 N 个 tab，并行等渲染，逐 tab evaluate。3min → 30s |
| AI 重排 65s | 已用并发 8，瓶颈在 API 速率限制 |
| enrich 30s (SS/OpenAlex) | 可调 `--delay` 参数到 1.5s（需注意 429） |
| 搜索阶段串行 | 四库可以**真并行**（每个搜索 spawn 子代理） |

**Tier 2 已并行化（✅ 本文档已更新）：** 子代理 Phase 1 并发打开所有 tab，Phase 2 统一等待渲染，Phase 4 逐 tab evaluate。6 篇 IEEE 详情页 30 秒搞定。
