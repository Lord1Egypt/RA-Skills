## 会议深度加工与质量增强引擎任务清单与依赖拓扑

会议深度加工与质量增强引擎按会议数据处理流程组织的任务清单，附任务间关系和元操作映射提示。

**使用方式**：定位目标任务后，**清单法**读取 `meeting-deep-process-requirements.md` 获取对应任务的组件清单与约束条件，按清单逐项产出；**样本法**读取 `exemplars.md` 范本索引后定位到具体范本文件，按四维分析（结构/风格/逻辑/格式）模仿产出。两种方法可同时使用——清单法保规范完整，样本法保风格一致。

**域间逻辑流**：D04（剖面初始化）→ D01（场景识别+执行，含D05-enhance-02亮点设计）→ D02（分析）→ D03（转化）+ D05-enhance-01（质量诊断）→ D04（剖面更新闭环）→ D05-enhance-04（模式优化）→ D05-enhance-02（改进后设计→下场会议）

---

### D01 智能交互执行域

| ID | 任务类型 | 说明 | 依赖 | 元操作映射 |
|----|---------|------|------|-----------|
| mdp-exec-01 | 交互上下文装配 | 聚合历史上下文，识别8种场景类型，判定数据充分度并下发场景参数至下游任务 | 无（入口） | S→C→O |
| mdp-exec-02 | 原生交互编排 | AI引导议题，实时捕获决策→行动项映射，交互结束时结构化产出已就绪 | 无（入口） | S→C→A→O |
| mdp-exec-03 | 外部会议兼容执行 | 被动参会三段式：会前加载议程与剖面 → 会中旁听与焦点提醒 → 会后摘要、待办与归档 | 无（入口） | S→C→A→O→G |

---

### D02 交互效能分析域

| ID | 任务类型 | 说明 | 依赖 | 元操作映射 |
|----|---------|------|------|-----------|
| mdp-analyze-01 | 跨录制议题聚类 | 多场会议议题自动聚类与主题热力图生成；场景参数调整聚类权重（谈判型偏向分歧点聚类，调解型偏向和解信号聚类，决策型偏向决策点聚类）；沉默议题预警 | mdp-exec-03 | S→C→A |
| mdp-analyze-02 | 决策溯源关联 | 任意决策回溯到原始发言片段（会议ID+speaker+timestamp）；跨会议决策链追踪（A决策→B结果→C修正）；与D04累积剖面关联标注决策者画像 | mdp-exec-03 | S→C→A |
| mdp-analyze-03 | 群体动力分析 | 立场聚类、权力流向、剖面-立场分歧检测、阵营稳定性、桥接者识别 | mdp-exec-03, mdp-profile-01 | S→C→A |
| mdp-analyze-04 | 发言者参与度分析 | 发言时长分布统计；话语权集中度指数；交互网络有向图谱（谁对谁说话）；沉默者与主导者识别 | mdp-exec-03 | S→C→A |
| mdp-analyze-05 | 行动闭环验证 | 决策存活率（已执行/已推翻/已遗忘）；行动项闭合率（及时完成/延期/未开始）；重复决策检测（同一议题在≥2场会议中反复出现但从未落地→预警） | mdp-exec-03 | S→C→G |
| mdp-analyze-06 | 录制价值评估 | 单场录制的信息密度评分；决策产出率；场景适配的ROI评估（谈判型=让步vs收益比，调解型=冲突降级幅度，信息型=知识传递有效率）；值得参加判断 | mdp-exec-03 | S→C→G |
| mdp-analyze-07 | 效率趋势分析 | 周期性体检报告（周/月/季）；时长趋势、决策密度变化、议程偏离率、可异步替代率趋势；≥2场会议数据后激活 | mdp-analyze-01, mdp-analyze-05, mdp-analyze-06 | S→C→A→G |

---

### D03 知识资产沉淀域

| ID | 任务类型 | 说明 | 依赖 | 元操作映射 |
|----|---------|------|------|-----------|
| mdp-knowledge-01 | 报告自动起草 | 按场景匹配报告模板自动生成周报/月报/项目报告；区分事实摘要（无人工干预自动生成）与润色稿（人工审核出口）；多语种适配 | mdp-exec-03, mdp-analyze-01 | C→A |
| mdp-knowledge-02 | 复盘材料生成 | 项目全生命周期交互串联（从启动到交付的完整信息链，涵盖原生交互和外部会议）；关键决策点+转折事件+经验教训一键生成 | mdp-exec-03, mdp-analyze-02 | C→A |
| mdp-knowledge-03 | 知识库条目提取 | 从会议数据抽取结构化知识点，标注来源与置信度，跨会议去重合并 | mdp-exec-03 | S→C→A→G |
| mdp-knowledge-04 | 结构化画像抽取 | 面试记录→候选人12维剖面（关联mdp-profile-01）；培训记录→结构化教学内容+知识点+案例抽取；外部沟通（路演/客户会议）→标准话术库条目持续优化 | mdp-exec-03, mdp-profile-02 | S→C→A→O |

---

### D04 发言者12维剖面分析域

| ID | 任务类型 | 说明 | 依赖 | 元操作映射 |
|----|---------|------|------|-----------|
| mdp-profile-01 | 单次剖面快照 | 单场会议中每个发言者的12维初步推断，标注置信度与信号来源 | mdp-exec-03 | S→C→A |
| mdp-profile-02 | 累积剖面画像 | 多场聚合的个人完整12维画像，≥2场激活，贝叶斯更新冲突数据 | mdp-profile-01 | C→A→O |
| mdp-profile-03 | 本人剖面对比 | 发言者画像与自身剖面的12维差异矩阵，识别维度对齐与张力 | mdp-profile-02 | C→A |
| mdp-profile-04 | 剖面演化追踪 | 跨时期12维变化轨迹检测，≥3场激活，识别晋升、离职等演化信号 | mdp-profile-02 | S→C→G |
| mdp-profile-05 | 交互策略生成 | 基于差异矩阵生成12维适配的个性化沟通策略与协作建议 | mdp-profile-03 | C→A |

---

### D05 会议质量增强域

| ID | 任务类型 | 说明 | 依赖 | 元操作映射 |
|----|---------|------|------|-----------|
| mdp-enhance-01a | 6维量化评分 | 6维质量评分（信息密度/新颖性/冲突深度/决策清晰度/参与均衡度/洞察产出率），场景权重自适应 | mdp-exec-03, mdp-analyze-04 | S→C→G |
| mdp-enhance-01b | 根因分析与12维诊断 | 对低分维度根因追溯，并行执行6项12维诊断信号检测，与根因交叉验证 | mdp-enhance-01a, mdp-profile-01 | S→C→G |
| mdp-enhance-01c | 亮点识别与改进方向 | 定位"差点成为亮点"的发言片段，标注追问方向与优先级排序的结构化改进方向 | mdp-enhance-01b | S→C→A |
| mdp-enhance-02a | 会前触发点设计 | 基于议程与参会人剖面生成场景适配的高质量触发点方案 | mdp-exec-01, mdp-profile-02 | S→C→A→O |
| mdp-enhance-02b | 触发点增量优化 | 对比触发点实际效果与设计预期，优化下一场同类会议的触发点方案 | mdp-enhance-01c, mdp-enhance-02a | C→A→O |
| mdp-enhance-03a | 实时话语深度干预 | 实时监测讨论深度，按12维特征匹配干预风格，每场≤3次（需实时转写流） | mdp-exec-03 | S→C→I |
| mdp-enhance-03b | 离线追问清单生成 | 识别应追问未追问节点，标注12维适配的追问方向与预期路径 | mdp-exec-03 | S→C→A |
| mdp-enhance-04 | 会议模式优化 | 识别跨会议重复平淡模式，执行12维人-会匹配分析，输出改进方案（≥3场激活） | mdp-enhance-01b, mdp-enhance-01c, mdp-analyze-07 | S→C→A→G |

**D05域内管线**：
- 质量诊断链：01a(评分) → 01b(根因+12维诊断) → 01c(亮点+改进方向)
- 亮点设计链：02a(会前设计) → 会议执行 → 01c(亮点识别) → 02b(增量优化)
- 话语干预链：03a(实时干预) ‖ 03b(离线清单) （并行，均依赖exec-03，03a需实时流转发）
- 跨会闭环：01b+01c(多场累积) → 04(模式优化) → 02a(下场会议设计改进)

D05任务场景适配参数（6维评分权重、触发点选用、干预阈值、模式差异化）及12维角色模型适配表（诊断信号、触发点定向激活、干预模式、人-会匹配）详见 `meeting-deep-process-requirements.md` D05域。

---

## 依赖拓扑摘要

### 域内链路

**D01智能交互执行链路**: mdp-exec-01 → mdp-exec-02/mdp-exec-03（场景识别后选择模式）

**D02交互效能分析链路**: mdp-exec-03 → mdp-analyze-01/mdp-analyze-02/mdp-analyze-03/mdp-analyze-04/mdp-analyze-05/mdp-analyze-06 → mdp-analyze-07

**D03知识资产沉淀链路**: mdp-exec-03 + mdp-analyze-01/mdp-analyze-02 + mdp-profile-02 → mdp-knowledge-01/mdp-knowledge-02/mdp-knowledge-03/mdp-knowledge-04

**D04发言者剖面分析链路**: mdp-exec-03 → mdp-profile-01 → mdp-profile-02 → mdp-profile-03/mdp-profile-04 → mdp-profile-05

**D05会议质量增强链路**: mdp-exec-03 + mdp-analyze-04 → mdp-enhance-01a → mdp-enhance-01b → mdp-enhance-01c; mdp-exec-01 + mdp-profile-02 → mdp-enhance-02a → (会议执行) → mdp-enhance-01c → mdp-enhance-02b; mdp-exec-03 → mdp-enhance-03a（需实时转写流）; mdp-exec-03 → mdp-enhance-03b; mdp-enhance-01b + mdp-enhance-01c + mdp-analyze-07 → mdp-enhance-04

### 跨域协同链路

**完整处理链路（单场会议）**: mdp-exec-01 → mdp-exec-03 → [mdp-profile-01 ‖ mdp-analyze-01-06] → [mdp-knowledge-01-04 ‖ mdp-profile-03 ‖ mdp-profile-05 ‖ mdp-enhance-01a → mdp-enhance-01b → mdp-enhance-01c ‖ mdp-enhance-03a ‖ mdp-enhance-03b] → mdp-enhance-02a(下次) → mdp-enhance-02b(本次反馈)

**剖面闭环链路**: mdp-exec-03 → mdp-profile-01 → mdp-profile-02 → mdp-exec-01（下次会议前加载更新后的累积剖面）

**分析→知识反馈链路**: mdp-analyze-01 → mdp-knowledge-01; mdp-analyze-02 → mdp-knowledge-02

**分析→剖面增强链路**: mdp-analyze-03 → mdp-profile-02（群体动力数据丰富个体剖面推断）

**质量增强闭环链路**: mdp-enhance-02a(会前触发点设计) → mdp-exec-03(会议执行) → mdp-enhance-01a(评分) → mdp-enhance-01b(诊断) → mdp-enhance-01c(亮点+改进) → mdp-enhance-04(模式优化, ≥3场) → mdp-enhance-02b(触发点优化) → mdp-enhance-02a(改进后设计)

### 数据充分度激活

| 阶段 | 条件 | 激活任务 | 休眠/降质任务 |
|------|------|---------|-------------|
| 冷启动 | 首次使用，0场历史 | 全部D01 + 降质D02(analyze-01-06除跨会议部分) + 降质D03 + D04(profile-01完整, profile-03用单次快照对比) + D05(01a/01b/01c/02a降质/03a/03b) | profile-02/04休眠, analyze-07休眠, analyzed-01/03/05的跨会议部分降质, 04休眠, 02b休眠(无历史01c数据) |
| 浅积累 | 2-5场会议 | 所有D01+D02+D03 + D04(profile-02低置信度激活, profile-03完整, profile-04低置信度激活) + D05(01a/01b/01c/02a增强/02b低置信度/03a/03b/04低置信度) | profile-04高置信度部分休眠, 04高置信度部分休眠 |
| 深积累 | ≥6场会议 | 全部27任务满能力运行 | 无 |

更多组合根据具体任务动态推导。
