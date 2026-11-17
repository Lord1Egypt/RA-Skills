# Infoseek 路线图（当前基线 · 待办 · 前景方向）

> 版本：v2.6.1 ｜ 更新：2026-10-15
>
> 本文件只保留**面向当前**的内容：已达成基线、真实未完成待办、前景方向、验收总闸。
> 各历史版本的详细实施记录 / 缺口审计 / 设计裁决已归档至
> **`ROADMAP_archive_20260917.md`**（v1.0.0 → v2.0.0 全量脉络，1088 行）。需要追溯
> 「某 GA 在哪个版本、为何这么设计、踩过什么坑」时查归档，不在本文件堆积。

---

## 一、当前基线（v2.6.1）

| 维度 | 状态 |
| --- | --- |
| 对外版本 | SKILL_VERSION **2.6.1**（唯一真源 `scripts/mcp_tools_common.py`）；调度台阶段 B 状态机固化 + 阶段 C 评测结论落地（不切 auto 默认，阶梯保留显式 opt-in）；前序 NER 性能优化四阶段 A/B/C：A 单例+NER 缓存、B 静态预算重构（normalize/边界正则预编译 + 实体预算缓存）、C1 热点正则预编译（不引新库）、C2 引入 pyahocorasick 把 name/static/hot/cold 别名正则扇出改为一次自动机扫描（缺失/构建失败静默回退，`INFOSEEK_AC_DISABLE=1` 可关）；research P50 57.4s→25.2s（约 2.3×），NER 不再是第一热点 |
| 全量回归 | **88 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT**（88 套件，2026-10-13；调度台阶段B（`scripts/infoseek_pipeline.py` mod-v1.5.2，PATCH 状态机默认仍等价旧行为）：`_expand_query` 拆出 `_expand_query_variants` 返回 (expanded, extra_list)（模块对象导入契约不变）、新增 `_staged_fanout` Stage0/1/2 阶梯（门控后有效判停/调用预算/<1.2s 不晋升）、`_effective_count` 轻量门控谓词、`_channel_is_high_quality` auto 通道判定（仅 sim/纯内置→保守旧全扇出）；`workbuddy_channel.is_simulated()` + meta capability=simulated、`platform_adapter.platform_engine_simulated()` 三态（守护⑥互斥）；新增 `tests/test_dispatch_stage_b.py`（11 用例覆盖守护①②⑤⑥）；前序阶段A mod-v1.5.1 CN_SUBQ 四态+预算脚手架 `test_dispatch_stage_a.py`；前序 2026-10-06 NER Aho-Corasick 基线 86 PASS、research P50 57.4s→25.2s 约 2.3×） |
| openfix 批次（2026-09-18，版本号不变） | P0-OPEN-04 score 量纲归一化+禁空骨架 / P0-OPEN-06 时间事实槽+无冲突·未评估区分 / P0-OPEN-05 GPT-5 路由+模板按域收窄+跨源综合段 / P1 README 对齐 19 工具+run_tests SKIP 判定修复；守护 `test_open_fixes_v210.py`（60 断言） |
| openfix 批次（2026-10-15，版本号不变） | A4 版本联动遗漏修复（2.6.1 发布时 compliance_audit.py 头部 mod-v 仍为 2.6.0、D-6 DIVERGENCE_WHITELIST 未同步）：compliance_audit.py 头部 `mod-v2.6.0`→`2.6.1` + D-6 白名单 `compliance_audit.py: {"2.6.0"}`→`{"2.6.1"}`；守护 test_compliance_audit_v220.py A4（30 断言）/ test_doc_state_sync_d6.py C2（29 断言）；全量复跑 88 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT（335s）ALL GREEN |
| 版本体系 | 四维分离：SKILL_VERSION（对外）/ mod-v（模块内部）/ algo-v（下游契约）/ proto-v（MCP） |
| OSINT 客户端 | sherlock v0.16.x（`--csv` 读结果）/ maigret 0.6.x（`-J simple` 报告文件 + 嵌套 status）契约对齐实测 |
| 身份归因 | Maigret×Sherlock **双源聚合去重**（`core/identity_aggregator.py`：交叉确认 +0.10/误报抑制/分区）+ AccountTrustScorer 验证 |
| 授权 UX | `scripts/infoseek_consent_cli.py`（list/grant/revoke/shell-init/doctor + consent.log 审计） |
| 评分口径 | 唯一聚合真源 `aggregate_score_v2()`（base 四维 + 独立加权层），三链路口径一致 |
| 分词真源 | `scripts/text_tokenizer.py` 单源（jieba 可选，缺失纯 Python 回退） |
| 人物调研 | GA9 人名消歧五步（`core/person_ner.py` + person-surnames.json）/ GA10 跨语言别名桥接（`core/xling_bridge.py`，pypinyin 可选） |
| 冲突检测 | GA11 键控事实槽（`core/contradiction_scorer.py`：keyed A 层 + LLM opt-in B 层，替代旧短语袋 Jaccard）+ P0-OPEN-06 **时间事实槽**（年月/季度→ISO 区间，第三路 max 融合）+ **v2.2.0 三元事件身份 `(subject,aspect,time_key)`**（多 span 扇出 + 半开区间事件对拍 + 多期间逐对明细 + LLM 全路径字段收口）+ verdict 三态（conflict/no_conflict/not_assessable）+ 覆盖率 |
| 报告模板 | `domains/templates.yaml` v3.2.0：5 域 + default，高分源（≥70）跨源综合段、空源守卫、filter_block 注入；tech 已按域收窄为通用技术（制造 + AI/软件） |
| 评分健壮性 | P0-OPEN-04 入口 0–1 量纲自动 ×100（`scale_normalized`）；核心源为 0 禁止空骨架（`filtered_out` 清单及原因） |
| 网络边界 | GA12 五步链（net_probe 单源 + registry host 台账 + boundary_gate 默认 OFF/fail-open + compensator 预检） |
| 实体持久层 | 双层落盘：`entities_learned.json`（动态回流 + 冷清理 prune）/ `entities_state.json`（hit/last_seen/90 天半衰期衰减）；FreshnessCron 七步闭环 |
| 身份取证 | FakeDetect 账号取证扩展（L1 统计 / L2 图结构 / 时序同步 / L3 ML，consent 闸控） |
| QCM 协同 | 双向桥接（Infoseek qcm_query ←→ QCM 归因），OAuth / GraphQL / OTel / 多进程 |
| 平台发布 | GitHub（GYINT/infoseek）+ npm + ClawHub + DSH 插件包；ima 注册幂等 |

---

## 二、待办（仅列**代码级核实仍开放**的项）

> 2026-09-18（v2.1.0）代码级审计：沙箱装包实测发现并修复了 Maigret/Sherlock
> 客户端 CLI 契约全错的 P0（旧实现真实环境必然落空），并交付双源聚合 + 授权 CLI，
> 销去原 P1#2/#3 的**代码侧**。下列项均**必须在真实环境闭环**，沙箱网络受限无法替代。

### P1 — 近期（低风险 / 需真实环境，测试无法替代）

1. **L3 登录源真实凭证端到端冒烟**——现有覆盖均为 mock 凭证；需在有真实 key 的
   目标机对至少一个登录源做一次真实抓取冒烟（沙箱网络受限，无法在此闭环）。
2. **OSINT 真实样本误报基线校准**——双源聚合引擎与高误报平台表（实测 Droners 对必不
   存在用户名误报 Claimed，已入内置表）已就位，但 CN/IN/全局误报率阈值、平台别名表、
   长尾 rank 阈值仍是**规则框架默认值**；需在隔离 venv 用 sherlock-project / maigret
   对真实样本标定（含 sherlock/maigret 结果融合的精度/召回）。
3. **跨平台安装实证**——`install.sh` 已在 Windows-Git-Bash 校验；Linux/macOS 需目标机
   联网装依赖后各跑一次 `bash install.sh --venv`。
4. **调度台阶段 D（auto 默认 + bump v2.7.0）待真实快通道补测**——阶段 B 状态机（`scripts/infoseek_pipeline.py` mod-v1.5.2，Stage0/1/2 阶梯）与阶段 C 评测（real/sim/synth 三类对拍）已完成，结论：召回 0 劣化、引擎调用 −34%、P95 −0.06s，但沙箱慢源下平均延迟仅 −0.15s（非显著，Stage1/2 晋升 24 组全未触发，8s 窗口主导）。**裁决（2026-10-15 选项①）：阶梯保留显式 opt-in（`CN_SUBQ=stage`），auto 不切默认；v2.6.1 固化阶段 B 代码 + 评测报告**。**选项③ FAST 模拟通道补充对拍（2026-10-15）已闭合盲区**：沙箱注入亚秒级（~80ms）FAST 引擎模拟真实快通道，双轮对拍 auto vs always —— ①理想形态（Stage0 满足）：延迟 0.16→0.08s（P95 −0.39s，−50%）、调用 −37%、召回 100% 达标不劣化、零晋升（满足标尺 D「延迟降+召回不劣化」严格门槛）；②降级补偿（整句弱/拆词强）：晋升 11/12 真实触发、召回接近不劣化、调用 +11%、延迟 +0.02s 可控（不误停）。**阶段 D 决策影响**：一旦生产具备真实快通道（每源亚秒），阶梯延迟优势成立且显著；FAST 为沙箱模拟非生产真实源，当前沙箱可用真实源仍偏慢。**建议**：生产侧若有快通道（如 WorkBuddy 渲染/直连高速源）→ 据选项③证据推进选项②（切 auto 默认 + bump v2.7.0）；若生产仍以慢源为主 → 维持选项①（阶梯 opt-in），待真生产快通道复现一次即切。回退开关 `CN_SUBQ=always` 保留。评测报告 `/sandbox/workspace/stage_c_ab/STAGE_C_REPORT.md` §7。

### P2 — 中期（核心收益）

4. ~~**矛盾检测叙述句事实槽召回增强**~~ ✅ **已收口（2026-10-01/10-02，P2-4）**——GA11 键控槽对结构化数值冲突强，对长叙述句
   （无明确指标词 / 隐式比较）召回仍偏弱；扩充方面簇词典 + B 层 LLM 槽的默认策略评估。
   → 方面簇词典 v1.2.0 / 36 簇 / zh 267 词，term-value 事实槽接线，经 `core/conflict_v3.py:173`
   唯一生产调用点间接接入（同步/异步/MCP 三入口），默认 OFF；详见后文 P2-4 与销账勘误。
5. ~~**三链路口径旁路字段收口**~~ ✅ **已收口（2026-10-01，P2-5）**——链 B（MCP 活跃链路）`domain_bonus` 原是旁路字段
   （仅报告不计入 final），待统一并入 `aggregate_score_v2()` 的环节化计算。
   → 已并入 `aggregate_score_v2()` 计入 final（评分契约 v2 L98 已对齐），防双重计分约束保留；详见后文 P2-5。
6. ~~**research 全链路性能**~~ ✅ **代码级已收口（P2-6）；真机复拍转 P1-4**——3000 源实测 research（2k 子集 lite）P50 ≈ 83.6s、
   冲突检测 P50 ≈ 39.3s（见 `dist/perf_baseline_v101.json`）；多轮统计已建立，
   下一步定位 research 融合阶段热点。
   → perf_baseline 增 `--profile`/`--rounds`，产物 perf_profile_v101.json；沙箱侧热点定位完成。
   唯一未竟——真机 3000 源端到端 profile 无法沙箱复拍，已登记 P1-4 随真机环境暂缓。

### P3 — 远期（v2.x 立项，保持零依赖 + 降级路径哲学）

7. **多模态理解**——图片 / 视频 / 音频内容理解与检索（独立大模块；当前 L4 whisper 仅音频转录）。
8. **编排 / 多 agent 协同**——与搜索 / 验证 / 归档工具深度整合，作为可观测子任务被组合。
9. ~~**合规审计增强**~~ ✅ **已落地（2026-09-21，D-8/P3-9）**——抓取合规 / 版权 / 凭证审计自动化报告（`scripts/compliance_audit.py` + 守护 `tests/test_compliance_audit_v220.py` 30 断言 + `references/compliance-audit-report.{md,json}`）。
10. **本地文件集成**——按用户反馈触发（不预设）。

### 明确不做（设计边界）

实时新闻监控 / 学术文献综述 / 浏览器自动化爬取 / 即时聊天对话——交由更专业的专用工具。

### 二·补、2026-09-20 六类分层待办盘点（规划任务清单）

> 起点：v2.2.0（GA11 事件槽批次）**发布收尾暂停**，转入优先级重排后再定发布。本清单交叉核验
> 本路线图 / `ROADMAP_archive_20260917.md` / `CHANGELOG.md` / `RELEASE_NOTES.md` / 风险与边界文档 /
> 代码接线 / 测试现状；**历史快照与归档中的开放描述不计为当前开放缺陷**。
> 唯一对外版本真源 `scripts/mcp_tools_common.py`（当时 `SKILL_VERSION="2.2.0"`；本节为 2026-09-20 历史快照，当前真源已为 2.6.0）。

**分层**：① 阻塞层 P1（沙箱不可替代）→ ② 收敛层 P2+D（沙箱可执行）→ ③ 清理层 B+C（文档/语义）→ ④ 远期层 P3。

> **状态更新（2026-09-20 21:03，已确认）**：当前环境**不支持真实环境与跨平台**验证——**P1-1 / P1-3 暂缓挂起**；P1-2 可在沙箱预置阈值/别名框架，真机样本标定仍需目标机。**可执行最高优先级切换至收敛层 P2 + D**，其次清理层 B + C；P3 维持归档。下列 P2/B/C/D 条目均已工具取证确认仍开放。
> **Phase-R1 执行记录（2026-09-20 21:44，已落地并全量回归 69 PASS / 0 FAIL·232s ALL GREEN）**：R1-a（D-1）cron 第7步传真实 `active_names` + stats 透出 `applied`，新增 `test_learned_prune_cron_r1a.py`；R1-b（P2-5/D-2）`domain_bonus` 收敛锁定，新增 `test_domain_bonus_no_double_count.py`（链B 传 0 为刻意设计防双重计分）；R1-c（D-5/B-1~B-4）删 `infoseek_mcp_server.py` 死分支、CHANGELOG→67 PASS/231s、risk-register L35 更正、freshness_cron 头注释 v2.2.0+7 步枚举、mcp_tools_forensics docstring→v2.2.0。版本号维持 **2.2.0**（清理/守护类，变动量<10%）。
> **Phase-R2 执行记录（2026-09-20 22:08，层 C 历史归档误命中销账，全量回归 69 PASS / 0 FAIL·230s ALL GREEN）**：C-1 `CHANGELOG.md` L235「边界审计遗留（已立案…）」段标题下加**事后闭合注**（DEF-13~16 系 v2.1.0 立案快照、v2.1.1 全修，守护 test_p2_v211.py 四组 70 断言；历史正文与「Open 口径（保持现状）」三条刻意保留、一字不改）；C-2 死路径 `roadmap_ch812.md` 经 glob 证实**文件已不存在**，仅在 ROADMAP 行内注明（A5 命中皆 GA5 分词单源化已闭合 / GA9 测试分组见归档 L933），不触碰冻结归档；C-3 复核 `ROADMAP_archive_20260917.md` L3-9 冻结快照声明成立，只查不改。连带如实化（同表已完成项，均工具复核）：B-1/B-2/B-3/B-5、D-1/D-2/D-5、P2-5 勾 ✅；L17 基线 67→**69 PASS**/231s→**232s 口径**（本次回归实测 230s）、L3 更新日→2026-09-20。零代码逻辑改动、零新增测试，版本号维持 **2.2.0**（变动量<10%）。
> **Phase-R2b 执行记录（2026-09-20 22:46，P2 收敛层销账，全量回归 72 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：P2-4/D-4 矛盾检测 term-value 事实槽闭环（aspects 24 簇 / opposites 9 组 / NUMERIC_ASPECTS 12 类 / 守护 22 断言，含 3 项 known_boundary 记延伸项）；P2-6/D-3 性能 profiling 闭环（`--profile` 热点 + `--rounds` 多轮 P50/P95 + `dist/perf_profile_v101.json`，守护 23 断言）；D-6 文档状态同步守护首建（25 断言）并修复 ROADMAP 尾部 2 个非 UTF-8 字节（L239/L240 重复行残迹去重，属错字级修复）；D-7 证据归档模板 + 验收台账立项交付。零代码逻辑破坏、零公开签名改动，版本号维持 **2.2.0**（守护/文档/采样类，变动量<10%）。
> **Phase-R3 执行记录（2026-09-21，P3 层推进：D-8/P3-9 合规审计自动化 + A5–A7 编号映射收口）**：**D-8/P3-9 落地**——新增 `scripts/compliance_audit.py`（凭证审计 / 抓取合规 / 网络边界 / 版权来源四维 → Markdown+JSON 双产物，全文零明文；`_iter_files` 跳过自产物 + `_redact` 命中不回显，自指污染根治，幂等复证）+ 守护 `tests/test_compliance_audit_v220.py`（**30 断言**，连续 4 次 exit=0）+ 产物 `references/compliance-audit-report.{md,json}`；**A5–A7 复核收口**——全仓命中皆 `GA5/GA6/GA7` 前缀子串，判为「编号来源不可考·命名缺失（非代码缺口）」，非开放缺陷。连带文档销账：L17 基线 72→**73 套件**、D 表 D-8/D-审、P3 表拆分（P3-9 已落地）、前景方向移出「长期」、B-5 复核、`tests/run_tests.py` docstring 套件数如实化。**连带修复（测试环境隔离）**——回归发现 `tests/test_identity_clients_v100.py` C1「能力默认 OFF」断言失效，根因定位为 **env 旁路**（`core/capability_registry.is_enabled` 中 `_env_override` 优先于 registry 声明 `enabled:false`，而沙箱进程遗留 `INFOSEEK_ENABLE_MAIGRET/SHERLOCK/ACCOUNTTRUSTSCORER=1` → 默认 OFF 早退闸口被绕过 → 落到 `_consent_gate` 抛 `ConsentRequired`）；修复 = 测试头部显式 pop 该三项 per-capability env，锁定「纯注册表默认态」，并沉淀为 **㉖铁律**：凡测试依赖「能力默认 OFF」语义，必须显式隔离 `INFOSEEK_ENABLE_*`，禁止依赖环境偶然性（单跑复现 20 PASS / 0 FAIL，幂等复证）。零代码逻辑破坏、零公开签名改动，版本号维持 **2.2.0**（新增模块/文档类，变动量<10%）。
> **Phase-BH 执行记录（2026-09-21，模块边界能力硬化 G1–G6 · 全量回归 74 PASS / 2 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN，76 套件）**：源自《infoseek_status_boundary_audit_20260921.md》111 项边界注入探测的 8 项缺口。**P1 三项闭环**——**G1** `core/capability_registry.py` 顶部加载期单例别名（`sys.modules` 双向登记）根治「顶层名 ↔ `core.` 包路径」双导入状态分裂（`_cache`/`_consent_state` 合一，consent 授权跨消费方可见）+ `scripts/capability_compensator.py` 导入双路加固；**G2** `core/conflict_v3.py::_extract_fact_claims` 增 `_as_text` 空值/类型守卫（`title=None` 不再 `.strip()` 崩溃、单坏源不 abort 全链）；**G3** `capabilities/registry.yaml` + 内嵌 `QVeris.degrade_to` 补 `manual_review` 并声明 `Exa`/`Tavily` 搜索替代层占位（消除悬空引用，`degrade_chain('QVeris')=[QVeris,Exa,Tavily,manual_review]` 末端闭合）+ host 台账补 `qveris.ai`/`qveris.cn`。**同类低危一并根治**——**G4** `core/anchor_score_v2.py::aggregate_score_v2` 入口有限性守卫（NaN/None/±inf/非数字→0 + `score_invalid` 留痕）；**G5** 同函数 `max(...,0)` 下界夹取；**G6** `compensate` 末端 `graceful_fallback` 无 handler 时内置默认（缺口必被显式标记，不再静默丢 `gap_flag`）。守护并入既有套件（`test_capability_registry_v100` R5 组 / `test_three_chain_v183` T10 组 / `test_boundary_v240` L2-13 / `test_ga12_boundary_v200` 能力数 12→14 同步），未新增套件（零 D-6 冲击）。**转入下批登记**：**G7** 文档/基线口径治理（`SKILL.md §10` 套件数 26→实测、`dist/quality_baseline.json` 悬空引用、`ROADMAP L17`/L165/L234 口径一致化，须与 D-6 守护联动）；**G8** 公共入口 None/类型契约统一（12 处类型违规 11 处 CRASH，架构级、需专项设计）。零公开签名破坏、零新增依赖，对外版本维持 **v2.2.0**（openfix 边界硬化，变动量<10%）。

#### G — 边界硬化续（Phase-BH 转入 G7/G8）

| 编号 | 任务 | 路径 | 处置 |
| --- | --- | --- | --- |
| G7 | 文档/基线口径治理：`SKILL.md §10` 套件数（25→实测）、MCP 工具数（17 / 19→18）三处一致、`README` 测试套件数（62→实测）、`dist/quality_baseline.json` 悬空引用收敛、`core/` 模块数（22→29）、`run_tests.py` docstring（73→实测） | `SKILL.md` · `README.md` · `references/risk-register.md` · `references/Infoseek_MCP集成契约_v1.5.md` · `tests/run_tests.py` | ✅ 已收口（Phase-G7 · 2026-09-21）：全部以代码/实测为真源复核修正；D-6 增 ⑤ 组 E1-E4（套件数·文件数口径 + `dist/*.json` 引用存在性），25→29 断言；零代码逻辑改动 |
| G8 | 公共入口 None/类型契约统一（12 处类型违规 11 处 CRASH，架构级） | `references/g8-entry-contract-design.md` · `tests/test_entry_contract_g8.py` | ✅ 已收口（Phase-G8 设计 2026-09-21 → **G8-apply 接线 2026-09-22，见下 L103**）：探测复现 12 OK / 11 CRASH；推荐方案 C（`scripts/entry_guard.py` 守卫原语 + 渐进接线）；11 处公共入口接线受控、零公开签名改动；守护升级 21 断言，边界注入 CRASH==0（9 CONTROLLED + 6 OK） |

> **Phase-G7/G8 执行记录（2026-09-21，Phase-BH 转入批 · 全量回归 76 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：
> **G7 文档/基线口径治理**——以「代码/实测为唯一真源」逐项复核并修正陈旧口径：① `SKILL.md §10` 套件数 25→**76 标准套件** / 测试文件 76→**77**；② MCP 工具面三处不一致（`SKILL.md` L71/L293「17」、`README`「19 工具」）统一为 **18 规范工具 + 12 兼容并存**（真源 `_CANONICAL_TOOL_NAMES` 18 项、`test_tools_surface` 亦断言 18），并补齐 `references/Infoseek_MCP集成契约_v1.5.md` 工具表 13→18（补 Key 管理 2 / QCM 1 / 身份归因 1 / 账号取证 1）；③ `README` 测试套件数 62→**77**；④ `dist/quality_baseline.json` **悬空引用**（文件从不存在）收敛为实际产物 `dist/perf_baseline_v101.json`（README + risk-register 两处）；⑤ `core/` 功能模块数 22→**29**；⑥ `tests/run_tests.py` docstring 套件数 73→**76**。**D-6 守护联动**：`test_doc_state_sync_d6.py` 新增 ⑤ 组 E1-E4，断言 25→**29**（SKILL/README 套件数·文件数与实测对拍 + 文档引用的 `dist/*.json` 产物存在性）。
> **G8 公共入口类型契约**——源审计《infoseek_status_boundary_audit_20260921.md》已不存在，**重新边界注入探测**（23 样例）复现登记结论 **12 OK / 0 CONTROLLED / 11 CRASH**（精确吻合「11 处 CRASH」）；11 处全为 `AttributeError`（`None`/`int`/`str`/`list` 直捣 `.get`/`.lower`/`.upper`/`.split`/`.items`），含 **2 处元素级违规**（`render_report([None])` / `detect_conflicts_v3([None])` 单坏源破链）。交付**设计切片（零入口改动）**：`references/g8-entry-contract-design.md`（背景/取证/根因/影响面/三方案对比/推荐 C：`scripts/entry_guard.py` 守卫原语 + 渐进接线/风险/验收/探测附录）+ `tests/test_entry_contract_g8.py`（**14 断言**，新增 CRASH 立即 FAIL、已登记项被修则提示）。**未改任何现有入口签名**，架构级改动留 **G8-apply**。
> 零代码逻辑改动、零公开签名改动，对外版本维持 **v2.2.0**（文档/设计/守护类，变动量<10%）。

> **G8-apply 执行记录（2026-09-22，公共入口类型契约接线 · 全量回归 76 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：G8 设计切片（references/g8-entry-contract-design.md）落地——新增 `scripts/entry_guard.py`（纯 stdlib 守卫原语 `require_text`/`require_mapping`/`require_sequence`/`coerce_mapping_list`）；**11 处公共入口接线受控**（extract_entities / get_entities_by_type / compute_trust_bonus / estimate_cost / score_source / detect_conflicts / render_report / detect_conflicts_v3 / identity_aggregator.aggregate，零公开签名改动）；`tests/test_entry_contract_g8.py` 升级为强回归守卫（21 断言），原 11 处 CRASH 现全部非 CRASH。**验收**：边界注入探测 CRASH==0（9 CONTROLLED + 6 OK）；全量回归 76 PASS / 0 FAIL / 0 TIMEOUT；D-6 文档守护 29 PASS。对外版本维持 **v2.2.0**（边界硬化，零逻辑变更，变动量<10%）。

#### 长尾中文召回增强（P0 落地 + P1 规划）

> **P0 执行记录（2026-09-29，四层退化根因修复 · 全量回归 77 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：
> 源自《infoseek 长尾中文召回评估报告》（2026-09-29）四层退化根因（A 召回退化 / B 召回增强零增益 / C 过滤门控误杀 / D jieba 缺失回退）。
> **P0 三项落地**——均位于 `scripts/infoseek_pipeline.py`，模块 mod-v `1.2.0`→**`1.2.1`**，对外版本维持 **v2.2.0**（模块内增强，变动量<10%）：
> ① **P0-1 长尾中文子查询拆解并行召回**——新增 `_decompose_longtail_cn()`（CJK 且 CJK 字数≥6 时剥离时间/问句/产出类限定词得核心子查询）+ `_fanout_recall()`（子查询共享 deadline 并行召回、url 去重、达阈值 `max(8,max_results*2)` 提前收敛）；`search_web` 默认层/AI 层/串行层统一走扇出（env `INFOSEEK_CN_SUBQ=0` 关闭）。
> ② **P0-2 CN-AI-Web 对含 CJK query 自动启用**——`_search_cn_web` 自判 `_has_cjk(query)` 即跑（不再依赖 `INFOSEEK_CN_AI_SEARCH=1`）；`_default_layer(query)` 对 CJK 自动并入 CN-AI-Web（非 CJK 保留原 opt-in）；`INFOSEEK_CN_AI_AUTO=0` 可关回 opt-in。
> ③ **P0-3 relevance 二级保底送 top-k**——`_filter_relevant` 末级在 floor 窗口仍空时，按原始 relevance 降序送 top-k（默认开，`INFOSEEK_RELEVANCE_TOPK_FALLBACK=0` 恢复严格空返回），根治长尾弱相关 query 被一刀切返回空。
> 守护 `tests/test_p0_cn_longtail_v221.py`（12 断言，CJK 路由/_decompose/_filter_relevant 全 mock 确定性）；D-6 白名单 `infoseek_pipeline.py`→`1.2.1`、SKILL.md/README/ROADMAP 套件数 76→77 同步。

> **v2.3.0 执行记录（2026-09-29，中文 NLP 依赖收口 + zerodep 增强 · 全量回归 78 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：
> 用户指令「6 处裸 import 收敛到 core/jieba_bridge.py + 增强 infoseek_zerodep_nlp.py」。审计实测裸 import **10 处**（6 直命中 + anchor_adapter×2 / summarize_adapter×2 首轮漏检）。
> ① **新增** `core/jieba_bridge.py`（mod-v1.0.0）：统一探测 jieba/jieba.dt/jieba.posseg/jieba.analyse/pypinyin + 按需 initialize + 一次性告警 + 降级永不抛错 + reset 钩子；sys.modules 双向登记防双模块分裂。
> ② **10 处收敛**：text_tokenizer（mod-v1.1.0，删三套状态）/ person_ner（删 pypinyin+jieba.dt 两套状态）/ entity_aliases（热路径 import 消除）/ entity_profile / zerodep_nlp / anchor_adapter×2 / summarize_adapter×2；消费方保持模块对象晚绑定，mock 契约实测生效。
> ③ **zerodep mod-v1.1.0**：内置 ≈250 中+40 英高频词典（估计器 D，单频专业词锚点）+ 锚点掩码切分（根治跨词 n-gram 噪声）+ `weighted_consensus`（阈值自适应）+ 分层合成（锚点高置信/统计共识补词/单票噪声丢弃/全空兜底收紧）+ 置信 (0,3]。
> 守护新增 `test_jieba_bridge_zerodep_v230.py`（26 断言）；更新 ga5/ga9（mock bridge 锁定路径）；risk-register v1.3.0（R36/R37）；套件数 77→78 / 文件 78→79；D-6 29 PASS。对外版本 **v2.3.0**（新增模块 + 底层增强，变动量>30%）。

> **S1 执行记录（2026-09-29，方向②阶段A「外部依赖统一注册表」建表零回归 · 全量回归 79 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：
> 用户裁决「先做方向②阶段A（建表零回归）→ 再做方向一 → 最后②后续阶段」。S1 为**纯新增、零行为改动、零回归，不 bump 对外版本**（版本口径维持 v2.3.0）。
> ① **审计校正三处**：`except ImportError` 总 62 处中 **45 处为 core 包内部兄弟模块互导垫片**（非外部依赖），真实外部第三方依赖点仅 **17 处**（14 业务 + 3 测试）；版本真源实为 **v2.3.0**（非评估报告所写 v2.2.0）；`core/jieba_bridge.py` 已存在并被消费，dep_registry 只做其**上层通用注册表**、委托不重造。
> ② **新增** `deps/registry.yaml`：19 项依赖声明（14 python_pkg / 2 cli_binary / 3 browser_binary），字段含 kind/import/pip/cli/probe/probe_mode/delegate/version_floor/required/degrade/install_hint/consumers；声明式 probe（import/path/env/which）取代 10+ 套分散探测。
> ③ **新增** `core/dep_registry.py`（mod-v1.0.0）：统一事实层接口 `dep_status` / `is_available` / `import_optional` / `require`（+ `get_dep` / `list_deps` / `reset` / `registry_source`）；**jieba/pypinyin 经 `delegate` 委托 `core/jieba_bridge`**（单一真源，不双轨）；零第三方硬依赖（PyYAML/表缺失回退内嵌 `_DEFAULT_DEPS`）；sys.modules 双向登记防双导入分裂；**绝不 import cap 层**（单向依赖：dep 事实层 ⊂ cap 策略层）。
> 守护 `tests/test_dep_registry_v230.py`（**27 断言**：A 声明/schema 8 · B 接口契约 9 · C 零硬依赖/内嵌回退 3 · D 委托桥一致性 3 · E 双导入登记 1 · F 单向依赖 1 · G 缓存 2）；D-6 白名单 `core/dep_registry.py`→`1.0.0`；套件数 78→79 / 文件 79→80；D-6 29 PASS。
> **S1–S7 三阶段路线（用户裁决顺序）**：S1 方向②阶段A 建表零回归 ✅ → S2/S3 方向一阶段A 只观测（候选锚跨域复现，零行为改动）✅ → S4 方向一阶段B learned 影子模式（影响<10% 不 bump）✅ → S5 方向一阶段C 自动晋级（约10–30% bump 第三位 → v2.3.1）✅ → S6/S7 方向②后续阶段（浏览器探测收口 + 消费点分批迁移，bump → v2.3.2）✅。

> **S2 观测记录（2026-09-30，方向一阶段A「候选锚跨域复现」纯离线只读 · 零行为改动 · 不 bump · 不进发行包）**：
> 用户裁决口径 **A+B**：方案A 通用跨域 6 主题（低空经济/人形机器人/固态电池/创新药/量子计算/跨境电商）+ 方案B 金融-大宗 5 主题（碳酸锂/工业硅/稀土/AI算力/铜）= **11 主题 × 8 篇 = 88 篇**正文（每篇 ≥600 字）；渠道=平台 web 搜索 + fetch，不碰知识库。
> 抽取走纯 zerodep 四估计器 + ≥2 估计器共识，**全程关 jieba**（口径一致且复现热路径最终兜底）；仅【调用】既有函数，观测脚本与产物全落 workspace `s2_anchor_observe/`（`anchors_candidates.json` + `S2_观测报告.md`）。
> **核心数据**：3,795 候选；跨域复现是稀疏事件——94.4% 仅单主题，≥2 大类仅 4.1%（大类级分布 1:3636 / 2:102 / 3:32 / 4:16 / 5:4 / 6:5）；非主题词大类≥2 域 154 个。
> **五大发现**：① 高跨域（≥4 的45个）顶端全是研报通用框架词（产业链/数据/供应链/竞争格局…），单维跨域会误收；② 估计器共识是强过滤器但"词典背书的通用词"（市场规模/技术路线）仍漏过；③ 候选混入实体（宁德时代/亿纬锂能/天齐锂业/字节跳动），印证锚点收录须严于实体、须经实体词典/NER 分流；④ 长词掩码残片是最大噪声（形机器人/人形机器/新能源汽/归母净利），根因是 `_longest_match_suppress` 仅单篇内抑制，须在跨文档聚合后再跑一次全局最长匹配；⑤ 剔除三类噪声后真正合格跨域行业锚点仅约 **6–10 个**（能量密度/动力电池/具身智能/出口管制/数据中心/低空飞行）。
> **门控结论**：支持融合报告「跨域复现 + 词性 + 估计器共识」三维联合，并补齐三个**必备前置过滤**（全局碎片抑制 / 实体分流 / 通用词桶）；建议阈值区间（S3 扩样后定死值）：大类≥2（探索3）× 共识篇≥3（区间3–5）× 总篇≥4 且每大类≥2。样本偏小（每主题8篇），**只出分布与候选名单、不钉死阈值**。S3 待办：扩样每主题≥20 篇 / 词性维度落地 / 通用词桶半自动构建 / 阈值敏感性网格——**骨架已落地（2026-10-02）：scripts/s3_expand.py mod-v1.0.0 + references/s3-expand-schema.md，合成语料 --demo 跑通（seeds=8/watch=3/generic=13/entity=15/fragment=2）；真实域校准待样本**。

> **S3 观测记录（2026-09-30，方向一阶段A 扩样+选种 · 纯离线只读 · 零行为改动 · 不 bump）**：语料按裁决扩至 **11 主题 × 20 篇 = 220 篇**（平台 web 搜索 + fetch 正文，渠道刚性）。落地第二版选种口径：硬排除实体/通用桶(52)/内置词(104)/drop_gate/<2 字/**非名词性 pos(2440)**；主门 **topic_cross_count≥3 且 cover≥0.9**。结果 **seeds 37 词 + watch(topic==2) 137 词**（产物 `s2_anchor_observe/out/learned_seeds_S4.json`）。词性过滤是关键增量——把 S2 顶端的框架虚词（全球/行业/预计/落地）挡在 seed 外；但仍有少量高频行业虚词混入，留待 S4 影子对拍 + 人工抽检裁决。

> **S4 执行记录（2026-09-30，方向一阶段B「learned 锚点层 + 影子模式」· openfix 不 bump · 版本维持 v2.3.0 · 放行三闸全过）**：
> **接入面** = `scripts/infoseek_zerodep_nlp.py` 切词词典锚点层（`_est_zh_dictionary`/`_mask_zh_anchors` 共同引用的模块级 frozenset `_ZH_HIGH_FREQ`）。**不改主链源码**——monkeypatch 该属性为「基线 ∪ learned」跑 base/shadow 对拍，force 时同时把 `_optional_jieba`/`_optional_summa` 置空，使对拍确定落到 zerodep 热路径（中文主链默认 jieba 优先，影子测的是 zerodep 兜底分支）。
> ① **新增** `core/learned_anchor_store.py`（mod-v1.0.0，264 行）：独立 learned 层，接口 `is_enabled`（**默认 False**，env `INFOSEEK_LEARNED_ANCHORS`∈1/true/yes/on 才开）/ `load`（异常回退空表绝不抛错）/ `list_entries` / `active_terms`（decision="accept"）/ `pending_terms` / `get` / `upsert_pending` / `bulk_upsert_pending` / `set_decision`（pending/accept/reject）/ `conflicts` / `save`（.tmp+os.replace 原子）/ `reset`；`_refresh_conflicts` 维护长词×短词 substring_of/has_substring 双向列表。**单向依赖铁律**：只依赖标准库 + 同层 state_dir，绝不 import capability_registry / zerodep_nlp / 任何 cap 或主链。
> ② **新增** `scripts/shadow_compare_s4.py`（mod-v1.0.0）：`_force_zerodep`/`_restore`（try/finally 保证引用还原）/ `run(texts, learned)` 逐篇算 added/removed/learned_hits，meta 锁定 phase='S4_shadow'、forced_engine='zerodep'、rule='shadow only; main chain never touched'；产出 JSON+四节 MD 报告。
> ③ **全量影子对拍（220 篇真实 corpus）**：**docs=220 changed=214 injected=37**（差异面 97%）。新增高频榜顶端含真锚（数据中心35/动力电池34/低空经济17/供需缺口17/具身智能15/价格中枢13/固态电池10/现货价格10/规划产能9）也含框架虚词（全球120/行业99/预计91/落地69/不确定性28/全球市场25）；被挤掉词（数据35/电力21/储能21/算力14，含长词切分断点效应）。**人工抽检裁决（S4 仅记录 pending，真正 accept 接线在 S5）**：reject 框架虚词一批（全球/行业/预计/落地/不确定性/全球市场/资本市场/海外市场/领先地位/政策层面 等）；建议 S5 晋级真锚一批（数据中心/动力电池/具身智能/低空经济/能量密度/供需缺口/地缘政治/价格中枢/技术壁垒/知识产权/固态电池/现货价格/规划产能/加征关税/能源转型）。
> ④ **守护** `tests/test_learned_anchor_s4.py`（**27 断言** A–F 六组：存储契约/决策状态机/子串双向登记/原子落盘/**影子旁路只记录不改主链**/learned 层单向依赖 AST 审计）；D-6 白名单加 `core/learned_anchor_store.py`→1.0.0、`scripts/shadow_compare_s4.py`→1.0.0；套件数 79→80 / 文件 80→81。
> **回归踩坑修正（F4）**：装 jieba 后 F4 FAIL——ref 走真实主链命中 jieba 引擎、base 走强制 zerodep，引擎不同输出必异。F4 语义是「shadow base 路径不改 zerodep 估计器输出」，故 ref 改为在**同一强制 zerodep 条件**下计算后立即还原，复跑 27/0。
> **放行三闸**：① 标准回归 **80 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN（304s）**；② 影子差异报告已产出（220 篇/214 changed）；③ 零词典污染（grep 确认主链零引用 learned 符号、`is_enabled()=False`、`active_terms=[]`、仓库无散落 learned_anchors.json）。**统一访问协议默认不启用动态结果，S5 才做自动晋级 accept 接线（预计 bump → v2.3.1）。**

> **S5 执行记录（2026-09-30，方向一阶段C「自动晋级真锚 + 主链显式开关接线」· bump 第三位 → v2.3.1 · 变动量 10–30%）**：
> ① **晋级名单固化**：S4 影子对拍 37 seeds 经程序化对拍闭合，**15 accept 真锚**（低空经济/能量密度/动力电池/规划产能/知识产权/固态电池/数据中心/具身智能/技术壁垒/地缘政治/加征关税/供需缺口/价格中枢/能源转型/现货价格）；**22 reject**（不确定性/资本市场/全球/预计/落地 等框架虚词）本就由选种硬规则（generic/in_builtin/non_noun_pos/drop_gate）天然排除，promote 脚本**不灌入 store**，边界最干净（37−15=22 闭合，accept 内部无子串冲突）。
> ② **新增** `scripts/promote_s5.py`（mod-v1.0.0）：固化 15 词完整证据（topic_cross/coverage/doc_hits/consensus_doc_hits/freq/pos/basis_version=v2.3.1），幂等 `bulk_upsert_pending`+`set_decision("accept")`，accept 运行时子串自检（冲突退出码 2）。真实库 `/root/.infoseek/learned_anchors.json` 首次灌库核验：version=1 / 15 accept / 0 pending / 0 冲突（运行时数据不进仓库）。
> ③ **主链接线** `scripts/infoseek_zerodep_nlp.py`（mod-v1.2.0）：新增统一访问协议 `_active_zh_anchors()`，函数内**双路惰性导入**（无顶层 import，护 F7b）；仅 env `INFOSEEK_LEARNED_ANCHORS`∈1/true/yes/on 时读 accept 词，与基线 `_ZH_HIGH_FREQ` **并集叠加（非替换）**；默认 OFF / store 缺失·损坏·空 逐字节回退基线。两个切词消费点统一改调。
> ④ **守护**：新增 `tests/test_learned_anchor_s5.py`（**31 断言** A–F：名单固化/晋级落库 9 证据字段+basis_version+decided_at/幂等/reject 不入库/主链端到端 OFF 回退·ON 叠加含基线·抽取命中/子串自检）；演进 `test_learned_anchor_s4.py` F7 契约（从「主链零接线」改为「定义存在+无顶层 import+默认 OFF 回退」，29 断言）。D-6 白名单加 `scripts/promote_s5.py`→1.0.0、`scripts/infoseek_zerodep_nlp.py`→1.2.0；套件数 80→81 / 文件 81→82。risk-register v1.4.0（R38 误判污染/R39 store 损坏）。

> **S6/S7 执行记录（2026-09-30，方向②「浏览器探测收口 + 外部依赖消费点统一迁移」· bump 第三位 → v2.3.2 · 行为保持型重构，变动量 10–30%）**：
> ① **S6** `scripts/l2_renderer.py`：chromium / chromium-headless-shell / playwright / camoufox / patchright 的 `path:` 求值改经 `core/dep_registry.py`（`has_module` / `which_path`），组合与降级逻辑留本层，camoufox 目录非空判定保留；import/path/env/which 四路径收口前后逐一对拍 **0 DRIFT**。
> ② **S7** 约 10 个消费点分批迁移：`domain_orchestrator`（Jinja2）/ `anchor_adapter`·`infoseek_zerodep_nlp`（summa）/ `mirror_map`（PyYAML→json 降级）/ `infoseek_auth`（cryptography）/ `mcp_tools_search`（playwright、whisper 用 `has_module` 兼容 sys.modules 注入）/ `sherlock_client`·`maigret_client`（CLI `which_path`）/ `summarize_adapter`（jieba 经 bridge、summa）/ `extensions/qcm/tracing.py`（opentelemetry，深两级 accessor）。可选点 `is_available`、必报错点 `require`；清死导入 shutil。
> ③ **边界裁决**：jieba/pypinyin 保持 `delegate` 委托 `core/jieba_bridge.py` 无双轨；required `import yaml` 与 OTLP 子包不迁移（避免过度收口）。
> ④ **守护/版本**：未新增测试套件（套件数/文件数不变）；D-6 联动——`scripts/compliance_audit.py` docstring 随 bump 并移出 docstring 版本白名单，SKILL.md/manifest/package.json/README/CHANGELOG/RELEASE_NOTES 同步；12 pkg + 2 CLI 收口前后对拍 0 DRIFT。**全量回归 81 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT（338s）ALL GREEN**。


| 编号 | 任务（P1 规划，待实施） | 路径 | 处置 |
| --- | --- | --- | --- |
| P1-CN1 | jieba 固化为必装依赖（消除回退分词精度下降；v2.3.0 已收口探测到 jieba_bridge 单源，是否改「必装」仍待定） | `core/jieba_bridge.py` · `scripts/text_tokenizer.py` · `install.sh` · `requirements.txt` | 部分闭合（探测/降级已单源化；「可选→必装」仍规划，目标机须 pip install jieba） |
| P1-CN2 | CJK query 中文引擎优先路由（长尾中文投喂中文垂直引擎优先于通用/国际引擎） | `scripts/infoseek_pipeline.py`（`_default_layer`/`_engine_weight_for` 引擎权重） | ✅ 已实施（v2.4.0，2026-10-02）：长尾中文 `_default_layer` 前置 CN-AI-Web、权重 0.3→封顶 1.0；`INFOSEEK_CN_PRIORITY=0` 可回退；search_web 传 query |
| P1-CN3 | 构建长尾中文评估基准量化验收（覆盖 A/B/C/D 四层退化的可量化样本集） | `tests/test_longtail_cn_benchmark_cn3.py` + `references/cn3-longtail-benchmark-ledger.md` | ✅ 已实施（v2.4.0，2026-10-02）：46 断言全离线基准，A/B/C/D/D+ 分组对拍（真实网络受限，自建 fixture） |
| P1-CN4 | 部署侧网络边界兜底（CN-AI-Web 非官方端点失效时优雅降级不污染主链） | `scripts/infoseek_pipeline.py`（`_search_cn_web` netguard 兜底） | ✅ 已实施（v2.4.0，2026-10-02）：调用前经 `net_probe.check_hosts` 预判过滤不可达端点（`INFOSEEK_CN_NETGUARD` 默认开），探测异常保守保留全部，逐端点 try/except 不污染主链 |

#### P1 — 真实环境验证（阻塞层 · 环境受限暂缓 · 发布可信度闸）

| 编号 | 任务 | 路径 | 处置 |
| --- | --- | --- | --- |
| P1-1 | L3 登录源真实凭证端到端冒烟（现覆盖均 mock） | `scripts/mcp_tools_search.py`(`_fetch_with_credential`) · `references/credential-tools.md` · `references/api-keys.md` | 真机闭环；完成前发布可信度不成立 |
| P1-2 | OSINT 真实样本误报基线校准（CN/IN/全局阈值、平台别名表、长尾 rank、双源融合精度/召回） | `core/identity_aggregator.py` · `references/trusted-sources.json` | 真机闭环（隔离 venv + sherlock/maigret 真实样本） |
| P1-3 | Linux/macOS 跨平台安装实证（Windows-Git-Bash 已校验） | `install.sh` · `references/external-deps.md` | 真机闭环 |
| P1-4 | 真实搜索环境 research 全链路性能复拍——目标机/真实网络出口对 3000 源跑端到端 profile；沙箱仅 mirrors/Bing 等少数站点可达，DuckDuckGo/Jina/中文引擎/Wikidata 不可达，性能数字无法沙箱独立复现 | `scripts/infoseek_zerodep_nlp.py`（research 链路）· `dist/perf_baseline_v101.json` · `dist/perf_profile_v101.json` · `references/real-env-evidence-log.md`（复用 D-7 台账） | 真机闭环；对拍基线 research 262.5s→115.4s（2.27×）、冲突检测 124.3s→48.9s、re._compile 19.6s→5.3s；⏸️ 随 P1 环境受限暂缓 |

#### P2 — 代码 / 性能（收敛层 · 沙箱可执行 · 核心收益）

| 编号 | 任务 | 路径 | 处置 |
| --- | --- | --- | --- |
| P2-4 | 矛盾检测叙述句事实槽召回增强（扩充方面簇词典 + 评估 B 层 LLM 槽默认策略） | `core/contradiction_scorer.py` · `references/contradiction-synonyms.json` | ✅ 已收口（R2b 收敛层：`references/contradiction-synonyms.json` aspects 20→24 簇 / opposites 8→9 组、`_meta.version` 1.1.0；`core/contradiction_scorer.py` 新增 term-value 事实槽链路（`_TERM_VALUE_ASPECTS` 4 类）与 `NUMERIC_ASPECTS` 10→12 类；守护 `test_p24_term_value_v250.py` **22 断言**；B 层 LLM 槽维持默认关闭（评估结论记延伸项）。零公开签名改动 → 19 处消费点安全） |
| P2-5 | 三链路口径 `domain_bonus` 旁路收口（链 B 旁路并入 `aggregate_score_v2()` 环节化计算） | `scripts/infoseek_core_v2.py:185-197/308/313/339` · `core/anchor_score_v2.py` | ✅ 已收口（R1-b，见 D-2：代码级核实 L313 传 `domain_bonus=0` 系刻意防双重计分、L339 仅回填观测；新增 `test_domain_bonus_no_double_count.py` 守护锁定，不重构评分核心） |
| P2-6 | research 全链路性能热点定位（旧基线 research P50≈83.6s、冲突检测 P50≈39.3s） | `scripts/perf_baseline_v101.py` · `dist/perf_baseline_v101.json` · `scripts/infoseek_core_v2.py` | ✅ 已收口（R2b 收敛层：`scripts/perf_baseline_v101.py` 增 `--profile`（cProfile+pstats 热点）与 `--rounds` 多轮采样；实测 scale 1000×3（`python -u`）评分 P50/P95 1.5/6.4s、冲突 41.0/42.2s、research 126.7/127.1s；产物 `dist/perf_profile_v101.json` + `dist/perf_baseline_v101.json`；守护 `test_perf_profile_d3.py` **23 断言**） |
| P2-A5A7 | 编号 A5–A7 映射**未证实**——当前仓 `A5/A7` 命中均指 GA5 分词单源化（已闭合）或 GA9 测试分组 | `CHANGELOG.md` · `RELEASE_NOTES.md`（历史段） | ✅ 已收口（R3-2026-09-21 全仓复核：`A5/A6/A7` 命中皆为 `GA5/GA6/GA7` **前缀子串**（CHANGELOG L499/L502/L636 · RELEASE_NOTES L165/L219/L224 · 归档 L778-780/L933），无独立 A5–A7 规划编号 → 判为「**编号来源不可考·命名缺失（非代码缺口）**」，非开放缺陷，cancelled） |

> **【口径覆盖 · 2026-10-01 · 不删历史，以下新口径取代上表旧结论】**
> - **P2-4 追加落地（B 层 hybrid 真正接线）**：2026-09-21 旧结论「B 层 LLM 槽维持默认关闭」系指 `score_contradiction_hybrid` 已实现但**从未被主链路调用（孤儿函数）**。本次审计坐实后完成接线——同步/异步/MCP 三入口全部接入：① `scripts/infoseek_core_v2.py` 同步路直接调 `score_contradiction_hybrid`；② 异步路 `await asyncio.to_thread(score_contradiction_hybrid,...)`；③ MCP 异步入口经 `score_contradiction_async`（无 router 分支改走 hybrid，to_thread 包裹，因 `llm_call` 仅同步）。三入口字段透传补齐 `llm_used/llm_error/scorer_mode`，元信息块新增 `contradiction_scoring.method`（local/llm_hybrid）与 `llm_augmented` 计数。**默认 OFF 零行为变化**（三态验证：OFF==base、ON 注入命中 llm_hybrid、无 provider 安全降级回 base 且记 `llm_error`）。方面簇词典 `contradiction-synonyms.json` **v1.1.0→v1.2.0**：24→36 簇、zh 160→267（新增产量/产能/用户规模/成本/利润率/增速/排名/政策态度/负债/现金流/分红/时间点等 12 簇，补既有簇长叙述句同义词）。
> - **P2-5 追加落地（并入 aggregate_score_v2）**：2026-09-21 旧结论「守护锁定、不重构评分核心」被本次明确要求取代——`domain_bonus` 三链路口径旁路已**收口并入 `aggregate_score_v2()` 环节化计算**（见任务⑤复核），不再仅以 `test_domain_bonus_no_double_count.py` 锁定旁路。防双重计分约束保留（KB 交集段 trust_bonus 已含 kb_bonus，domain_bonus 仅承载纯领域特定信任段）。
> - **【销账勘误 · 2026-10-02 · 代码级复跑核实】** 四项任务（G8-apply / 事实槽召回 / 三链路口径 / research 性能）代码真源全部坐实，全量回归 **82 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT（295s）**。两点文档漂移已修正：① 上方 P2-4 所称「`scripts/infoseek_core_v2.py` 同步路**直接调** `score_contradiction_hybrid`」表述不准——实际为**经 `core/conflict_v3.py` 间接接入**：`infoseek_core_v2`（同步 L717 / 异步 L1209 调 `detect_conflicts_v3`）→ `_group_and_detect` L220 → `_score_pair_hybrid` L173（`import contradiction_scorer as _cs` 模块对象调用，永久约束）→ `score_contradiction_hybrid`。全仓唯一生产调用点为 `conflict_v3.py:173`。② 评分契约 v2 §6.1 表格旧写链B domain_bonus「仅报告不计入 final」，已对齐为「经 aggregate_score_v2 计入 final」（见 `references/Infoseek_Anchor_Score评分契约_v2.md` L98）。版本号真源 `scripts/mcp_tools_common.py` SKILL_VERSION=2.3.3；词典 contradiction-synonyms.json `_meta` v1.2.0 / 36 簇 / zh 267 词，与声明一致。**四项均判已收口，予以销账。** 唯一未竟项——真实搜索网络环境下 3000 源 research 全链路性能 profile 无法沙箱复拍（网络边界所限）——已登记为 **P1-4 / Phase-D**，随 P1 阻塞层暂缓。


#### P3 — 前景（远期层 · 归档，v2.x 立项）

| 编号 | 方向 | 路径 | 处置 |
| --- | --- | --- | --- |
| P3-9 | 合规审计增强（抓取合规 / 版权 / 凭证审计自动化报告） | `scripts/compliance_audit.py` · `references/compliance-audit-report.{md,json}` | ✅ 已落地（R3-2026-09-21；守护 `tests/test_compliance_audit_v220.py` **30 断言**，幂等 4 次复证；全文零明文） |
| P3-7/8/10 | 多模态理解 / 编排·多 agent 协同 / 本地文件集成 | 独立大模块（保持零依赖 + 降级路径） | 归档（远期立项） |
| P3-边界 | 明确不做：实时新闻监控 / 学术文献综述 / 浏览器自动化爬取 / 即时聊天对话 | — | 归档（设计边界） |

#### B — 文档陈旧（清理层）

| 编号 | 陈旧点 | 路径 | 处置 |
| --- | --- | --- | --- |
| B-1 | v2.2.0 回归数写 **66 PASS / 229s**（实为 67 PASS / 231s，含新增 llm_fields 套件） | `CHANGELOG.md`（v2.2.0「守护与回归」段 L43） | ✅ 已清理（R1-c：L43 已为 67 PASS/231s；2026-09-20 复核） |
| B-2 | 风险注册表 v1.0.1 称 `fetch_content` L2–L4 为函数壳（现行代码 L2 渲染 / L3 凭证 / L4 多媒体均已接线） | `references/risk-register.md` | ✅ 已清理/归档（R1-c：L35 改为「L2-L4 已接线（L2 渲染/L3 凭证/L4 多媒体）」；2026-09-20 复核无「函数壳」残留） |
| B-3 | `freshness_cron.py` 版本/步骤/docstring 漂移（头注释标 v2.4.0；头列 6 步、实现称第 7 步；`run_full_scan` docstring 仅述衰减/冷条目/alias） | `core/freshness_cron.py:1-16/128-167` | ✅ 已清理（R1-c：头注 v2.2.0 + 7 步枚举；2026-09-20 复核 L3/L5/L12 属实） |
| B-4 | `mcp_tools_forensics.py` 内部 docstring 标 v1.0.0（MCP 集成语境 v1.6.0） | `scripts/mcp_tools_forensics.py:3` | ✅ 已清理（R1-c：docstring 改 v2.2.0） |
| B-5 | 本路线图自身基线表标题/回归数旧（L12 v2.1.0 / L17 65 PASS·2 SKIP·87.9s） | `references/ROADMAP.md`（本次计入时已同步） | ✅ 已清理（R1-c 起逐步同步；R3-2026-09-21 复核：L3 已 2026-09-21、L17 已 75 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT（75 套件）、验收总闸已 75 PASS） |

#### C — 历史归档误命中（归档层）

| 编号 | 误命中点 | 路径 | 处置 |
| --- | --- | --- | --- |
| C-1 | DEF-13~16 早期「开放」表述实为 v2.1.0 立案快照，v2.1.1 已修复/关闭 | `CHANGELOG.md` 历史段（L235 立案快照） · `tests/test_p2_v211.py` | ✅ 已归档（R2-2026-09-20：CHANGELOG 立案段标题下加事后闭合注，历史正文/Open 口径段不改；守护 test_p2_v211.py 四组 70 断言） |
| C-2 | 「A5」在归档中为 GA9 测试分组，非当前 A5–A7 规划项 | `CHANGELOG.md` · `RELEASE_NOTES.md` 历史段（命中皆 GA5 分词单源化，已闭合）· `ROADMAP_archive_20260917.md:933`（A4/A5=GA9 检测守卫测试分组）；原引 `roadmap_ch812.md` **文件已不存在（死路径，2026-09-20 glob 证实）** | ✅ 已归档（R2-2026-09-20：A5 去伪结论见 P2-A5A7 行；死路径仅在本行注明，不触碰冻结归档） |
| C-3 | GA5/GA9/GA10/GA11/GA12 等历史事项已闭合；G6 真实网络运行并入 P1 | `ROADMAP_archive_20260917.md`（冻结快照 L3-9 声明明确「仅供追溯」） | ✅ 已归档（R2-2026-09-20 复核归档声明成立；冻结快照只查不改，G6 真机诉求见 P1 表） |

#### D — 建议立项（收敛层 · 规划任务 + 审计缺口）

| 编号 | 建议 | 路径 | 处置 |
| --- | --- | --- | --- |
| D-1 | learned prune cron **apply 安全测试**：补「cron 携带 `INFOSEEK_LEARNED_PRUNE_APPLY=1` 时真实落盘」用例 + 真实 `active_names` 传入 + stats 透出 `remaining/dry_run/applied` | `core/freshness_cron.py:128-167` · `core/entities.py` · `tests/test_learned_prune_cron_r1a.py` | ✅ 已收口（R1-a：真实 active_names + stats 透出 applied，守护 test_learned_prune_cron_r1a.py） |
| D-2 | 三链路评分字段**归属统一 + 架构守护测试**（与 P2-5 同源，落地为守护） | `scripts/infoseek_core_v2.py` · `core/anchor_score_v2.py` · `tests/test_domain_bonus_no_double_count.py` | ✅ 已收口（R1-b：守护锁定链 B 传 `domain_bonus=0` 防双重计分、链 A 计入） |
| D-3 | research 融合阶段**性能 profiling**（与 P2-6 同源，落地为采样基线） | `scripts/perf_baseline_v101.py` | ✅ 已收口（R2b 收敛层：与 P2-6 同源；`_STATS_ROW` 表格解析 + `profile_research()` 采样，可离线复跑） |
| D-4 | 叙述句事实槽召回增强（与 P2-4 同源） | `core/contradiction_scorer.py` | ✅ 已收口（R2b 收敛层：与 P2-4 同源；`_term_value()` 槽抽取 + `_build_keyed_slots` 接线） |
| D-5 | `infoseek_mcp_server.py` 连续重复 `elif tool_name == "account_forensics"` 死分支清理（L549/L551 第二个不可达） | `scripts/infoseek_mcp_server.py:549-552` | ✅ 已清理（R2b 收敛层复核：`elif tool_name == "account_forensics"` 现存 **1 处**（L549），连续重复死分支已于 R1-c 删除） |
| D-6 | 文档真实状态**同步机制**（风险表 / ROADMAP / CHANGELOG / 内部 docstring 版本与结论自动校验） | `references/` · CI/`tests/` | ✅ 已收口（R2b 收敛层：新增 `tests/test_doc_state_sync_d6.py` **25 断言**（A 8 / B 9 / C 4 / D 4）——五文档版本单源 + ROADMAP 基线行自校验 + docstring 分歧白名单 + 产物 JSON 契约 + ROADMAP 严格 UTF-8；三处解码点加 `errors=replace`；ROADMAP 尾部 2 个非 UTF-8 字节已同行清理） |
| D-7 | 真实环境验证**证据归档模板 + 验收台账**（支撑 P1 可复现） | `references/`（新增） | ✅ 已立项并交付模板（R2b 收敛层：新增 `references/real-env-evidence-log.md` 证据归档模板 + 验收台账；真机样本仍受 P1 环境阻塞，模板冻结可填） |
| D-8 | 合规审计自动化（= P3-9 立项形式） | `scripts/compliance_audit.py` · `tests/test_compliance_audit_v220.py`（30 断言） · `references/compliance-audit-report.{md,json}` | ✅ 已落地（R3-2026-09-21：凭证审计 / 抓取合规 / 网络边界 / 版权来源四维 → Markdown+JSON 双产物，全文零明文；自指污染已修（自产物跳过 + `_redact` 不回显明文），幂等 4 次复证 30 PASS / exit=0） |
| D-审 | 无 `audit`/`审计` 命名文件**≠ 无审计缺口**；A5–A7 编号仅「命名缺失」 | — | ✅ 已闭合（R3-2026-09-21：审计能力已由 D-8/P3-9 落地补齐；A5–A7 经全仓整词复核判为「编号来源不可考·命名缺失（非代码缺口）」，详见 P2-A5A7 行） |

**补注**：全仓 `TODO|FIXME|XXX|HACK` 仅命中 `scripts/leak_scan.py` 文档示例 `XXX_API_KEY`，无真实未处理标记；`scripts/perf_baseline_v101.py` 支持 `--rounds` 多轮采样，非缺陷。

#### HF — 人因指纹增强（2026-09-21 评估立项 · 载体须换 · 红线不碰）

> 评估结论：**目标可行、载体须换、增量靠补齐、红线不碰**。三类因子对既有资产重叠度 60%～75%，增量在**既有资产补齐**而非新建体系。
> 全文：`references/human-fingerprint-feasibility-report.md`（八节：结论摘要 / 任务背景 / 三类因子逐项可行性 / 合规边界裁决 / 重叠度矩阵 / 开发路径与优先级 / 风险与合规闸 / 结论与建议）。
> 红线边界：**设备 / 客户端指纹（UA / 屏幕 / Canvas·WebGL / 字体 / 时区 / JA3·JA4）一律不采集**——触碰 `PRIVACY.md §4/§6`、`network-boundary-report.md §4`，且与 `scripts/l2_renderer.py` 反指纹方向相反。

| 编号 | 任务 | 路径 | 处置 |
| --- | --- | --- | --- |
| HF-P0 | 既有资产补齐（零合规风险）：AccountTrustScorer 增「内容伪造特征」子维→五维；FakeDetect L1 增列活跃时段熵 / 节奏规律 / 内容模板化 n-gram；粉丝质量回灌；`account_forensics` dataset 增 `profile` / `timing` 字段（向后兼容） | `scripts/account_trust_scorer.py` · `extensions/fake_detect/l1_engine.py` · `scripts/mcp_tools_forensics.py` | ✅ 已落地（HF-R1 · 2026-09-21）：仅扩字段 + 规则，**不新增能力项 / 不改 network_boundary / 不动默认开关**；守护 `tests/test_hf_r1_v220.py`（33 断言，零回归） |
| HF-P1 | 协同簇增强 + 融合权重校准：`coord_clusters` / `sync_groups` 群体置信注入融合→A/B/C/D 四因子（D = 协同簇强度）；四因子动态重归一化；FPR ≤ 2% + `train_l1_thresholds` 重训 | `scripts/identity_confidence_fusion.py` · `extensions/fake_detect/` | ⏳ 部分落地（HF-P1 · 2026-09-21）：D 因子 + 四因子动态重归一化 + 样本接入契约/校准套件已就绪；**权重最终值与生产 FPR 待真实样本校准**（沙箱无真实环境）；**L1 重训骨架已落地（2026-10-02）：scripts/train_l1_thresholds.py mod-v1.0.0 + references/l1-retrain-schema.md，合成账户 --demo FPR=0.012≤0.02；真实校准仍待样本** |
| HF-P2 | 设备层窄口（**暂缓**）：仅「账号自身主动公开发布的设备标签」作弱证据；前置 = 修订 `PRIVACY.md §4` + 重评 network_boundary + 6 条合规判据全通 + 用户显式授权 | `PRIVACY.md` · `references/network-boundary-report.md` | 仅登记不排期（红线内候选，当前建议：不实施） |
| HF-否 | **否决项**：设备 / 客户端指纹（义 1）不采集；保留「机械化行为指纹」（义 2） | — | 红线（`PRIVACY §4/§6` / `network §4`） |

> 术语口径：义 1「设备 / 客户端指纹」（采「设备是什么」，被动计算，红线）与义 2「机械化行为指纹」（采「行为像不像机器」，主动观察账号可见行为，安全）**命名分离**，禁用「机器指纹」混指。
> 版本：评估类文档，零代码逻辑改动，对外版本维持 **v2.2.0**。

> **HF-R1 执行记录（2026-09-21，人因指纹增强 P0 落地 · 全量回归 74 PASS / 0 SKIP / 0 FAIL / 0 TIMEOUT ALL GREEN）**：四子项编码完成——① `scripts/account_trust_scorer.py` v1.0.0→**v1.1.0**，新增「内容伪造特征」子维（`template_similarity` / `ai_generated_ratio` / `duplicate_ratio`）四维升五维，权重各 0.20，`confidence` 分母随维度数自适应；② `extensions/fake_detect/l1_engine.py` 增列 `hour_entropy` / `rhythm_cv` / `tpl_ngram` / `follower_quality` 四特征并新增 L1f-L1i 四条规则（**默认关闭** `*_enabled=False`，不进入既有 `n_flags` 聚合 → 零回归），`l1_rule_names()` 扩至 9 项；③ `extensions/fake_detect/data_adapter.py` 增 `follower_quality` / `template_similarity` 别名与归一化（0-100 自动降 0-1）；④ `scripts/mcp_tools_forensics.py` dataset 增 `profile` / `timing` 字段（向后兼容，`from_raw` 透传 → `Dataset.profile/timing`）。守护 `tests/test_hf_r1_v220.py`（**33 断言**：A 五维 / B 零回归 / C 粉丝质量回灌 / D profile·timing 兼容 / E 合规判据）；连带修复 `l1_engine.spike_feats` 空数组守卫（growth 缺失不再崩，非空行为不变）；D-6 白名单同步（`scripts/account_trust_scorer.py` → `1.1.0`）。零破坏性变更（`DIM_WEIGHTS` 四维→五维、`apply_l1_rules` 返回追加键属扩展型），对外版本维持 **v2.2.0**。

> **HF-P1 执行记录（2026-09-21，协同簇融合 + 真实样本准备落地）**：① `scripts/identity_confidence_fusion.py` v1.6.0→**v1.7.0** —— A/B/C **扩为 A/B/C/D**（D = 协同簇强度，`norm_cluster` 综合 `coord_clusters` 规模/密度 + `sync_groups` 规模，复用 CROSS_SOURCE_BOOST 群体证据语义）；D 以**互补证据**参与（协同越强 → 身份置信越下调），四因子**动态重归一化**（缺因子不中断）；默认权重 `a:b:c:d = 0.28:0.32:0.20:0.20`，其中 **a:b:c 保持旧 7:8:5 比例 → 无 D 信号时逐点等价旧三因子（零回归）**；`INFOSEEK_FUSION_WEIGHTS` 兼容旧 3 值（d=0）与新 4 值。② **真实样本准备物**：`references/hf-real-sample-schema.md`（接入契约：schema / 来源清单 / 合规闸 / 校准流程）+ `scripts/hf_sample_kit.py`（`--validate` 契约校验 / `make_synthetic` 半合成打样 / `--calibrate` 在 FPR ≤ 2% 约束下搜 D 权重 + 扫描曲线）。③ 守护 `tests/test_hf_p1_v220.py`（**33 断言**：A D 因子归一化 / B 四因子融合 / C 零回归 / D 权重契约 / E 样本套件 / F 合规容错）；既有 `test_identity_fusion_v160.py` **39/39 全绿**（零回归）。④ 半合成打样实测 **D 因子增益显著**：`d=0 → recall 0.52`；`d=0.20（默认）→ recall 1.00 @ FPR 0.6%`。**遗留（须真实样本）**：权重最终值、CN/IN/全局分区 FPR、`train_l1_thresholds` 重训 —— 待 Phase-B 真机样本。（对外版本维持 **v2.2.0**）

#### P1 执行 phase（最高优先级任务 · 真实环境）

- **Phase-A · L3 凭证冒烟**（约 0.5d）：目标机 `export` 真实 key → 对 1 个登录源跑 `fetch_content` → 断言 `extraction_level==3` 且正文非空 → 响应摘要/`cosKey` 入验收台账。
- **Phase-B · OSINT 阈值标定**（约 1d）：隔离 venv 装 `sherlock-project`/`maigret` → 真实样本跑双源聚合 → 标定 CN/IN/全局误报阈值、平台别名、长尾 rank → `test_identity_aggregator*` 不劣化。
- **Phase-C · 跨平台安装**（约 0.5d）：Linux/macOS 各跑 `bash install.sh --venv` → 回归全绿 → 记录 OS/依赖版本。
- **Phase-D · 真实搜索性能复拍**（约 0.5d）：目标机/真实网络出口对 3000 源跑 research 端到端 cProfile → 与基线对拍（research 262.5s→115.4s / 2.27×、冲突检测 124.3s→48.9s、re._compile 19.6s→5.3s）→ profile 与对拍结论入 `references/real-env-evidence-log.md` 台账。
- **解冻条件**：A/B/C/D 四绿 → 才恢复 v2.2.0 发布收尾（备份 tar → ima 幂等注册 → 终检）。
- **验收总闸**：`cd /root/.skills/infoseek && python tests/run_tests.py` → 0 FAIL / 0 TIMEOUT。
- **状态**：⏸️ 暂缓——当前环境不支持真实环境/跨平台，待目标机就绪后按 A→B→C→D 执行。

---

## 三、2026-09-18 收尾记录（v2.1.0 OSINT 契约修复 + 双源聚合）

审计起点是原 P1「OSINT 双客户端真实实证」。沙箱 pip 实测 sherlock-project 0.16.2 /
maigret 0.6.5 后，发现 ROADMAP 未记录的 **P0 集成故障**，并交付三项产物：

- **P0 契约修复**：sherlock `--json` 实为站点数据输入、无 JSON 结果 → 改 `--csv` 读回；
  maigret `-J simple` 是报告类型且写文件、`status` 为嵌套 dict、`-a` 是全量站点 →
  改临时目录读 `reports/report_<user>_simple.json` + `--top-sites N`。修掉 sherlock
  username 写死空串致 cross_platform 统计失效的连带 bug。
- **双源聚合**（`core/identity_aggregator.py`）：旧 compensate 只取首个成功源、两源从不
  融合；现双源优先 + 归一去重 + 交叉确认置信增强 + 误报抑制 + 分区，全空回退单源代偿链。
- **授权 CLI**（`infoseek_consent_cli.py`）：闭合原 P1#3 代码侧；真实长驻授权仍靠
  shell export（设计上不改写只读 registry.yaml）。
- **测试脆弱性根因修复**：三处身份相关测试原依赖"本机恰好未装 CLI"，装了真 CLI 即挂死；
  统一改注入式 mock 显式锁定路径。新增 2 套件（聚合 24 + CLI 16 断言），客户端契约
  守护扩至 20 断言。版本 2.0.0 → **2.1.0**（MINOR）。
- 仍开放：上述真实环境三类冒烟（凭证 / OSINT 样本阈值 / 跨平台安装）。

---

## 三·续、2026-09-19 收尾记录（v2.1.2 事件槽批次 · GA11 阶段 1-3）

起点是 2.1.1 立案的 P3 三缺口（F-06 多事实句召回 / F-04 相邻季语义裁决 / F-07 time 路跨主体误报）；
其主体前置依赖已由 2.1.1-openfix-p3stage0（主体贯通）解除，本批按 GA11 事件槽重构阶段顺序落地：

- **F-06 事件抽取**：新增零依赖 `_split_clauses` / `_extract_events`，逐事件
  `{subject, aspect, value, polarity, time_span, event_sig}`；数值/方面由「全文单次扫描」改为
  **句内独立归属**（这才是 F-06 的原始缺口）；事件在**原始正文**抽取并随 claim 穿透
  （`conflict_v3._extract_fact_claims` → `_group_and_detect`），跨越 `text[:500]` / `text[:300]` 两级截断。
- **F-04 期间裁决**：新增 `_period_adjudicate`；同主体同方面且双方期间均已知且不相交 → 判为非冲突，
  落地为**降权（×0.5，不滤除、不归零）**；触发条件严格三连（含「空主体不裁决」以守旧契约）。
- **F-07 time 路主体闸**：`time_slot_score` 向后兼容扩展 `subject/subject_b/events_a/events_b`；
  同主体 → 事件级对齐（`_event_time_score`），跨主体 → 不可对拍（消除跨主体时间误报）。
- **research 链路字段穿透对齐**（异步两处 + 同步一处统一）。
- **零回归口径**：唯一行为变化点是「双方主体非空且相等 + 同方面 + 双方期间非空且不相交」，
  对应 `test_p1_hardening_v211` L105-109 语料（60→30），断言已按 F-04 语义更新并补两例。
- 版本 2.1.1 → **2.1.2**（PATCH）；守护 `tests/test_event_slots_v220.py`（47 断言 / 5 组）。

## 三·续二、2026-09-19 收尾记录（v2.2.0 三元事件身份 + 时间槽键 + LLM 收口 · GA11 阶段 1-3 续）

v2.1.2 后跨文本对齐仍用二元 `event_sig=(subject, aspect)`，不同期间的同主体同方面事件无法在事件层
区分；且 B 层 LLM 成功路径返回窄白名单 dict，截断 v2.1.2/v2.2.0 全部事件槽字段。本批：

- **阶段 1**：事件增 `time_key`（`{start,end,label}` 半开 `[start,end)`），单句多 span 事件**扇出**，
  跨文本签名升三元 `(subject, aspect, time_key)`；三类键严格分离。
- **阶段 2**：`_event_time_score` 三元对拍（同键才对；不同 time_key 按真实半开区间，overlap→conflict、
  全 disjoint→60/35，端点相接=disjoint，span 缺失保守不误判）；透出 `event_disjoint_slots`/
  `event_overlap_slots`/`event_pairs` 与多期间逐对 `period_pair_details`。
- **阶段 3**：B 层 LLM 槽表增时间维度（真实 span disjoint→suppression）；同步 `score_with_llm`
  **窄白名单截断根治**——以完整 A 层 `dict(local)` 为底；同步/异步/hybrid/batch/`infoseek_core_v2`/
  MCP wrapper 统一字段透传（审计无白名单）；纯 A 层默认补两个 suppression 空列表。
- 守护：`tests/test_event_slots_v220.py` **54 断言**；新增 `tests/test_llm_fields_v220.py` **26 断言**
  锁定五出口 A 层 31 字段完整超集契约（防窄白名单回归），并固化 R4 修复（router 返 None 旧被伪装成
  异常降级，同步/异步统一 raw 归一化）。
- 全量回归（`tests/run_tests.py` 唯一入口）**75 PASS / 0 SKIP / 0 FAIL ALL GREEN**
  （较 bump 前 66 套件新增 llm_fields）；版本单源守护 22 PASS。
- 版本 2.1.2 → **2.2.0**（MINOR：事件身份签名升级跨 2 核心模块）；联动 7 处版本号（含
  `core/__init__.__version__`）+ CHANGELOG/RELEASE_NOTES；代码内 `v2.1.2` 历史标注为历史锚点不改；
  B 层 LLM 默认关闭；默认不推 GitHub。

---

## 四、前景方向

- **短期**：把已实现能力从「测试验证」推向「生产可用」——真实凭证 / 真实 OSINT 样本阈值 /
  跨平台安装三类**必须在真实环境闭环**的冒烟（P1 #1-#3）。
- **中期（v2.x）**：矛盾检测叙述句召回、research 性能、口径旁路收口；与 QCM 等
  跨 skill 协同继续扩展（已有契约基础）。
- **长期**：AI Agent 深度协作、实时协作调研；坚持零依赖哲学
  （所有增强均有降级路径，可选依赖缺失不塌）。

---

## 五、验收总闸（每次合入）

- 全量回归全绿：`python tests/run_tests.py` → 0 FAIL / 0 TIMEOUT（SKIP 需为可选依赖 preflight）。
- 零破坏性变更：状态文件（`~/.infoseek/*.json`）/ env 向后兼容；清理类动作默认 dry_run。
- 版本单源：对外版本只改 `scripts/mcp_tools_common.py:SKILL_VERSION`，并与
  SKILL.md / manifest / package.json / RELEASE_NOTES / CHANGELOG 联动；四维版本语义不得混用。
- 文档同步：SKILL.md / README / 本路线图；历史实施细节入归档而非堆积本文件。
- 发布前：备份 tar（命名带章节/内容标识 + 解包校验）→ ima 幂等注册 → 嵌套终检
  （`find -maxdepth 2 -type d | grep "/infoseek/infoseek$"` 须零命中）。
