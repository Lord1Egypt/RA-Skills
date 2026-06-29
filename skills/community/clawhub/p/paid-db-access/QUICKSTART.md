# QUICKSTART.md — 10 分钟跑通第一条文献检索

> Paid Database Access 是一个 AI 驱动的付费学术数据库检索管道。
> 通过浏览器接管你的机构登录态，搜索 IEEE / Scopus / ACM / Engineering Village，
> 自动去重、补摘要、评分排序、输出结构化文献综述 + BibTeX。

---

## 你需要什么

| 条件 | 说明 |
|---|---|
| 机构账号 | 能登录 IEEE Xplore / Scopus / ACM DL / Engineering Village 中至少一个 |
| Scopus API Key | [免费注册](https://dev.elsevier.com)，机构邮箱即可（仅 Scopus 需要） |
| OpenClaw 浏览器 | `browser.start(profile="openclaw")` |
| Python 3.10+ | 已安装，带 `pyyaml` |

---

## 5 分钟上手

### 1. 写检索概念

创建 `memory/search_concept.json`：

```json
{
  "core_concepts": ["你的研究主题关键词"],
  "synonyms": {},
  "sub_topics": ["子方向1", "子方向2"],
  "exclude": ["排除词"],
  "year_range": "2023-2026",
  "databases": ["ieee", "scopus", "acm", "engineering_village"]
}
```

### 2. 环境检查

```bash
python scripts/pipeline/setup.py --check
```

### 3. 免费预检（确认查询合理，避免零结果）

```bash
python scripts/pipeline/free_precheck.py -c memory/search_concept.json --json
```

> 命中 3-2000 → ✅ 继续。≤3 → 放宽概念。>2000 → 收紧范围。

### 4. 生成查询 + 四库搜索

```bash
# 生成各库搜索命令
python scripts/pipeline/query_builder.py -c memory/search_concept.json --format commands

# 执行搜索（以 IEEE 为例，其他库同理）
# 打开浏览器 → 登录 → 运行搜索 URL → evaluate 提取
```

### 5. 合并 + 补摘要 + 评分 + 输出

```bash
python scripts/pipeline/merge_results.py \
  --files memory/ieee.json memory/scopus.json memory/acm.json memory/ev.json \
  -o memory/merged.json

python scripts/pipeline/enrich_abstracts.py \
  -i memory/merged.json -o memory/enriched.json -k "$SCOPUS_API_KEY"

python scripts/pipeline/paper_ranker.py \
  -i memory/enriched.json -o memory/ranked.json \
  -k "你的关键词" --mode balanced

python scripts/pipeline/ai_rerank.py \
  -i memory/ranked.json -o memory/ai_ranked.json \
  -t "完整的研究主题描述"

python scripts/pipeline/ai_summarize.py \
  -i memory/ai_ranked.json -o memory/summarized.json --top 15

python scripts/pipeline/theme_cluster.py \
  -i memory/summarized.json --top 15 -o memory/themed.json \
  -t "研究主题"

python scripts/pipeline/make_output.py \
  -i memory/themed.json -o memory/final_results.md --top 15

python scripts/pipeline/export_citations.py \
  --bibtex --files memory/themed.json -o memory/results.bib
```

### 6. 查看结果

```bash
cat memory/final_results.md
```

输出格式：
```markdown
## 🔬 主题 · 精选 15 篇（来源: IEEE/Scopus/ACM/EV）

### 🟢 一、自动识别的主题 A（5 篇）
**1. 论文标题** [IEEE]
👤 作者 · 📅 2025 · 📊 引用 42 · 🏛️ 期刊名
🔗 原文链接
💡 中文摘要（200-300字）
...
```

---

## 🎬 IEEE 现场演示 — 为什么你需要这个工具

**IEEE Xplore 没有公开搜索 API。** 普通 HTTP 请求拿不到 IEEE 的论文列表——它只服务于浏览器里的真人用户。

而这个工具通过 **浏览器 CDP 接管**，用你的眼睛（登录态）去看 IEEE 的页面，用 JS 提取器把结果变成结构化数据。这是它跟所有"API 聚合搜索"工具的本质区别。

### 30 秒跑通 IEEE 搜索

假设你的 AI agent 已启动 OpenClaw 浏览器（`browser.start`），对话如下：

```
👤 你：帮我在 IEEE Xplore 搜索 "autonomous scientific discovery"，
      2023-2025 年的论文，取前 10 篇。

🤖 Agent：
  1. browser.open → https://ieeexplore.ieee.org/search/searchresult.jsp?
     queryText=autonomous+scientific+discovery&ranges=2023_2025_Year
  2. 等待 3 秒页面渲染
  3. browser.act(kind="evaluate", fn=<extractors/ieee.js>)
  4. 返回结构化 JSON →
```

**提取结果（真实输出格式）：**
```json
{
  "totalResults": 1247,
  "papers": [
    {
      "title": "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery",
      "authors": "Lu, Chris; Lu, Cong; Lange, Robert Tjarko; ...",
      "year": 2024,
      "venue": "arXiv",
      "citations": 156,
      "doi": "10.48550/arXiv.2408.06292",
      "link": "https://ieeexplore.ieee.org/document/12345678",
      "isOA": true
    }
    // ... 9 篇更多
  ]
}
```

### 然后呢？一键走完剩余管道

```bash
# 搜索结果已存为 memory/ieee_results.json
# 如果你还搜了其他库，合并即可：
python scripts/pipeline/merge_results.py \
  --files memory/ieee.json -o memory/merged.json

python scripts/pipeline/enrich_abstracts.py \
  -i memory/merged.json -o memory/enriched.json

python scripts/pipeline/ai_rerank.py \
  -i memory/enriched.json -o memory/ai_ranked.json \
  -t "autonomous scientific discovery with AI agents"

python scripts/pipeline/ai_summarize.py \
  -i memory/ai_ranked.json -o memory/summarized.json --top 10

python scripts/pipeline/theme_cluster.py \
  -i memory/summarized.json --top 10 -o memory/themed.json \
  -t "AI Autonomous Scientific Discovery"

python scripts/pipeline/make_output.py \
  -i memory/themed.json -o memory/final_results.md --top 10

python scripts/pipeline/export_citations.py \
  --bibtex --files memory/themed.json -o memory/results.bib
```

**30 秒搜索 + 2 分钟后处理 = 一篇带中文摘要 + BibTeX 的文献综述。**

### 对比：有/没有这个工具

| | 手动翻 IEEE | 用 paid-db-access |
|---|---|---|
| 搜索 | 点开网页 → 敲关键词 → 翻页 → 一篇篇点进去看摘要 | 一句话，30 秒出 JSON |
| 去重 | 手动对比四个数据库 | `merge_results.py` 自动 |
| 摘要 | 逐篇打开详情页，复制粘贴 | `enrich_abstracts.py` 自动补全 + Tier 2 兜底 |
| 评分 | 凭感觉 | AI 三维语义评分 (relevance/quality/novelty) |
| 输出 | 浏览器书签 + Word 文档 | Markdown 综述 + BibTeX，直接导入 Zotero |
| 下次搜 | 从零开始 | 摘要缓存命中，秒出 |

---

## 完整示例

假设你研究 **AI 自动科研**：

**`memory/search_concept.json`：**
```json
{
  "core_concepts": ["autonomous scientific discovery", "AI automated research"],
  "synonyms": {
    "AI": ["LLM", "large language model", "artificial intelligence"]
  },
  "sub_topics": [
    "automated paper generation",
    "scientific hypothesis generation",
    "experiment automation agent"
  ],
  "exclude": ["healthcare", "clinical", "drug discovery"],
  "year_range": "2023-2026",
  "databases": ["scopus", "ieee", "acm", "engineering_village"]
}
```

**运行后得到：**
- `memory/final_results.md` — 15 篇精选论文，按主题分组 + 中文摘要
- `memory/results.bib` — BibTeX，可直接导入 Zotero/EndNote
- `memory/paper-abstracts/` — 全部摘要缓存，后续搜索即时命中

---

## 首次使用最可能遇到的坑

| 问题 | 解决 |
|---|---|
| 搜索零结果 | 先跑 `free_precheck.py`，放宽 `core_concepts` 或去掉部分 `exclude` |
| Scopus API 403 | 不在机构 IP，需连 VPN |
| 浏览器 evaluate 返回 count:0 | 数据库前端改版，跑探路诊断 JS，更新 extractor |
| 摘要大量缺失 | 自动触发 Tier 2 子代理补全（浏览器逐个打开详情页），等待 1-2 分钟 |
| ACM 详情页 503 | 在浏览器中手动登录一次 ACM，Cookie 持久化后即可 |

---

## 下一步

- 阅读 `SKILL.md` — 完整管道规范，含 Tier 2、检查点、子代理并发
- 阅读 `REFERENCE.md` — 各数据库细节、故障速查、提取器调试
- 调整 `paper_ranker.py --mode`（`recall` / `precision` / `balanced`）改变评分策略
- 设置 `monitor.py` 定时扫描新论文

---

## 项目结构

```
paid-db-access/
├── SKILL.md              # 完整管道规范
├── REFERENCE.md          # 各数据库参考手册
├── QUICKSTART.md         # ← 你在这里
├── config.yaml           # 数据库配置 + API Key
├── extractors/           # JS 页面提取器 (IEEE/Scopus/ACM/EV)
├── scripts/
│   ├── pipeline/         # 核心管道 (15 个脚本)
│   ├── utils/            # 支撑工具
│   └── extra/            # 附加功能 (监控/下载)
└── memory/               # 检索结果（管道输出目录）
    ├── search_concept.json   # ← 从这里开始
    └── paper-abstracts/      # 摘要缓存（越用越快）
```
