# 变更记录(倒序)

## v5.6.0(全链路审计修复:P0×2 / P1×8 / P2×7)

**来源**:外部全链路审计报告(audit-report-2026-09-10.md,17 项发现逐条实证后全部确认,P1-8④ 目录盲区与 T30 重复)。共性根因为"升级时新增一层、旧层引用不随动"的单向棘轮。

- **P0-1** score_prompt.py 第三处位序硬编码消除:改为 `import validate_skill` 引用 `CORE_ATOM_KEYS`(单一真相源),help 文案谎言同步修正;"新增原子无需改脚本"承诺恢复成立。
- **P0-2** depth-adaptation.md 覆盖触发表新增**顶档分支**(位不变-内容增强 / 改调关联原子),iterate.md D4 同步日志格式与调档前置(diff);complete-examples 示例3 即兴处理改挂新规则。
- **P1-1** 组装步数统一"八步"(manifest 标题、routing、usage-guide、SKILL×2 共 5 处);**P1-2** SKILL.md 七维表引用改"manifest 第 8 步(门禁自检)"。
- **P1-3** usage-guide 整体重写:六步路由(含第零步)、28 原子、多族校验、完整目录树(补 benchmark/registry/model-adapters/IR/包协议/资产)。
- **P1-4** SKILL.md 示例3 回链修正(指向 complete-examples 示例3=秒杀系统的真实过程)。
- **P1-5** 门面示例去年份锚("2026"全链路清除,含 case-07 快照与 5 组样本);cases.yaml 12 条新增 `boundary_precheck` 字段,门禁新增 **RB008**(第零步预判结论必须登记)。
- **P1-6** `@lang` 空接口补全:depth-adaptation.md 新增"@lang 处理规则"(zh/en/bilingual 语义 + 与中文标点条款的优先级裁决);SKILL.md 注意事项同步。
- **P1-7** iterate.md D4 补调档前置:先 fingerprint.py diff 评估影响面(与 SKILL.md 路由第 6 步闭环)。
- **P1-8** gen_registry.py 移入 scripts/(ROOT 改 `__file__` 相对定位),registry"由 scripts 下脚本实证生成"声明恢复成立;WHITELIST_TOP 死条目 TODO.md 清理。
- **P2-1** fingerprint.py `canonical()` 对 lang=zh 按缺省归一,裸指纹与 @lang=zh 哈希等价(实测 96d5bcd2f545 一致);自测新增等价性用例。
- **P2-2** 12 份快照 + 5 份样本头部全部注入实测 FP-HASH 行(FP-HASH 死链激活,幂等可重跑)。
- **P2-3** deps 死接口激活:语义定义为"该原子参与的依赖规则编号",9 核心原子按 DEPENDENCY_RULES 实算回填(think-chain=R1,R3 等),gen_registry 携带 deps,门禁新增 **RG006** 反查一致性。
- **P2-4** changelog 登记勘误(MF014 从未实现);manifest 补"信号词归属声明"。
- **P2-5** 门禁条目号跨文档漂移订正 5 处(fingerprint.py FP005→FP003;depth-adaptation FP003→FP004/005/007 族、TB 表述;quality-metrics QL001-QL008 与级别说明)。
- **P2-6** 伪反例重构:原 replace 构造在全 confirmed 后是空操作;现拆为 RB007(删单条快照)+ RB003(confirmed:false+快照存在)两个真实反例,自测增至 9 例。
- **P2-7** depth-adaptation 目录与概览补全(R04/后缀哈希/@lang/LITE 豁免,"三要素"改"多要素体系")。
- 报告文件移出根目录归档至 assets/.workbuddy/,DH005 归零。
- 新增 `references/architecture.md` 全局架构文档:体系分层思维导图(mermaid)、**唯一真相源对照表**(通则:数量/编号/引用性表述只许一处,其余语义名引用)、指纹数据流图、门禁 20 族清单(脚本实证提取,修正此前 14 族的低估)、升级同步检查单(把审计报告发现的"单向棘轮"固化为显式工序)。

## v5.5.0(进阶路线 R03 归档 + R05/R06/R08 v0)

- R03 收口:12 条 benchmark 用例(cases.yaml)全部按 manifest 组装流程产出快照并归档至 `references/benchmark/snapshots/`(B1×3 / B2×3 / B3×3 / B4×3,域覆盖 hr/marketing/education/internet-product/finance/tech/consulting/legal/medical,输出覆盖 text-doc/table/structured-data/chart-desc/slides);每条快照头部 DEPTH 指纹经 fingerprint.py parse 校验、依赖规则 R1-R5 零违反;confirmed 全部置 true,门禁 RB003/RB007 清零。**R08 前置解除。**
- R05 v0:生成 5 组多模型产出样本(`references/benchmark/model-samples/`,同一 case-07 语义载荷按 claude/openai/gemini/deepseek/qwen 五适配器渲染,头部带 @model 后缀);基于样本抽象 **PromptIR 规范 v0**(`references/prompt-ir.md`):IR 字段表(14 字段 × 档位条件)+ 五后端映射表(实证形态差异)+ 一致性不变量(渲染器校验清单)+ v1 迁移路径(脚本化 round-trip 待样本扩充)。
- R06 v0:新增**提示词包协议**(`references/prompt-package.md`):包结构(package.yaml + main.md + subtasks/)、Handoff Schema(task_id/status/output/assumptions/handoff_notes)、DAG 依赖(depends_on 无环)、组包六步流程与最小示例。v0 只定协议不含运行时。
- R08 v0:新增**原子注册中心** `references/registry/atom-registry.yaml`(28 原子,id/type/source/version/description,由脚本从 atoms/ 目录实证生成);为跨 Skill 复用提供机器可读登记。
- 门禁新增三组校验:IR001-IR005(规范章节 + 样本完备性 + 样本头部 @model 指纹)、PK001-PK004(协议章节 + 交接字段 + DAG + 包清单)、RG001-RG005(注册中心与 atoms 目录双向一致 + type 归属核对 + 字段完整性)。
- R09(CLI)维持暂缓:价值 ★★ 且依赖 R05 v1 脚本化,避免在样本未扩齐时固化命令面。
- 批次七(T21-T29)隐匿 bug 修复同批收录:score_prompt None 统一 skip、WHITELIST_TOP 接回 DH005、FP010 依赖规则双真相源门禁、RB007 快照双向校验、CR011、EX004/005 收紧、自测补 encoding。
- 批次八(T30)DH005 目录盲区修复:顶层目录此前不受白名单约束,新增 `assets/` 目录时静默绕过门禁;现顶层目录同受 WHITELIST_TOP 约束,assets/ 入白名单并在资源索引声明,自测新增 rogue_topdir_blocked 破坏性用例(7 用例)。

## v5.4.0(进阶路线 R10:能力边界预判)

- R10:routing-protocol.md 新增"能力边界预判(R10)"节 —— 五类判定:C1 需实时/外部数据、C2 需执行副作用动作、C3 需确定性计算、C4 需运行时编排、C5 超出认知边界。每类给出判定信号与"为什么提示词工程解决不了"。
- 决策树五步 → **六步**:新增**第零步:能力边界预判**,前置到计分之前;命中即走**路由 D**,不产出 DEPTH 指纹。
- 路由 D 处理模板:识别 → 说明限制 → 给 A 降级 / B 转交 / C 拆分 三条路径 → 用户选择后继续。C3 若用户坚持要直接结果,必须标注"未经执行验证"。
- 消除重复定义:边界场景 4(超出认知边界)改为**指向 R10 节的 C5 类**,不再自带规则(唯一真相源);并显式给出 C4 与边界场景 3(超复杂需求)的区分表 —— 前者需循环/状态/回溯,后者只是维度多。
- 门禁新增 BN001-BN007:章节存在、C1-C5 类别齐全、第零步标题标注能力边界、场景 4 必须指向 R10 节、处理模板与 A/B/C 路径、C4 与场景 3 的区分说明(warning)。
- 反向验证(副本破坏测试,6 个断点全拦):删 R10 节→BN002、删 C3 类别→BN003、第零步标题去标记→BN004、删整条第零步标题→BN004、场景 4 不引用→BN005、删处理模板→BN006。
- 自查修正:BN004 初版用 `"第零步" in text` 判断,文档别处提及即蒙混过关(断点 3 漏检)。已收紧为正则定位 `^### 第零步[:：]` 标题行再校验其含"能力边界预判"。**这是本项目第三次踩"存在性检查过宽"的坑(FP004 / BN004 / 同类),值得作为编写门禁的通用禁忌。**

## v5.3.0(进阶路线 R07:指纹 v2)

- R07:新增 `scripts/fingerprint.py`,三个子命令 —— `parse`(解析带后缀指纹并校验合法性)、`hash`(计算规范哈希)、`diff`(逐位差异 + 影响面 + 依赖违规 + 新旧哈希)。
- 后缀语法扩展为三键:`@model`(R02 已建)、`@lang=zh|en|bilingual`、`@tokens=<预算>`(联动 R04)。合法键仅此三种,其余一律拒绝。
- 指纹哈希:规范串 = `[9 位档位]|model=..|lang=..`(后缀按字典序,`@tokens` 排除 —— 预算不是产出特征),取 sha256 前 12 位,写作 `FP-HASH: <12 位>`。用于缓存命中与复现追溯;缓存库依赖 R03 快照归档,当前未启用。
- 指纹 diff:`levels_changed` 逐位给出位序/原子名/升降档,`regenerate_modules` 给出需重生成的模块清单;**存在降档时退出码 3**,供脚本判断需人工确认。
- depth-adaptation.md 原"模型适配后缀(R02)"节升级为"指纹后缀与哈希(R02 / R07)"。
- 门禁新增 FP001-FP009:工具存在性(FP001)、`CORE_ATOM_KEYS` 解析失败(FP002)、工具位序与门禁不一致(FP003)、后缀语法声明行缺失(FP004)、语法行缺某个后缀键(FP005)、哈希规范缺失(FP006)、文档用了未支持后缀(FP007)、**文档中出现的每个 DEPTH 指纹都实测可解析**(FP008,subprocess 调用 fingerprint.py parse)、未发现任何指纹示例(FP009 warning)。
- 反向验证(项目副本破坏测试):工具位序改动→FP003;语法行删 `@tokens`→FP005;删整条语法声明→FP004;文档加非法位数指纹→FP008(+DP017);文档加未知后缀 `@color=`→FP007+FP008。五个断点全部拦截。
- 自查修正:FP004 初版只判断 `@model/@lang/@tokens` 是否在文档中出现,导致删除后缀定义表的行仍能通过(文档别处提及即误判为已定义)。已收紧为**正则定位后缀语法声明行**再逐键检查,并新增 FP004(行缺失)与 FP005(行内缺键)两级。

## v5.2.0(进阶路线 R02:模型适配层)

- R02:新增 `references/model-adapters/`,5 个适配器(claude / openai / gemini / deepseek / qwen),每个含 MODEL-ADAPTER 契约块、结构偏好映射表、必用与禁用写法、注入模块、与档位的交互、质量检查清单。
- 各适配器要点:claude → XML 标签分段、禁用强 JSON Schema;openai → Markdown 标题 + JSON Schema、o-series 撤销显式 CoT;gemini → 全大写指令块 + 编号步骤 + 关键约束首尾复述;deepseek → 中文自然语言 + 显式思维链触发语、禁用刚性 Schema;qwen → 中文 Markdown 三段式、角色段须写满三维。
- 指纹后缀规范:`DEPTH: [d1..d9] @model=<id>`,写于 depth-adaptation.md 新增"模型适配后缀(R02)"节。**正交性原则:后缀只改表达形态,不得改变任何一位档位**,适配器只做段落形态改写与尾部注入两件事。
- composition-manifest.md:组装流程 7 步 → **8 步**(新增第 7 步"模型适配"),新增"模型适配表"。
- 门禁新增 MA001-MA013:契约块(id/target/fingerprint_suffix)、id 与文件名一致、注入模块与判定信号章节、manifest 模型适配表双向登记、文档内 `@model=` 值必须已注册。
- 顺带修复既有解析 bug:`_parse_manifest_tables` 遇到任意 `##` 标题不终止上一个表的收集,导致 manifest 中新增章节的表格被误吞入 outputs 判定表(表现为 MF012 误报)。已改为任何二级标题均终止收集。

## v5.1.0(进阶路线批次六:R01 / R03 / R04)

- R01:新增 `references/quality-metrics.md` 作为七维质量表**可计算子集**的唯一真相源(QL001-QL008,含模糊词、五段齐全度、来源标注率、约束条数与对称性、思考阶段标签、自检项、语境触发词);主观项(专业性/适配性/语气一致性)保留人工。
- R01:新增 `scripts/score_prompt.py`,对产出提示词做静态评分并输出 JSON;阈值**草案未标定**,fail 仅提示不阻断。
- R01:门禁新增 QL001-QL008,校验指标表与评分脚本 `METRICS` 常量逐格一致(文档侧改动未同步脚本即报错)。
- R03:新增 `references/benchmark/cases.yaml`,12 条固定需求集(B1-B4 × 3 域)锁定"需求 → 产出"映射;快照目录 `benchmark/snapshots/` 待人工归档。
- R03:门禁新增 RB001-RB006(cases 缺失/用例数不足/指纹位数不符/快照未确认)。
- R04:`depth-adaptation.md` 新增"档位 Token 基线"节与预算反推公式;门禁新增 TB001-TB004 与 `--token-budget` 参数(输出推荐最高档位,并提示降级后须重跑 R1-R5)。
- 标定记录:QL003 修掉一类误报 —— 任务标题中的纯年份(如"2026年…报告")不再计为需标注来源的数据项;仅具备统计语义(百分比/四位数以上统计量/占比·渗透率·同比等)的行计入。
- 顺带修复:depth-adaptation.md 扩展指南残留"按字母序登记"表述,改为"按组装顺序登记(门禁 DP007 校验三方一致)"。

## v5.0.1(缺陷修复批次,TODO T01-T20)

- T01/T14:位序双轨冲突修复,全链路统一为组装序(9 位,含新增 example-shot 原子),修复示例指纹注释。
- T02:门禁新增 CR010(原子质量清单位号比对)与 DP007(depth-adaptation 位序表逐位比对),消除"34 全绿"盲区。
- T03:新增 MF010-MF014(manifest 判定表与原子目录双向存在性、信号词弱比对)。**勘误(v5.6.0 复核)**:MF014 信号词弱比对从未实现,实际存在为 MF010-013/MF015;信号词以 manifest 判定表为准,原子内"适用判定信号"节为辅助描述(两者当前抽查一致,但无机制保障,见 manifest 声明)。
- T04:新增 DP011(R1-R5 依赖规则对 complete-examples 全部 DEPTH 指纹求值)与 DP012(规则表原子名异常告警);补 R3/R4 示例验证(T18/EX004)。
- T05:删除 LITE-2/3/4 死代码,LITE-1 更名"LITE-1 骨架"并保留锚点;T20 补 LITE 与 D1 组装的判定规则。
- T06:depth-adaptation.md 增补 LITE-1 唯一真相源豁免声明及理由。
- T07:基调映射表降级为速查,判定唯一口径收敛至 routing-protocol.md 计分制;风险信号补齐高专业门槛、技术密集、合规敏感。
- T08:修正 SKILL.md 示例 3 笔误;complete-examples 示例 2 消除 finance 幻觉命中,修正为 internet-product 单域。
- T09:跳过(git 仓库实测已存在)。
- T10:新增 references/usage-guide.md(README 等价物)与 references/changelog.md;LICENSE 待用户确认后补,暂缺。
- T11:frontmatter 新增 version 字段,新增 FM006 校验 SKILL.md 标题/脚本常量三处主版本一致。
- T12:新增 scripts/test_validate_skill.py 门禁自测用例;CI 平台化配置暂缓(沙箱无 CI 挂载点)。
- T13:域信号词消歧,hr 收敛为"员工培训",education 收敛为"培训课程";七维表补对应原子映射列,manifest 组装第 7 步引用之。
- T15:输出原子新增 code-block、structured-data、dialogue、slides 四类并登记判定表。
- T16:域原子新增 medical;routing-protocol 场景 5 联动 medical 原子。
- T17:注意事项补标点规范(中文标点统一,禁中英混排);脚本常量统一。
- T19:假设标注统一"假设:"前缀,四种应用场景明确。
- T20:七维表标注自动核验程度,R01 落地前的过渡标注。

## v5.0.0(初始原子化版本)

- 22 原子库(8 核心 × D1-D4 + 8 域 + 6 输出)、DEPTH 指纹、R1-R5 依赖规则、注册制扩展位、契约门禁。
