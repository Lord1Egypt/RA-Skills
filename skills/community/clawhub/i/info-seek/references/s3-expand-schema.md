# S3 扩样选种数据格式 (s3-expand-schema)

> 配套脚本：`scripts/s3_expand.py` (mod-v1.0.0)
> 吸收 `workspace/s2_anchor_observe/` 一次性观测脚本（`observe_anchors_s3.py` /
> `filter_pipeline_s3.py` / `select_seeds_s4.py`）的可复用固化口径。
> 数据格式对齐 `core/learned_anchor_store.py` provenance 字段，便于回填生产锚点库。

---

## 1. Corpus（语料）

### 1.1 合成语料（`make_synthetic_corpus` 产出）
内存结构：`Dict[topic:str, List[doc:str]]`，`topic ∈ TOPIC_TERMS`（11 主题），每主题 ≥20 篇。

落盘格式（当 `out_dir` 给定）：
```
<out_dir>/corpus/<topic>_<NN>.txt     # NN=01..20，正文无 DATE: 前缀
```
正文为连续中文，真锚/实体/通用框架词/碎片子串按 `_build_doc` 模板拼接。

### 1.2 真实语料（`load_corpus` 加载）
- 扁平目录 `*.txt`，文件名 `topic_NN.txt`，topic 取 `_` 前段；
- 或每主题一子目录 `<topic>/xxx.txt`。

---

## 2. Candidates（候选，extract_candidates 内存结构）

`List[Dict]`，每条：
```json
{
  "term": "技术壁垒",
  "doc_hits": 12,
  "freq_total": 38,
  "topic_cross_count": 4,
  "cat_cross_count": 2,
  "consensus_doc_hits": 12
}
```
- `doc_hits`：出现文档数（同篇去重）
- `freq_total`：总出现次数（含同篇重复）
- `topic_cross_count`：跨主题数（主门阈值 ≥3）
- `cat_cross_count`：跨大类数（A 通用跨域 / B 金融大宗；通用桶阈值 ≥2）
- `consensus_doc_hits`：≥2 篇出现（共识）

抽取：jieba 分词 token 优先（无 jieba 降级 n-gram）；`doc_hits>=3` 且非 `STOPWORDS` 且 `len>=3`。

---

## 3. anchors_filtered_S3.json（过滤管线 P0-P3 输出）

```json
{ "anchors": [ { ... }, ... ] }
```
单项：
```json
{
  "term": "技术壁垒",
  "pos": "n",
  "is_entity": false,
  "is_generic": false,
  "cover": 1.0,
  "drop_gates": [],
  "topic_cross_count": 4,
  "cat_cross_count": 2,
  "doc_hits": 12,
  "consensus_doc_hits": 12,
  "freq_total": 38
}
```
- `pos`：jieba.posseg（锁定领域词强制 `n`，见脚本 `_preprocess`）
- `is_entity`：内置实体名或实体后缀（ORG/PRODUCT/PERSON）
- `is_generic`：由 `build_generic_bucket` 回填（`true` 则选种排除）
- `cover`：jieba 分词边界对齐占比（P1 碎片门，阈值 `COVER_MIN=0.15`）；无 jieba 时为 `null`
- `drop_gates`：`["len"|"non_cn"|"time"|"conn"|"tmpl"|"fragment"]`，空=通过

---

## 4. generic_bucket_S3.json（通用词桶，半自动）

```json
{ "generic_terms": ["产能", "需求", "集中度", "产业链", "成本", "商业模式", "供应链", "供给", "规模", "市场份额"] }
```
规则（S3_扩样校准结论.md §3）：显式白名单 `GENERIC_TERMS` +（后缀 `格局/规模/链/份额/模式/体系/生态/逻辑/路径/结构/中枢/趋势` 或前缀 `同比/环比/市场/核心/...`）且 `cat_cross_count>=2` 且 `cover>=0.9`；剔除实体与真锚（`TRUE_ANCHOR_TERMS`）。

---

## 5. learned_seeds_S4.json（选种主门输出）

```json
{
  "meta": {
    "phase": "S4",
    "rule": "topic>=3&cover>=0.9&noun_pos",
    "n_seeds": 8,
    "n_watch_topic2": 3,
    "excluded_breakdown": { "entity": 15, "generic": 13, "fragment": 2, "non_noun_pos": 2 },
    "intra_seed_substring_pairs": []
  },
  "seeds": [
    {
      "term": "技术壁垒", "status": "pending", "topic_cross_count": 4,
      "cat_cross_count": 2, "cover": 1.0, "doc_hits": 12,
      "consensus_doc_hits": 12, "freq_total": 38, "pos": "n", "len": 4
    }
  ],
  "watch_topic2": [
    {
      "term": "减速器技术", "topic_cross_count": 2, "cat_cross_count": 2,
      "cover": 1.0, "doc_hits": 14, "pos": "n", "len": 4
    }
  ]
}
```

### 选种主门（select_seeds）
- **硬排除**：`is_entity` / `is_generic` / 内置 `_ZH_HIGH_FREQ` / `drop_gates` 非空 / `len<2` / `pos not in NOUN_POS`
- **seeds(pending)**：`topic_cross_count>=3` 且 `cover>=0.9`（或 null）且 名词性 pos
- **watch_topic2**：`topic_cross_count==2` 且 名词性 pos（观察桶，待真实样本确认升级）

`NOUN_POS = {n, nz, nv, nvn, vn, nt, ns, nns}`；名词性判定对锁定领域词强制 `n`（规避 jieba 未登录 4 字词标 `x` 误杀，S3 结论 §2）。

---

## 6. 阈值敏感性网格（threshold_grid_scan 输出）

```json
{
  "cover_fragment_reject": { "0.05": 0, "0.1": 0, "0.15": 2, "0.2": 4, "0.3": 6 },
  "topic_seeds": { "2": 11, "3": 8, "4": 8 }
}
```
- `cover_fragment_reject`：各 cover 阈值下碎片拒绝数（拐点选 `0.15`）
- `topic_seeds`：各 topic 主门阈值下 seeds 数（稳定点选 `>=3`）

---

## 7. CLI
```bash
python scripts/s3_expand.py --demo                 # 合成语料(11×20)全链 self-check
python scripts/s3_expand.py --corpus DIR --out DIR  # 真实语料 → 选种（写 3 个 json）
python scripts/s3_expand.py --grid                 # 仅跑阈值敏感性网格
```
