# GPA 更新日志（原 DGRA - Dynamic Genomic Risk Assessment）

## [v0.8.0] - 2026-05-23

### SpliceAI 剪接预测集成（P5）

**目标**：对 canonical splice（acceptor/donor）和 splice_region 变异自动查询 SpliceAI delta score，作为剪接功能影响的独立证据，修正 VEP HIGH 剪接过调用（false positive）。

**默认关闭** — 仅当用户显式提供 `--spliceai` 时启用。

#### 1. 新增 `scripts/dgra_splice_predictor.py`
- `SpliceAIPredictor` 类：异步批量查询 Broad Institute SpliceAI lookup API
- 并发限制：`asyncio.Semaphore`（默认 5，CLI `--spliceai-concurrency` 可调）
- 指数退避重试：HTTP 429/502/503/504 + `asyncio.TimeoutError` → 1s→2s→4s
- 内存缓存：同分析内重复查询去重
- Graceful fallback：
  - API 失败 → `source="api_error"`，QC flag `SPLICEAI_API_ERROR`
  - 不在数据库 → `source="not_in_db"`，不阻断分析
- 阈值体系：
  - canonical（acceptor/donor）：strong≥0.5 / moderate≥0.2 / weak≥0.1
  - splice_region：strong≥0.2 / moderate≥0.1 / weak≥0.05
- 模块级兼容函数：`query_spliceai_batch()`、`should_query_spliceai()`、`reset_spliceai_cache()`、`_cache_key()`

#### 2. `dgra_core.py` 集成
- `Variant` dataclass 新增 `spliceai_result: Optional[Dict[str, Any]]`
- `GPAConfig` 新增 `spliceai_enabled`（默认 False）、`spliceai_concurrency`（默认 5）
- `run_dgra_pipeline()` Step 6.75：
  - 在表型关联（Step 6.5）与分级（Step 7）之间插入
  - 仅对 `should_query_spliceai()` 返回 True 的变异批量查询
  - 结果写入 `variant.spliceai_result`
- `classify_variant_tier()` 新增 SpliceAI evidence 链：
  - **Tier 1 降级**（NMD-sensitive canonical splice）：delta=0 → weight=-0.5，降级为 Tier 2
  - **Tier 2 降级**（tissue-relevant canonical splice）：delta=0 → weight=-0.5，降级为 Tier 3
  - **Tier 3 升级**：delta≥0.5（strong）→ weight=0.8，升级为 Tier 2
  - **Tier 3 moderate**：delta≥0.2 → weight=0.4，保留 Tier 3
  - **not_in_db** → evidence weight=0（仅记录）
  - **api_error** → QC flag `SPLICEAI_API_ERROR`

#### 3. CLI 扩展（`dgra_cli_wrapper.py` + `dgra_core.py`）
- `--spliceai`：显式开启 SpliceAI 查询
- `--spliceai-concurrency`：最大并发数（默认 5）
- 参数透传：`main()` → `run_gpa_from_file()` → `run_gpa()` → `GPAConfig` → `run_dgra_pipeline()`

#### 4. 测试套件（`tests/test_spliceai.py`）
| 测试 | 场景 | 结果 |
|------|------|------|
| PYGL 降级 | canonical splice + delta=0 | Tier 2 → 3 ✅ |
| 强剪接升级 | canonical splice + delta=0.8 | Tier 3 → 2 ✅ |
| 不在数据库 | not_in_db | 不崩溃，evidence 记录 ✅ |
| API 失败 | api_error | 不崩溃，QC flag ✅ |
| 未开启一致 | spliceai_enabled=False | 无 SpliceAI evidence ✅ |
| 非剪接不查 | missense/stop_gained | should_query=False ✅ |
| 阈值分级 | canonical/splice_region | determine_impact ✅ |
| 阈值配置 | 0.5/0.2/0.1 vs 0.2/0.1/0.05 | 正确 ✅ |
| canonical vs region | 区分 acceptor/donor vs region | 正确 ✅ |
| Async mock | mocked API 响应 | batch 查询 ✅ |

**10/10 通过**

---

### P2: 中文 VEP 术语映射 + P6: gnomAD 频率接入 pipeline

**P2 — 中文适配器**：`dgra_adapters.py` 新增 `CN_EXONIC_FUNC_MAP`，支持国内测序公司（诺禾致源、华大基因）中文 VEP 注释输出。`_infer_impact()` 已委托 `gpa_i18n.py` 统一处理中英文 consequence 术语。

**P6 — gnomAD 频率接入**：修复 `query_gnomad_variant()` 已实现但从未被调用的阻断性缺陷。`run_dgra_pipeline()` 现在对 `gnomad_af=None` 的变异自动批量查询 gnomAD GraphQL API，结果写入 `variant.gnomad_af` 和 `variant.gnomad_populations`。频率降级逻辑（BA1: AF>1% → Tier 3）现已生效。

---

## [v0.7.2] - 2026-05-23

### ClinVar Review Status 星级纳入置信度评估

**目标**：解决 P4 — ClinVar 判断只看文本不看提交者星级的问题。

**1. 新增 `_parse_clinvar_confidence()`（`dgra_core.py`）**
- CLNREVSTAT 文本 → 置信度权重（0.30~0.95）
  - `practice_guideline` → 0.95（★★★★ 实践指南认可）
  - `reviewed_by_expert_panel` → 0.80（★★★☆ 专家小组审核）
  - `multiple_submitters_no_conflict` → 0.55（★★☆☆ 多提交者一致）
  - `single_submitter` → 0.40（★☆☆☆ 单一提交者）
  - 缺失 / `no_assertion` / `conflicting` → 0.30

**2. Pathogenic evidence weight 乘以星级**
- 4 个 pathogenic 调用点（coagulation、HIGH+tissue-relevant、phenotype mismatch、non-tissue-relevant）全部 weight × clinvar_conf
- 原始 weight 1.0 → 有效范围 0.30~0.95
- Confidence level 根据星级动态调整：≥0.8 high，≥0.5 medium，<0.5 low

**3. Benign evidence 新增负权重**
- Tier 3 benign 分支新增独立 ClinVar evidence：weight = -0.5 × clinvar_conf
- 高星级 benign 排除信号更强（-0.475），低星级更弱（-0.15）

**4. 输入层支持 CLNREVSTAT**
- `dgra_cli_wrapper.py`：REQUIRED_COLS + OPTIONAL_DEFAULTS 新增 `CLNREVSTAT`
- `dgra_core.py` TSV 解析器：读取 CLNREVSTAT 传入 Variant 构造函数
- Variant dataclass 新增 `clinvar_review_status: Optional[str]`

**关键边界：**
- 冲突注释（v0.7.1 P3）优先于星级 — `_clinvar_is_conflicting` 返回 True 时 pathogenic/benign 均返回 False
- `Pathogenic/Likely_pathogenic` 复合评级正常处理
- 缺失 CLNREVSTAT → 保守 weight × 0.30

**测试**：
- A-Layer 回归：11/11 ✅
- CLNREVSTAT 专项：5/5 ✅（practice_guideline 0.95、single_submitter 0.40、missing 0.30、benign multi-submitter -0.275、conflicting priority）

---

## [v0.7.1] - 2026-05-23

### P010 三问题修复：ClinVar 冲突检测 + 中英文映射 + 预过滤

**1. Phase 1: ClinVar 冲突注释检测（P3）**
- 新增 `_clinvar_is_conflicting()`：正反同时存在（如 "良性, 致病"）→ True
- 标准复合评级（`Pathogenic/Likely_pathogenic`）不算冲突
- 冲突变异标记 `CLINVAR_CONFLICTING` qc_flag，weight=0，不触发 Tier 升级

**2. Phase 2: 统一中英文 consequence 映射（P2）**
- 新建 `gpa_i18n.py`：`CONSEQUENCE_MAP` 40+ 中文→英文术语，`normalize_consequence()`、`infer_impact_from_consequence()`
- `dgra_adapters.py` 的 `_infer_impact()` 委托给 `gpa_i18n`

**3. Phase 3: 预过滤模块（P1）**
- 新建 `dgra_variant_filter.py`：strict/clinical/broad 三档过滤
  - strict：仅 HIGH/MODERATE
  - clinical：+ 剪接区 LOW + 组织相关基因同义 + ClinVar 冲突保留
  - broad：+ LOW
- `dgra_cli_wrapper.py` 新增 `--filter-preset` CLI 参数
- 报告头部显示过滤统计（Input → Output 计数、Impact 分布、保留明细）

**4. Phase 4: 文档同步**
- `SKILL.md` 更新：版本号、过滤 preset 用法、中英文映射表、ClinVar 冲突说明
- `dgra.yaml` 更新：版本号、新增 `filter_presets` 配置段

**测试全绿：** A-Layer 11/11、中英文映射 8/8、过滤模块三档正确、ClinVar 冲突端到端通过

---

## [v0.7.0] - 2026-05-23

### Phase 4: 报告模板重写 + 表型关联评估章节

**目标**：完成 GPA v0.7 品牌化后的报告模板重构，新增表型关联独立评估章节，彻底清理供者/移植相关术语。

**1. 新增表型关联评估章节（`_generate_phenotype_assessment_section()`）**
- **位置**：Markdown 报告中 Multi-hit 章节之后、Tier 1 之前
- **汇总表**：基因 / 位点 / 合子型 / VAF / 匹配评分 / 关联等级（🟢高度/🟡中度/🔴低度）/ 假基因状态 / 建议
- **逐变异分析**：表型匹配评分、解释、匹配对、基因已知表型、当前分级
- **ClinVar Pathogenic + 低分警告**：明确提示 "ClinVar 致病性标注但与输入表型匹配度低，建议结合临床表现验证"
- **高分验证建议（≥0.75）**：Sanger / 长读长测序 / 家系共分离 / 功能实验

**2. JSON 报告扩展**
- 新增 `phenotype_association` 顶层字段：
  - `total_tier12_with_phenotype`: 执行表型关联的变异数
  - `high_match_count`: 高分匹配（≥0.75）变异数
  - `variants[]`: 逐变异表型关联详情（score/confidence/explanation/matched_pairs/known_list）

**3. 供者术语清理**
- `TIER1_ACTION_GENES["VWF"]`："collection safety" → "vWD risk in patient"
- `classify_variant_tier()` Priority 1 注释："donor safety logic" → "disease risk logic"
- Action 字符串："affects collection safety (coagulation gene)" → "in coagulation gene — bleeding risk"
- Tier 1/2 报告描述："intervention" → "clinical attention"，"patients should be informed" → "clinical significance"

**4. 版本与方法论更新**
- 报告标题：v0.5 → v0.7
- `_get_version_info()`: 0.5.3 → 0.7.0
- 方法学附录：新增 Step 6 "表型关联分析（v0.7）"

**测试**：
- A-Layer 回归：11/11 ✅
- Phase 2 表型关联：6/6 ✅
- Phase 3 分级逻辑：6/6 ✅
- 自定义报告验证：Markdown + JSON 均正常 ✅

---

## [v0.6.2] - 2026-05-22

### 品牌重定位：DGRA → GPA (Genomic Phenotype Association)

- **核心功能不变**：基因变异分级、组织相关性评估、多维度注释
- **定位调整**：从"供者安全评估"扩展为"基因-表型关联分析"
- **适用场景**：遗传病诊断、携带者筛查、药物基因组、供者评估
- **命名更新**：
  - `README.md` — 标题、描述、所有引用统一为 GPA
  - `SKILL.md` — 描述头更新
  - `CHANGELOG.md` — 更新为 GPA 更新日志
  - 代码中报告输出字符串更新（类名/模块名保留向后兼容）
- **代码层面**：模块名 `dgra_core.py`、类名 `DGRAConfig` 等保留，仅用户可见字符串更新

---

## [v0.6.1] - 2026-05-22

### A-Layer：构建流程稳定性增强

**目标**：长耗时构建任务（基因同步、假基因索引、VEP重注释）在弱网/限流环境中容易中断，增加三层防护。

**1. 指数退避重试（`scripts/dgra_api.py`）**
- 所有外部 API 统一通过 `_request_with_retry()` 收敛
- 新增 HTTP 429 处理：读取 `Retry-After` header，按服务器建议等待
- 新增 HTTP 502/503/504 处理：指数退避 1s→2s→4s
- `asyncio.TimeoutError` / `ClientError` 同样触发指数退避
- 日志格式：`[DGRA API] {api_name}: {error}, retrying in Xs (attempt N/M)`

**2. 流式下载 + 断点续传（`scripts/dgra_pseudogene_sync.py`）**
- 替换 `urllib.request.urlretrieve` → `_download_gtf_streaming()`
- chunk_size = 8KB，每 10 MB 打印进度
- HTTP `Range` header + `206 Partial Content` 断点续传
- 状态集成：`sync_gencode_pseudogenes()` 完成后写入 `.dgra_build_state.json`

**3. 全局构建状态持久化（`scripts/dgra_build_state.py`，新增）**
- `.dgra_build_state.json` 记录每个步骤的 status/timestamp/data
- `BuildStep` 上下文管理器：原子化 `in_progress → complete/failed` 记录
- API：`save_state()` / `load_state()` / `get_step_status()` / `is_step_complete()` / `reset_state()`
- 最佳努力：读写失败不阻塞主流程（`except Exception: pass`）

**4. 回归测试（`tests/test_a_layer.py`，新增）**
- 11 项测试覆盖：429 Retry-After、503 指数退避、超时重试链、断点续传、状态恢复、BuildStep 上下文、BuildStep 异常、save/load、get_step_status、is_step_complete、reset_state
- 全部 PASS（17.0s）

**新增文件**：
- `scripts/dgra_build_state.py` — 全局构建状态持久化
- `tests/test_a_layer.py` — A-Layer 回归测试套件

**修改文件**：
- `scripts/dgra_api.py` — `_request_with_retry()` 增强（429/502/503/504/timeout）
- `scripts/dgra_pseudogene_sync.py` — `_download_gtf_streaming()` + 状态集成
- `README.md` — 新增 "构建流程稳定性" 章节 + 版本历史更新

---

## [v0.6.0] - 2026-05-22

### 假基因架构升级（Pseudogene Architecture）

**问题**：VWF p.Gln1311Ter 在女儿供者分析中 VAF=13.3%（预期杂合~50%），疑似 VWFP1 假基因干扰。原有硬编码5基因检查不足以覆盖临床场景。

**解决方案**：
- **轻量版假基因数据库**：`references/pseudogene_lookup.json`，51个临床相关假基因对（VWF/GBA/PMS2/PTEN/CYP2D6/HBA/GUSB/SETBP1等）
- **VAF模式检测**：0-1评分，4级分类：
  - `strong_interference` (≥0.75)：VAF < 0.20，confidence → LOW
  - `interference` (≥0.40)：VAF < 0.30，confidence → MEDIUM
  - `suspected` (≥0.40)：VAF < 0.40，confidence → MEDIUM
  - `bias_suspected` (>0)：VAF > 0.65，confidence → MEDIUM
- **Tier不变confidence降级原则**：不直接修改Tier，仅下调置信度，保持原有分类框架
- **独立Markdown报告章节**：汇总表、详细分析、重点关注（评分≥0.75强烈建议验证）
- **查询函数**：`get_pseudogenes_for_gene()`，解析顺序：本地lookup → legacy DB → (未来) Ensembl REST
- **向后兼容**：`pseudogene_database.json`仍作为fallback
- **GENCODE同步保留**：`scripts/dgra_pseudogene_sync.py`为未来大规模自动同步预留

**新增文件**：
- `references/pseudogene_lookup.json` — 51个假基因对（含notes、chromosome、detection_strategy、confidence）
- `scripts/dgra_pseudogene_sync.py` — GENCODE v48流式同步+查询API

**修改文件**：
- `scripts/dgra_core.py` — 新增 `_calculate_pseudogene_score()`、`get_pseudogenes_for_gene()`、重写 `detect_pseudogene_artifact()`、集成证据链(weight=0)、新增 `_generate_pseudogene_assessment_section()`、报告自动插入

**设计决策**：
- 放弃下载整份56MB GENCODE GTF（EBI速度慢），改用轻量版本地JSON
- 协调者手动录入Top 50临床相关对，精确控制
- 未来可扩展：Ensembl REST API按需查询、GENCODE完整同步

---

## [v0.5.3] - 2026-05-22

### 版本号统一升级

- 全仓库版本号对齐：v0.5.2 → **v0.5.3**
- 修改位置：
  - `scripts/dgra_core.py` — `_get_version_info()` 返回 `"0.5.3"`
  - `scripts/dgra_core.py` — Markdown 报告 fallback `'0.5.3'`
  - `README.md` — 标题、YAML 示例、当前版本声明
  - `SKILL.md` — 描述头
  - `references/dgra.yaml` — 配置模板
- 无功能变更，纯版本号对齐，为后续 v0.5.3 功能开发准备基线

---

## [v0.5.2] - 2026-05-22

### 核心功能 — VEP Canonical Reannotation (Transcript Discrepancy Fix)

**问题**：ANNOVAR/VEP/SnpEff 选择的 "首选转录本" 与 Ensembl canonical 不一致，导致非编码转录本（NR_/XM_）被标注为 `splice_donor_variant`/`HIGH`，但 canonical 蛋白编码转录本（NM_/ENST_）下同一变异实为 `upstream_gene_variant`/`MODIFIER`。`HIGH` 被错误送入 `classify_variant_tier()`，产生假阳性 Tier 1。

**解决方案**：
- **Step 1.5 新增 `batch_query_vep_region()`**：收集 Step 1 中 `TRANSCRIPT_DISCREPANCY` 变异，用 Ensembl VEP API 以 `canonical=1&domains=1&protein=1&hgvs=1&mane_select=1` 重新注释
- **解析优先级**：canonical → MANE Select → protein_coding
- **覆盖字段**：`consequence`, `impact`, `hgvsc`, `hgvsp`, `transcript`
- **`transcript_warning.vep_reannotation`**：记录 original vs canonical 对比，Markdown 报告中加 ⚠️ 标注
- **失败/离线降级**：`quality_confidence="LOW"`, `tier_confidence="LOW"`, `vep_reannotation_failed=True`
- **Domain mapping 顺序修正**：Step 1.5 在 Step 4 之前，修正后的 HGVSp 自动流入 UniProt 功能域映射

**典型案例 — CRIP2 chr14:105473030**：
| 阶段 | 转录本 | 后果 | 影响 | 最终分级 |
|:---|:---|:---|:---|:---|
| 原始（ANNOVAR） | `NR_073082` | `splice_donor_variant` | **HIGH** | 可能 Tier 1 |
| VEP reannotation | `NM_001312` | `upstream_gene_variant` | **MODIFIER** | **Tier 3** |

**验证**：`test_vep_reannotation_e2e.py` 端到端测试通过（9 步 Pipeline 验证）。

**相关文件**：
- `scripts/dgra_api.py` — 新增 `query_ensembl_vep_region()`, `_parse_vep_batch_response()`, `batch_query_vep_region()` (+216 行)
- `scripts/dgra_core.py` — Step 1.5 插入 `run_dgra_pipeline()` (+104 行)，`transcript_warning` fallback confidence 降级，`_format_vep_reannotation_note()` 报告增强 (+~50 行)
- `scripts/test_vep_reannotation.py` — 3 个单元测试（canonical/MANE/protein_coding fallback）
- `scripts/test_vep_reannotation_e2e.py` — CRIP2 端到端测试（9 步验证）

### 核心逻辑修正（v0.5.2 同时包含）
- **Multi-hit 不再升级变异**：只标记 multi-hit 基因，各变异独立分级（Tier 1: 301→4 突变）
- **ClinVar 中文注释支持**：`_clinvar_pathogenic` 同时匹配 "Pathogenic" 和 "致病"
- **新增 Priority 1c**：ClinVar 致病 + HIGH + 组织相关无路可走 → Tier 1（CD36 正确分级）
- **Transcript discrepancy 降级**：NR_/XM_ 非编码转录本标注 HIGH，若 canonical 为 ENST 蛋白编码 → 降级为 MODERATE
- **统计格式**："X 基因 / Y 突变" 双维度
- **报告位点格式**：强制包含 `CHROM:POS:REF>ALT`

**提交信息**：`485b851` v0.5.2 - VEP canonical reannotation + transcript discrepancy fix

---

## [v0.4.4] - 2026-05-20

### 重大改进 - Multi-hit 致病性证据过滤

**问题**：原始 multi-hit 规则将同一基因内所有变异都 elevation 到 Tier 1，导致大量 false positive。556 个变异的供者分析中，334 个被标为 Tier 1，绝大多数是正常多态性。

**解决方案**：
- 新增 `_variant_has_pathogenic_evidence()` 函数，定义致病性证据的 3 条标准（或的关系）：
  1. **影响蛋白质功能域** + 目标组织表达（GTEx TPM ≥ 1.0）
  2. **ClinVar 致病性/可能致病性** 或 **IMPACT=HIGH** 或 **gnomAD AF < 0.001**
  3. **剪切位点变化**
- **ClinVar benign 排除**：即使落在功能域内，ClinVar benign 的变异也不视为致病证据
- **精准 elevation**：只 elevation 自身满足致病性条件的变异，不是整个基因的全部变异
- **HLA 排除保留**：继续排除 HLA 基因的天然多态性

**效果**：
| 版本 | Tier 1 | Multi-hit 基因 |
|------|--------|----------------|
| 原始 | 334 | 86 |
| v0.4.3 (HLA 排除) | 238 | 43 |
| **v0.4.4** | **28** | **14** |

### 报告格式改进

- Tier 1 按基因分组，展示详细变异表格：染色体位置、转录本、变异名称、功能域、合子型、ClinVar、原因
- 每个变异增加详细说明：影响程度、后果、功能域位置、组织相关性
- 方法学附录改为中文

### 提交信息
`87cf5c0` v0.4.4 - Multi-hit pathogenic evidence filtering + report format overhaul

---

## [v0.4.3] - 2026-05-20

### 改进 - HLA 基因从 multi-hit elevation 中排除

**问题**：HLA-A/B/C 在 WES 中各有 30-38 个变异，触发 multi-hit 后被全部 elevation 到 Tier 1。但 HLA 是人类基因组多态性最高的区域，这些变异是正常免疫多样性，不代表致病性。

**解决方案**：
- 定义 HLA 基因排除集合（HLA-A/B/C/DRB1/DQA1/DQB1/DPA1/DPB1/E/F/G 等 + MICA/MICB/TAP1/TAP2）
- HLA 基因的多态性变异不再触发 elevation
- HLA 仍在 multi-hit 列表中报告，但 tier 不会被强制降至 1

**效果**：Tier 1 从 334 → 238（减少 96 个 false positive）

### 提交信息
`bcc4e4c` v0.4.3 - Exclude HLA genes from multi-hit elevation

---

## [v0.4.2] - 2026-05-20

### 修复 - GTEx API v2 迁移 + 并发优化

**问题**：GTEx API v1 (`/rest/v1`) 返回空结果，API 覆盖率 0%。

**解决方案**：
- 迁移到 GTEx API v2 (`/api/v2/expression/medianGeneExpression`)
- 支持 versioned gencodeId 解析（两步查找 + 缓存）
- 并发优化：`asyncio.Semaphore(20)` + 30-gene chunks + 0.5s 批间间隔
- 连接池扩容：TCPConnector `limit=50, limit_per_host=20`
- 超时延长：Ensembl 15→30s, UniProt 20→45s
- 单位更新：GTEx 从 RPKM 改为 TPM

**效果**：GTEx 覆盖率从 0% → **304/309 (98.4%)**

### 提交信息
`9a5a0d8` v0.4.2 - GTEx API v2 fix + UniProt batch concurrency optimization

---

## [v0.4.1] - 2026-05-19

### 关键修复

| 修复 | 说明 |
|------|------|
| **UniProt fragment 选择** | `size=1` → `size=5`，选择 reviewed + 最长的 canonical entry，避免选择 60aa 的 fragment |
| **Tissue 默认值移除** | `--tissue` 参数设为 `required=True`，禁止默认 tissue |
| **Cache JSON 解码** | 增加 `.decode('utf-8')` 处理 bytes 类型的 JSON 响应 |
| **硬编码日期** | 替换为 `datetime.now().isoformat()` |
| **UniProt feature 大小写** | 统一 `.upper()` 处理 |

### 提交信息
`39dedbe` v0.4.1 - critical fixes

---

## [v0.4.0] - 2026-05-19

### 首次发布 - API-first 架构

**重大重构**：从离线静态字典迁移到 API-first 架构

- **Phase 1**：替换 `MANE_SELECT` / `PROTEIN_DOMAINS` / `tissue_gene_lists` 为实时 API 查询
- **Ensembl REST API**：基因注释、转录本校正、canonical 转录本选择
- **UniProt REST API**：蛋白质功能域映射
- **GTEx API**：组织特异性表达
- **async 并发**：批量 API 查询 + SQLite 缓存 30 天
- **离线模式**：`--offline` 跳过 API，使用缓存 + 本地回退

### 提交信息
`edc3f75` DGRA v0.4.0 - API-first with offline archive

---

## 版本概览

| 版本 | 日期 | 主题 |
|------|------|------|
| v0.4.4 | 2026-05-20 | Multi-hit 致病性证据过滤 |
| v0.4.3 | 2026-05-20 | HLA 排除 |
| v0.4.2 | 2026-05-20 | GTEx v2 + 并发优化 |
| v0.4.1 | 2026-05-19 | 关键修复 |
| v0.4.0 | 2026-05-19 | API-first 架构 |
