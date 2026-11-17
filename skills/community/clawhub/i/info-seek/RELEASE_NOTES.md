# Infoseek v2.6.1 发布说明

> 发布日期：2026-10-15 ｜ 版本：**2.6.1**（调度台阶段 B 固化 + 阶段 C 评测结论落地；不切 auto 默认，阶梯保留显式 opt-in）｜ 许可证：MIT

---

## 本次更新（v2.6.1）

性能专项四阶段 A→B→C→D，针对 cProfile 定位的全链第一热点——NER `_match_entity` 正则扇出（292146 次 / cum 11.546s）：

- **A 快速收益**：EntityAliases 模块级单例 + NER 结果缓存，消除重复初始化与重复 NER。
- **B 静态预算重构**：normalize/边界正则预编译、实体归一化预算按 id 缓存并以指纹失效。
- **C1 热点正则预编译（不引新库）**：正则对象复用。
- **C2 Aho-Corasick（pyahocorasick，唯一新引入依赖）**：name/static alias/hot/cold 动态别名统一 6 元组负载，一次自动机扫描替代逐实体逐别名正则扇出；未命中实体才补跑动态别名正则。pyahocorasick 缺失或构建失败静默回退原正则路径（`INFOSEEK_AC_DISABLE=1` 可关），结果语义不变。

**性能效果**（perf_baseline_v101，scale 1000 / rounds 3）：
- extract_entities cum 24.963s → 9.873s（约 2.5×）；正则扇出由 29 万次降至近 0。
- 冲突检测 P50 16.9s → 6.1s（约 2.8×）；research(2k lite) P50 57.4s → 25.2s（约 2.3×）。
- NER 不再是第一热点，新热点为 entity_tracker 高频 JSON 落盘（既有机制，本次不动）。

**验证**：新增守护 tests/test_aho_corasick_c2.py（29 断言）；A/B/C 每阶段全量回归 85 PASS / 0 FAIL；冒烟 + 动态别名双验证通过。

---

## 历史版本

### v2.5.0（2026-10-05，意图槽门控堵主题漂移 + L2 渲染恢复实测）

中文长尾实网对拍暴露：360/Kimi/天工召回结果中混入大量同实体**主题漂移页**（旅游攻略/百科/文旅新闻），旧相关性门控的边缘分与 floor/top-k 保底机制将其漏出为「相关结果」。

核心修复（方向 B，pipeline mod-v1.5.0）：
- **意图槽门控**：7 组意图触发词（价格/收购/产量/行情/排名/教程/厂家），主门槛、floor 保底、二级 top-k **三路径统一过槽**。
- **trade 同族归并**：价格/收购/行情同属交易族，簇内任一词回显即过，避免误杀只写「收购」不写「价格」的真相关页；跨族（排名/教程/厂家）仍须各自回显。
- **图谱邻域意图感知**：带意图长尾 query 默认跳过图谱邻居，杜绝邻域引入跨主题扩展；`INFOSEEK_RECALL_GRAPH_INTENT=1` 可恢复。
- **异常安全**：过滤异常返回 `[]`，不裸返全量。

方向 A（L2 渲染恢复，实测负结果、能力保留）：
- 恢复系统 chromium + playwright + stealth，sannysoft 31 项检测全过；但实测 360 数据中心 IP 滑块墙、Kimi/天工需登录且 URL 未承接查询，渲染对当前端点增益=0，能力保留供未来住宅 IP 部署。

**验证**：新增守护 23 断言；实网对拍「信阳板栗最新收购价格」主题漂移漏出 3→0、真相关页全部保留；既有套件零回归。

---

# Infoseek v2.4.1 发布说明

> 发布日期：2026-10-04 ｜ 版本：**2.4.1**（GA12 薄壳漏标修复：品牌官网首页壳判定 + 防误杀三门控）｜ 许可证：MIT

---

## 本次修复（v2.4.1）

中文长尾搜索实测暴露：Kimi 探索版、天工 AI 两个准官方端点在静态抓取时返回**根域名 SPA 官网首页**（通用营销文案、与查询无关），旧判定仅承认标题精确等于「首页/官网」，Kimi 标题只含「官网」、天工不含，均绕过而被当作有效结果召回（薄壳漏标）。

修复要点：
- **判定分层**：captcha/login 静态即拦（浏览器穿不透）；thin_home 延后到渲染尝试之后对最终页补判，不短路 L2 渲染门控。
- **三重防误杀**：查询词回显 / 正文含结果列表结构词，均不判；仅标题命中品牌强壳词（正文可长）或通用官网词（正文须 <600）才判 thin_home。
- 真实三端点对拍：360 `captcha`、Kimi/天工 `thin_home` 全部正确降级并提示人工核验，真实结果页零误杀。

回归：全量 **84 PASS / 0 FAIL**（229s），D-6 文档守护 29/29。

---

## v2.4.0 历史说明

> 前置：v2.3.3。MINOR 定级：主链路新增长尾中文路由能力（默认 ON，仅对判定为长尾中文的 query 生效），影响 `scripts/infoseek_pipeline.py`（mod-v1.2.1→1.3.0）、新增 1 测试套件与 1 验收台账（变动量 >30% 于长尾召回路径，整体 <30%）。

## v2.4.0 核心改动

### ① P1-CN2 CJK query 中文引擎优先路由
- 长尾中文 query（CJK 字数 ≥6）在 `_default_layer` 中把 CN-AI-Web（360AI搜/Kimi探索版/天工AI）**前置**为首位引擎，优先于通用/国际引擎。
- `_engine_weight_for` 对长尾中文给 CN-AI-Web 权重加帽：基础 0.3 → 封顶 1.0（独立于 DYN_WEIGHT 动态权重），融合排序时中文结果居首。
- 保留通用/国际引擎作兜底；`INFOSEEK_CN_PRIORITY=0` 可回退到旧顺序（CN 居末尾、权重 0.3）。

### ② P1-CN3 长尾中文评估基准
- 新增 `tests/test_longtail_cn_benchmark_cn3.py`（46 断言，全离线、不触网），覆盖 A/B/C/D 四层退化：
  A 召回退化（中文前置）、B 融合权重（0.3→1.0 封顶）、C 短中文/英文不误杀、D jieba 屏蔽仍判长尾、D+ CN4 netguard 行为。
- 验收台账 `references/cn3-longtail-benchmark-ledger.md`。真实网络环境受沙箱所限，基准为内部契约级，不代表真实召回质量。

### ③ P1-CN4 部署侧网络边界兜底
- `_search_cn_web` 调用非官方端点前先经 `net_probe.check_hosts` 预判，过滤不可达 host（`INFOSEEK_CN_NETGUARD` 默认 ON）。
- 探测本身异常时**保守保留全部端点**不崩；逐端点 try/except，单点失效不污染主链。

---

# Infoseek v2.3.3 发布说明

> 发布日期：2026-10-01 ｜ 版本：**2.3.3**（矛盾检测事实槽召回增强 + research 全链路性能优化）｜ 许可证：MIT
> 前置：v2.3.2。PATCH 定级：新增主链路能力（默认 OFF 零行为变化）+ 热路径性能改动，影响 core/contradiction_scorer.py、scripts/infoseek_core_v2.py、core/ner.py、references/contradiction-synonyms.json（变动量 10–30%）。

## v2.3.3 核心改动

### ① 矛盾检测长叙述句事实槽召回增强（P2-4）
- **B 层 LLM 结构化槽 hybrid `score_contradiction_hybrid` 正式接线**（此前为孤儿函数）：
  同步路 `score_contradiction` 与异步路 `score_contradiction_async`（经 `asyncio.to_thread`）均接入；
  默认 OFF 返回值 == base（逐字段零漂移），env `INFOSEEK_CONTRADICTION_LLM=1` 开启。
  LLM 出槽走「方面归一化 + 极性/数值/时间/枚举」冲突判定，解决长叙述句键控召回稀疏。
- **方面簇词典 `references/contradiction-synonyms.json` v1.1.0 → v1.2.0**：24 → 36 簇，
  新增 production_output/capacity/user_scale/cost/margin_rate/growth_rate/rank/policy_stance/debt/cash/dividend/time_point 12 簇；
  zh 词条 160 → 267；既有 revenue/profit/market_share 等 6 簇补词。

### ② research 全链路性能优化（P2-6）
- **根因**：NER 在逐源热路径对每个实体名/别名无缓存重复 `re.escape + re.compile`，
  `re._compile` tottime 19.6s 居融合阶段首位，`extract_entities` cum 87.1s（占 research ~60%）。
- **修法**：`core/ner.py _boundary_pattern` 加模块级 Pattern 缓存（编译结果只依赖归一化 keyword，与 text 无关，缓存安全）。
- **实测（3000 源 ×1 轮）**：research **262.5s → 115.4s（-56%，2.27×）**；冲突 124.3s → 48.9s（-61%）；
  `re._compile` 19.6s → 5.3s（-73%）。评分阶段持平（53s）。

### ③ domain_bonus 口径收口复核（P2-5）
- 确认 v2.3.2 已将三链路口径旁路字段 `domain_bonus` 统一并入 `aggregate_score_v2()`（链 A `anchor_score_v2` / 链 B `infoseek_core_v2.score_source`），
  降级保底不平行自算、只标 `_aggregate_degraded`；守护测试 `test_domain_bonus_no_double_count.py` ALL PASS，无双重计分。

### ④ G8-apply 口径销账（P2-2）
- G8 入口契约守护（脚本式测试 `tests/test_entry_contract_g8.py`）实跑 21 PASS / 0 FAIL；
  ROADMAP G8 收口行与 G8-apply 接线行查实，无遗留口径矛盾。

---

# Infoseek v2.3.2 发布说明

> 发布日期：2026-09-30 ｜ 版本：**2.3.2**（S6/S7：浏览器探测收口 + 外部依赖消费点统一迁移到 dep_registry）｜ 许可证：MIT
> 前置：v2.3.1。PATCH 定级：**行为保持型重构**（零逻辑变更、收口前后逐点零漂移对拍），仅将分散探测统一求值，影响 11 文件（变动量 10–30%）。

## v2.3.2 核心改动

### ① S6 浏览器探测收口
- **`scripts/l2_renderer.py`**（mod-v 不变）：chromium / chromium-headless-shell / playwright / camoufox / patchright
  的 `path:` 求值改经 `core/dep_registry.py` 统一接口（`has_module` / `which_path`），组合与降级逻辑仍留本层；
  camoufox 目录非空判定保留。import/path/env/which 四路径逐一对拍 **0 DRIFT**。

### ② S7 消费点分批迁移
- **门控点**：`domain_orchestrator`（Jinja2）/ `anchor_adapter`（summa）/ `infoseek_zerodep_nlp`（summa）/
  `mirror_map`（PyYAML→json 降级）/ `infoseek_auth`（cryptography）/ `mcp_tools_search`（playwright、whisper）/
  `sherlock_client`·`maigret_client`（CLI 路径）/ `summarize_adapter`（jieba 经 bridge、summa）/
  `extensions/qcm/tracing.py`（opentelemetry，深两级 accessor）。
- **接口用法**：可选/降级点 `is_available`（带缓存），必报错点 `require`，
  须感知 sys.modules 注入用 `has_module`（whisper，无缓存），CLI 用 `which_path`。
- **边界裁决**：jieba/pypinyin 保持 `delegate` 委托 `core/jieba_bridge.py` 无双轨；
  required `import yaml` 与 OTLP 子包不迁移，避免过度收口。

### 守护与回归
- 未新增测试套件；D-6 守护联动（compliance_audit.py docstring 随 bump、移出 docstring 版本白名单）。
- **全量回归 81 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT（338s）ALL GREEN**。

---

# Infoseek v2.3.1 发布说明

> 发布日期：2026-09-30 ｜ 版本：**2.3.1**（S5 learned 锚点自动晋级真锚：15 个 accept 词显式开关下接入主链切词锚点层）｜ 许可证：MIT
> 前置：v2.3.0。PATCH 定级：默认 OFF 逐字节回退，仅在显式开关下叠加消费动态锚点，影响范围可控（变动量 10–30%）。

## v2.3.1 核心改动

### ① S5 晋级真锚
- **新增** `core/learned_anchor_store.py`（mod-v1.0.0，S4 已落地）：learned 锚点存储三铁律——默认不启用 / 损坏回退空表 / 单向依赖。
- **新增** `scripts/promote_s5.py`（mod-v1.0.0）：S4 影子对拍人工裁决的 37 候选 → **15 accept 晋级 / 22 reject 不灌库**；每词固化 9 个证据字段（basis_version=v2.3.1）。真实库首次灌库：15 accept / 0 pending。
- **主链接线** `scripts/infoseek_zerodep_nlp.py` bump mod-v1.2.0：新增 `_active_zh_anchors()` 统一访问协议，双路惰性导入（无顶层 import），默认 OFF 返基线 `_ZH_HIGH_FREQ` 逐字节回退；`INFOSEEK_LEARNED_ANCHORS=1` 显式开启后叠加（非替换）accept 词，两个切词消费点统一收口。
- **守护**：新增 `tests/test_learned_anchor_s5.py`（31 断言），演进 `test_learned_anchor_s4.py`（F7 契约，29 断言）；risk-register v1.4.0（R38 晋级词误判污染 / R39 store 损坏）。
- **全量回归**：81 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT（81 标准套件）。

---

# Infoseek v2.3.0 发布说明

> 发布日期：2026-09-29 ｜ 版本：**2.3.0**（中文 NLP 依赖收口：10 处裸 import 单源化 + zerodep 高频词典与共识强化）｜ 许可证：MIT
> 前置：v2.2.0。MINOR 定级：新增 `core/jieba_bridge.py` 底层模块 + zerodep 词典/投票机制增强，影响中文分词与关键词召回链路（变动量 >30%）。

## v2.3.0 核心改动

### ① 中文 NLP 依赖收口（10 处裸 import → 1 个 bridge）
- **新增唯一真源** `core/jieba_bridge.py`（mod-v1.0.0）：统一探测 jieba / jieba.dt / jieba.posseg /
  jieba.analyse / pypinyin，按需 initialize（进程内一次），缺失一次性告警，降级永不抛错；
  sys.modules 双向登记防双模块状态分裂。
- **10 处收敛**：`text_tokenizer.py`（mod-v1.1.0，删三套状态）/ `person_ner.py`（删 pypinyin+jieba.dt 两套状态）/
  `entity_aliases.py`（热路径重复 import 消除）/ `entity_profile.py` / `infoseek_zerodep_nlp.py` /
  `anchor_adapter.py`×2 / `summarize_adapter.py`×2。消费方保持模块对象晚绑定，mock 契约实测生效。

### ② zerodep 零依赖 NLP 增强（mod-v1.1.0）
- **内置小型高频词典**：≈250 中文（AI/金融/医疗/能源/消费五域）+ 40 英文领域词；
  新增「词典匹配估计器 D」，解决 n-gram 对**单频专业词/词表输入**全盲的长尾召回缺口。
- **锚点掩码切分**：命中词掩码断开连续串，根治「智能大模/能大模型」等跨词 n-gram 噪声。
- **共识投票强化**：`weighted_consensus` 阈值自适应（≥3 估计器 2 票 / 2 估计器两侧互证）；
  分层合成——锚点命中即高置信、统计共识补词表外词、单票噪声丢弃、全空兜底收紧；置信 (0,3]。

### 守护与回归
- 新增 `tests/test_jieba_bridge_zerodep_v230.py`（26 断言）；更新 ga5 / ga9（mock bridge 锁定路径）；
  risk-register v1.3.0（R36/R37）；标准套件 77→**78** / 测试文件 78→**79**；D-6 29 PASS。
- 全量回归 **78 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN**。

---

# Infoseek v2.2.0 发布说明

> 发布日期：2026-09-19 ｜ 版本：**2.2.0**（GA11 事件槽批次阶段 1-3：三元事件身份 + 跨文本时间槽键 + LLM 路径收口）｜ 许可证：MIT
> 前置：v2.1.2（F-06 事件抽取 + F-04 期间裁决 + F-07 time 路主体闸）。MINOR 定级：跨文本事件身份从
> 二元 `(subject, aspect)` 升级为三元 `(subject, aspect, time_key)`，跨 2 核心模块 + LLM 全路径字段收口。

## v2.2.0 核心改动

**主题**：把「时间」从对齐后的裁决维度，升级为**事件身份的一等组成**，并根治 LLM 成功路径的字段截断。

- **阶段 1 · 事件身份规范化**：事件 schema 增 `time_key`（`{start,end,label}`，半开 `[start,end)`）；
  单句多时间 span 时事件**扇出**（不再只取 `spans[0]`）；跨文本签名升级三元 `(subject, aspect, time_key)`。
  三类键严格分离（事件身份 ／ 单侧去重 `(subject,aspect,value,polarity,time_label)` ／ 时间关系用真实 span）。
- **阶段 2 · 跨文本时间槽键**：`_event_time_score` 三元对拍，不同 time_key 的同主体同方面事件按真实
  半开区间对拍，任一 overlap → conflict、全 disjoint 按 label 给 60/35；端点相接视为 disjoint；
  透出 `event_disjoint_slots`/`event_overlap_slots`/`event_pairs` 与多期间逐对 `period_pair_details`。
- **阶段 3 · LLM 与调用路径收口**：B 层 LLM 槽表增时间维度（`_llm_slot_span`/`_llm_slot_conflicts`，
  真实 span 可解析且 disjoint → suppression）；**同步 `score_with_llm` 成功分支原窄白名单截断全部事件/期间/
  keyed 字段，改为完整 A 层 `dict(local)` 为底**；同步/异步/hybrid/batch/`infoseek_core_v2`/MCP wrapper
  统一字段透传，纯 A 层默认补 `llm_time_suppressed*=[]`。

**兼容性**：返回体为超集（新增字段，老字段语义不动）；二元 `event_sig` 内部保留，三元对齐为新增事件层逻辑。
B 层 LLM 仍默认关闭（`INFOSEEK_CONTRADICTION_LLM=1` 启用）。默认不推送 GitHub。

**验证**：`test_event_slots_v220.py` 54 断言 + 新增 `test_llm_fields_v220.py` 26 断言（五出口 A 层 31 字段
完整超集契约，防窄白名单回归；固化 R4：router 返 None 不再被伪装成异常降级）；版本单源守护 22 断言；
全量回归 `python tests/run_tests.py` **67 PASS / 0 SKIP / 0 FAIL（231s）ALL GREEN**。

---

# Infoseek v2.1.2 发布说明

> 发布日期：2026-09-19 ｜ 版本：**2.1.2**（GA11 事件槽批次：事件抽取 + 期间裁决 + time 路主体闸）｜ 许可证：MIT
> 前置：v2.1.1（边界审计 P2 四项硬化；同日另有不 bump 的 P3 阶段0 主体贯通 openfix）。

## v2.1.2 核心改动

**主题**：把矛盾检测从「短语级信号」推进到「**结构化事件级对齐**」——GA11 事件槽重构的阶段 1-3。

- **F-06 事件抽取**（`_split_clauses` / `_extract_events`）：标点分句 → 逐事件
  `{subject, aspect, value, polarity, time_span, event_sig}`；数值/方面**句内独立归属**，
  修「全文单次扫描」导致的多事实句串味。事件在**原始正文**上抽取并随 claim 穿透
  （跨越 `text[:500]` / `text[:300]` 两级截断）。
- **F-04 期间裁决**（`_period_adjudicate`）：同主体同方面且双方期间均已知且不相交 → 判为非冲突，
  落地为**降权（×0.5，只降权、不滤除、不归零）**；期间相同/相交/缺失 → 走现值冲突规则；
  空主体不裁决（保持旧契约）。
- **F-07 time 路主体闸**（`time_slot_score`）：签名向后兼容地扩展主体参数与事件参数；
  同主体 → 事件级对齐，跨主体 → 不可对拍，**消除跨主体时间误报**。
- **research 链路字段穿透对齐**：单条冲突补齐 `verdict/time_coverage/keyed_score/conflict_slots/period_adjudication`。

**兼容性**：所有既有公开调用（2 参 `time_slot_score`、不带 `events` 的 `score_contradiction`）
行为不变；返回体为**超集**（新增字段，老字段语义不动）。B 层 LLM 槽维持默认关闭。

**验证**：新增 `tests/test_event_slots_v220.py`（47 断言 / 5 组）；全量回归
**65 PASS / 2 SKIP / 0 FAIL / 0 TIMEOUT**（67 套件，2 SKIP = jieba/pypinyin 可选依赖缺失）。

---

# Infoseek v2.1.1 发布说明

> 发布日期：2026-09-18 ｜ 版本：**2.1.1**（边界审计 P2 四项硬化）｜ 许可证：MIT
> 前置：v2.1.0（OSINT 身份归因 P0 契约修复 + 双源聚合 + 授权 UX；同日另有不 bump 的 P1 openfix）。
> PATCH 定级：4 项均为边界/安全缺陷硬化，无对外工具契约破坏性变更；但横跨 4 模块 + 词表 schema
> 扩展（strict_keywords/false_compounds）+ 新增清洗管线，按 Xes 版本规则（改动幅度 >30%）递增 PATCH 位。

## 本版要点
- **DEF-13** `detect_domain` 入参类型守卫（None/数字不再 AttributeError）。
- **DEF-15** legacy 短语袋路统一 50k 有界窗口，500k 长文本从 >150s 超时降到 <0.2s，三路窗口一致。
- **DEF-14** 报告输出层注入清洗（危险标签/on*=/危险协议，无 SSTI）+ CSV 公式注入防护（正常 markdown/数值零误伤）。
- **DEF-16** 中文 2 字歧义词「回测」误嵌守卫（strict_keywords + false_compounds 区间覆盖判定），yaml/内置双源同步。
- 新增守护 `tests/test_p2_v211.py`（70 断言）；P1 守护 41 断言与全量既有套件零回归。

---

# Infoseek v2.1.0 发布说明

> 发布日期：2026-09-18 ｜ 版本：**2.1.0**（OSINT 身份归因 P0 契约修复 + 双源聚合 + 授权 UX）｜ 许可证：MIT
> 前置：v2.0.0（GA11 键控事实槽 + GA12 网络边界门控）。MINOR 定级：修复 Maigret/Sherlock 客户端真实 CLI 契约（功能性），新增双源聚合引擎与授权 CLI，向后兼容。

## 一句话总结

**让身份归因从"测试通过但真实环境跑不通"变为"契约对齐真实 CLI + 双源交叉验证"**：
沙箱装包实测发现 sherlock 0.16.2 / maigret 0.6.5 的调用参数与输出解析与代码完全不符
（sherlock `--json` 是数据输入、无 JSON 结果；maigret `-J simple` 写报告文件、状态嵌套 dict），
重写两客户端后新增 **Maigret×Sherlock 双源聚合去重引擎**（平台/URL 归一去重、交叉确认置信增强、
高误报平台抑制、CN/IN/全局分区）与**能力授权 consent CLI**。全量回归
**62 PASS / 0 SKIP / 0 FAIL（91.4s）**，默认 OFF / 降级链 / 老契约不变。

## v2.1.0 核心改动

1. **P0 契约修复**：`sherlock_client` 改 `--csv --print-found` 读 CSV（回填 username）；
   `maigret_client` 改 `--top-sites N --no-recursion -J simple` 读报告文件 + 嵌套 status 解析。
2. **双源聚合**（新增 `core/identity_aggregator.py`）：去重 / 双源交叉 +0.10（封顶 0.99）/
   单源高误报平台丢弃、跨源复活 / 单源长尾降档 / CN/IN/global 分区。
3. **pipeline 接线**：`search_identity_attribution` 双源聚合优先，全空回退单源代偿链；
   锚点新增 attribution_sources / cross_source_confirmed / weak_single_source / region。
4. **授权 UX**（新增 `scripts/infoseek_consent_cli.py`）：list / grant / revoke / shell-init / doctor，
   grant/revoke 写 consent.log 审计并输出 export 引导（registry.yaml 保持只读）。
5. **测试加固**：消除三处"依赖本机未装 CLI"的环境脆弱性（注入式 mock，零网络）；
   新增 2 套件（聚合 24 断言、CLI 16 断言），客户端契约守护扩至 20 断言。

## 真实环境待办（本版不闭环）

真实登录源凭证冒烟、真实 OSINT 样本误报阈值校准（误报表为规则框架，Droners 等实测平台先行入表）、
Linux/macOS 安装实证。见 `references/ROADMAP.md` P1。

---

# Infoseek v2.0.0 发布说明

> 发布日期：2026-09-16 ｜ 版本：**2.0.0**（GA11 键控事实槽 C 混合分层 + GA12 网络边界门控）｜ 许可证：MIT
> 前置：v1.9.0（GA9 人名消歧 + GA10 跨语言别名桥接）。MAJOR 定级：GA11 更换矛盾评分的事实槽口径（判定语义变更）。

## 一句话总结

**P3 深水区落地**：GA11 把语义矛盾检测从「短语袋 Jaccard 相似度」重构为「同槽键值冲突」
键控事实槽（keyed slots），段落级口径差异从 **12/12 漏判（none）→ 8/8 真实差异召回、同义复述零误报**；
GA12 建立网络边界探测门控（probe 单源化 + 能力 host 声明 + 执行前门控），让沙箱受限能力
**显式降级留痕而非静默长超时**。两路均守既有设计哲学：默认 OFF / 降级链 / 老契约不变。
全量回归 **59 PASS / 0 FAIL / 0 SKIP / 0 TIMEOUT（90.0s）**。

## v2.0.0 核心改动

### GA11 · 键控事实槽（C 混合分层）

1. **数据真源** `references/contradiction-synonyms.json`：20 个方面谓词簇（中英）+ 8 方面互斥对
   + 否定词 + 主体停用词。
2. **A 层（默认零依赖）** `core/contradiction_scorer.py`：槽键=(主体键, 方面)，值=数值/枚举/极性；
   仅同键值冲突计分。主体契约驱动（entity/subject，不同主体不比）；数值全文单次扫描+左优先
   就近唯一归属（指标后侧窄窗、趋势词仅收百分比、年份专归 founded_year、季度/裸年份排除、
   「百分之二十」中文归一）；同值对跨槽去重；keyed 与否定路 **max 融合不叠加**。
   裁决：单冲突 35（medium）/2 槽 60/≥3 槽 85；长文本保护 50k/500/200 上限。
3. **B 层（opt-in）** `score_contradiction_hybrid()`（`INFOSEEK_CONTRADICTION_LLM=1`）：
   LLM JSON 槽表复用键控比对，表外方面动态键，温度 0 + 缓存，降级链 B→A→legacy。
4. **契约**：新增 `keyed_score`/`conflict_slots`/`scorer_mode`，老字段语义不变。
5. **质量**：12 组段落语料 8 真实差异全召回（4 强 ≥medium + 4 细微 low+），4 同义复述零误报；
   L1-01..06 逐条零回归；100 字 vs 300 字同判不稀释。守护测试 38 断言。

### GA12 · 网络边界门控（五步链，默认 OFF 零行为变更）

1. `scripts/net_probe.py` 探测唯一真源（TTL 进程内+磁盘缓存、幂等、并发、fail-safe）；
   engine_router/search_engine_health 重复 probe_http 收口为委托。
2. registry.yaml：12 能力补 requires_hosts + network_boundary；新增 WikiVerify/L4Transcribe/
   PatentLookup 三能力；network_boundaries 11-host 台账；core 访问器 + 内嵌默认同步。
3. `scripts/boundary_gate.py`：静态声明校验/实测可达/执行前 preflight（默认 OFF、fail-open）。
4. `references/network-boundary-report.md`：沙箱受限清单（目标机可重刷对照）。
5. `capability_compensator` 边界预检：不可达沿 degrade_to 显式降级 + boundary_restricted 留痕。

## 兼容性

- 矛盾评分老字段与 score→severity 主映射保留；GA11 仅新增字段，短句/极性对立判定零回归。
- GA12 门控默认关闭，未设置 `INFOSEEK_BOUNDARY_GATE=1` 时对现有抓取/代偿路径零影响。
- 无新增硬依赖（GA11-B 为 opt-in，复用既有 llm_router）。

## 验证

- 新增守护：`tests/test_ga11_slots_v200.py`（38）+ `tests/test_ga12_boundary_v200.py`（36）。
- 全量回归：59 套件 59 PASS / 0 FAIL / 0 SKIP / 0 TIMEOUT（90.0s）。

---

# Infoseek v1.9.0 发布说明

> 发布日期：2026-09-14 ｜ 版本：1.9.0（GA9 人名消歧五步 + GA10 跨语言别名桥接）｜ 许可证：MIT
> 前置：v1.8.4（GA5 分词单源化）→ v1.8.3（§8.4 三链路口径一致性）→ v1.8.2（遗留 4 缺口闭合）

## 一句话总结

**P2 人物调研补强落地**：闭合 ROADMAP §8.12.2 **GA9**（人名消歧五步：多音字姓氏白名单 →
复姓整词长匹配 → heteronym 全读音枚举 → person 实体族动态注册 → 拼音别名接 `_expand_query`）
与 **GA10**（跨语言别名桥接，修复 D1 英文源系统性低估）。实测 D1 实锤场景
`ualberta.ca` 官方一手源由 **9 分 ❌噪声 → 55 分 🟡潜力**；D2 场景英文源经拉丁拼音别名
命中中文人名实体（`Linjian Xiang` → 项林坚），人物调研融合链不再空转。

## v1.9.0 核心改动

1. **GA9① 数据真源** `references/person-surnames.json`：单姓 245 / 复姓 68（含 4 字复姓）/
   多音字姓氏 26（preferred + heteronym）/ 误报防护词 662 + 地名 47 + 地名后缀 56 + 虚词 143。
2. **GA9②③ 检测与别名** `core/person_ner.py`：复姓整词长匹配（禁逐字拆）；text/subject 双层模式
   （精度/召回分层）；姓氏多音字全枚举 + 名连写英文化（`xiang linjian` / `linjian xiang`）；
   五重守卫（虚词 / 常用词 jieba-FREQ / 地名后缀 / blocklist / 叠字）。
3. **GA9④ D2 闭合**：`bootstrap_subject()` 把人名注册进 person 实体族（运行时会话级），
   NER 对中文源按 `name` 命中、对英文源按注册别名（拉丁拼写）命中；冲突检测/图谱可按人名索引。
4. **GA9⑤ + GA10 桥接** `core/xling_bridge.py`：subject 的人名拼音别名组 + 词典实体拉丁别名组
   构成跨语言桥接；`score_source` fallback 与 `_filter_relevant` 双闸门命中即保底 55（多组至 70）；
   区分度守卫（常见英文词 blocklist）防误抬；env `INFOSEEK_XLING_BRIDGE` 可关。
5. **召回扩展**：`_expand_query` 追加拼音别名（与词典别名去重），提升英文源召回面。
6. **守护测试**：`test_ga9_person_v190`（40 断言）+ `test_ga10_xling_v190`（29 断言），
   含导入纪律 AST 守护（固化「禁 from-import」永久约束）。

## 零回归契约

| 项 | 保证 |
|----|------|
| 既有命中路径 | 桥接为 `max()` 抬底语义——原 Jaccard/containment 命中不受影响 |
| 中文×中文 | `xling_bridge=0`，env on/off 分数**恒等**（B3 断言） |
| algo-v 契约 | `score_source` 返回体 `version` 保持 **1.2.0**；仅新增 `xling_bridge` 字段 |
| RE1/RE2/RE3 | `_expand_query` 既有契约全保（BYD 扩展 / 无命中原样 / 异常防御） |
| 导入纪律 | `_anchor_mod`/`_person_mod`/`_xling_mod` 模块对象晚绑定，禁 from-import（AST 守护） |

## 升级注意

- **新增可选依赖** `pypinyin>=0.55`：未安装时检测/注册仍工作，拼音别名降级为空 +
  一次性告警（不阻断主链路）。
- env 开关：`INFOSEEK_XLING_BRIDGE`（默认开）/ `INFOSEEK_PERSON_NER`（默认开）；
  关闭后完全回退 v1.8.4 行为。
- 人名注册默认**会话级内存态**（零文件写入，无跨会话噪声累积）；需持久化可显式
  `register_person_runtime(..., persist=True)` 走 `learn_entity` 通道。

## 剩余路线

- **P3 / v2.x**：GA11 段落级事实槽重构（`contradiction_scorer` 长叙述句召回近零）、
  GA12 目标机闭环（沙箱网络边界受限项）。

---

# Infoseek v1.8.4 发布说明

> 发布日期：2026-09-13 ｜ 版本：1.8.4（GA5 分词单源化 + 局部 import 收口）｜ 许可证：MIT
> 前置：v1.8.3（§8.4 三链路口径一致性闭合）→ v1.8.2（遗留 4 缺口闭合）→ v1.8.1（版本号单源化治理）

## 一句话总结

**P1 治理收口**：闭合 ROADMAP §8.12.2 最后一个 P1 余项 **GA5「分词单源化」**——把
`anchor_adapter._tokenize_subject` 与 `infoseek_pipeline._tokenize_query` 两份并存的同构分词
实现抽为唯一真源 `scripts/text_tokenizer.py::tokenize_text()`，两侧退化为薄封装委托；连带收口
§8.12.4 点名的 `infoseek_pipeline.py:996-999`（函数体内 `sys.path.insert` + 局部 import）。
18 样本旧↔新**零差异**对拍，全量回归 **55 PASS / 0 FAIL（90.1s）**。

## v1.8.4 核心改动

1. **唯一分词真源**：新增 `text_tokenizer.tokenize_text(text, require_chinese=False,
   warn_on_fallback=False)`——jieba 优先（探测进程内缓存，避免热路径重复 try-import）→ 缺失
   回退纯 Python（中文连续段 ≤4 字整段 / >4 字滑窗 2-gram；英数 ≥2 字符整词；小写归一）。
   零 infoseek 内部依赖 → 天然无循环依赖，原「独立实现避免循环依赖」的理由消解。
2. **两侧退化委托**：`_tokenize_subject` 33 行 / `_tokenize_query` 32 行算法体各收敛为一句
   `return tokenize_text(...)`；保留函数名（兼容 `_string_containment_similarity` 调用点与
   `test_relevance_gate_v177` 断言）；`_RELEVANCE_WARNED` 移除（一次性告警迁真源）。
3. **有意差异显式参数化**：`require_chinese=True`（query 侧）——纯英文/数字 → 空集，服务
   `_filter_relevant`「中文多字词硬门槛」；subject 侧无门控（处理任意语言）。这是**唯一**
   保留差异，已由 G9/G10 断言锁定「含中文样本分叉恒为 0」。
4. **局部 import 收口**：删原 996-999 每次调用的 `sys.path.insert` + 局部 import → 顶层
   `import anchor_adapter as _anchor_mod` + 属性访问；300 次调用实测 `sys.path` **Δ=0**
   （原 +300，与 GA8 已治的 O(n²) 隐患同源）。
5. **新增守护测试**：`tests/test_ga5_tokenizer_v184.py`（170 行 / **24 断言**，6 组），含
   **G23/G24 mock 可patch性**——把本轮踩到的隐性契约固化为断言。

## 本轮最大教训：from-import 早绑定击穿 mock 契约

首次收口用顶层 `from anchor_adapter import compute_semantic_similarity,
_string_containment_similarity`，全量回归**击穿 3 套件 9 项断言**
（`test_p1p3p2_fixes` 12/15、`test_recall_enhance_v101` 13/16、`test_relevance_gate_v177` 9/12，
含 C2 `calls=0`）。

- **根因**：from-import 在导入期把函数对象**固化**进 pipeline 命名空间（早绑定）；测试替换的是
  `anchor_adapter` 的**模块属性**，晚替换无效。原「函数体内局部 import」虽是性能反模式，却每次
  重新取属性（晚绑定）——这是既有测试依赖的隐性契约，不只是路径注入。
- **修法**：模块对象 + 属性访问（调用时求值）→ patch 恢复生效，同时 `sys.path` 不膨胀。
- **铁律**：收口局部 import 时，若被导入对象存在 mock/monkey-patch 契约，必须用模块对象属性
  访问；**全量回归是唯一判据**（单套件自测发现不了）。

## 验收

| 项 | 结果 |
|----|------|
| 行为等价 | 备份 exec 旧实现，18 样本旧↔新**零差异**（含中/英/混排/空/单字/全角/标点） |
| 分叉口径 | 旧 3 == 新 3，全为纯英文/数字样本（有意门控 A）；含中文分叉 **0** |
| sys.path | 300 次调用 **Δ=0**（原 +300） |
| AST 收口 | `_filter_relevant` 体内 Import/ImportFrom/path.insert 节点 **0 命中** |
| 守护测试 | `test_ga5_tokenizer_v184` **24 PASS / 0 FAIL** |
| 全量回归 | **55 PASS / 0 FAIL / 0 SKIP / 0 TIMEOUT / 0 KNOWN，90.1s** |
| 版本联动 | SKILL.md / mcp_tools_common.SKILL_VERSION / core.__version__ / manifest.yaml 四处 1.8.4 |

## 升级注意

- **行为零变更**：本版为等价重构，评分/门控/召回口径均不变，无需调整任何调用方或 env。
- 若你在外部代码里 patch 过 `anchor_adapter` 的相似度函数，**继续可用**（G23/G24 已守护）；
  但请勿把 pipeline 顶层的 `import anchor_adapter as _anchor_mod` 改回 from-import。
- jieba 仍为可选依赖：未安装时自动回退纯 Python 并发一次性 WARNING（精度下降，建议安装）。

## 剩余路线

- **P2 / v1.9.0**：GA9 人名消歧五步（多音字白名单 → 整词长匹配 → heteronym 枚举 → person
  实体族 → 拼音别名接 `_expand_query`）、GA10 跨语言别名桥接（英文一手源被中文 query 系统性低估）。
  **P1 5/5 全闭合 → P2 启动条件已满足**。
- **P3 / v2.x**：GA11 段落级事实槽重构、GA12 目标机闭环（沙箱网络边界受限）。
