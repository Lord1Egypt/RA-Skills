---
workflow: 审计项目与整套底稿编制总流程
version: 1.0
profession: 审计
output_type: 底稿
risk_level: high
required_inputs:
  - 本期未审试算平衡表
  - 上期审定数或上期审计报告
  - 本期财务报表及附注
  - 审计期间、主体、适用准则与报告目的
required_capabilities:
  - spreadsheet.read
  - spreadsheet.calculate
  - spreadsheet.write
  - evidence.index
optional_capabilities:
  - visualization.generate
  - script.execute
external_write: false
mind_write: true
---

# 审计项目与整套底稿编制总流程

## 触发条件

用户要求编制整套审计底稿、启动审计项目、组织底稿框架、或统筹多个科目程序时加载：做一套底稿、审计底稿框架、整套工作底稿、审计项目初始化、编现场底稿、底稿归整、审计执行统筹。

仅询问某一个科目或某一项专项程序时，直接加载对应专项 Workflow，不必启动总控。仅询问概念时读取 `references/knowledge/audit/` 相关文件直接回答。

## 前置条件

必要材料：

- 本期未审试算平衡表（TB）；
- 上期审定数或上期审计报告；
- 本期财务报表（资产负债表、利润表、现金流量表、所有者权益变动表）及附注；
- 审计期间、被审计主体、适用会计准则、报告目的与预期意见类型。

推荐材料：总账与明细账、完整序时账、科目余额明细、事务所底稿模板、上期底稿、组织架构与股权结构、纳税申报表、银行对账单、主要合同台账。

开始前必须确认或记录：

1. 被审计主体、报告期间、合并还是单体；
2. 适用准则（企业会计准则 / 小企业会计准则 / 其他）；
3. 报告目的（法定审计 / 专项 / 尽调 / 内部）；
4. 底稿模板与索引编号规则；
5. 输出位置与是否允许生成文件；
6. 数据完整性与保密要求。

资料不齐不阻塞框架搭建，但必须生成资料缺口清单，并在缺资料的科目底稿上标明"待补充证据，程序未完成"。

## 专业知识绑定

执行前读取：

- `references/knowledge/audit/audit.md`：审计准则体系与报告；
- `references/knowledge/audit/audit_procedures.md`：六阶段、实质性程序、报表填列、重分类、截止；
- `references/knowledge/audit/audit_if_lines.md`：审计判断与复盘。

按需读取 `references/knowledge/audit/internal_control.md`、`references/knowledge/audit/journal_entry_analytics.md` 及各科目/专项 Workflow。

本 Workflow 只负责编排和汇总，不替代现场程序、函证、监盘和最终审计意见。任何未实际实施的程序不得表述为已完成。

## Workflow 所有权与数据契约

| 数据对象/职责 | 唯一主责 Workflow | 其他 Workflow 的权限 |
|---|---|---|
| TB 标准化、科目映射、Lead Schedule 骨架 | `references/workflows/audit/trial_balance_and_lead_schedules.md` | 只读主数据；科目 Workflow 更新本循环程序结果，不另建重复底座 |
| 重要性、风险参数、项目级初步分析 | `references/workflows/audit/materiality_and_risk_assessment.md` | 引用风险 ID 与参数；科目 Workflow 只做科目级钻取 |
| 异常分录线索 | `references/workflows/audit/journal_entry_testing.md` | 作为定向选样来源，不直接认定错报 |
| 抽样总体、样本编号与投射结果 | `references/workflows/audit/audit_sampling.md` | 专项 Workflow 执行样本程序并回填结果，不自行改变样本口径 |
| 控制描述、穿行与控制测试结论 | `references/workflows/audit/internal_controls_and_walkthroughs.md` | 风险评估和专项 Workflow 引用控制 ID，不重复描述同一控制 |
| 科目程序结果与调整候选 | 对应科目 Workflow | 只能提出候选，不得正式过入审定 TB |
| 正式调整过账、最终审定 TB、未更正错报 | `references/workflows/audit/audit_adjustments_and_completion.md` | 其他 Workflow 不得覆盖或并行维护最终审定数 |
| 项目索引、资料缺口、交付完整性 | `references/workflows/audit/audit_engagement_workpapers.md` | 专项回传状态和底稿索引 |

跨 Workflow 传递至少使用：`project_id`、`period`、`entity`、`source_version`、`workpaper_ref`。调整候选另含 `candidate_id`、认定、金额、借贷方向、证据状态；共享样本另含 `sample_id`、`lead_workflow`、`evidence_ref`、`cross_reference`、`conclusion_owner`。

同一交易跨循环测试时只设一个主测试底稿。其他 Workflow 引用同一 `sample_id` 和证据索引，只补充本循环判断，不重新取样；确需扩大样本时必须记录新增原因。

## 执行步骤

### 步骤1：项目初始化与底稿骨架

- 建立项目档案：主体、期间、准则、报告目的、项目组、关键日期；
- 按模板生成底稿索引结构（A 类：计划与风险；B 类：完成与报告；C 类及以后：各科目实质性底稿）；
- 建立交叉索引规则与命名规范；
- 输出《底稿索引总表》和《项目基本信息表》。

降级：无模板时采用通用事务所索引结构，并向用户说明可替换。

### 步骤2：资料清单与缺口管理

- 生成标准资料需求清单（按科目和阶段）；
- 比对已提供资料，标记已收到、缺失、待更新；
- 缺口按对审计结论的影响分级；
- 输出《资料清单与缺口表》，全程滚动更新。

不得在缺关键资料时假装已获取，也不得据缺失数据下确定性结论。

### 步骤3：调度数据底座

调用 `references/workflows/audit/trial_balance_and_lead_schedules.md`：

- 导入未审 TB 与上期审定数；
- 检查借贷平衡；
- 科目映射到报表项目；
- 生成各科目审定表（Lead Schedule）骨架；
- 完成 TB、报表、明细账初步勾稽。

验收：未审数与报表可勾稽；差异均有说明。数据底座不成立前，不进入后续实质性程序。

### 步骤4：调度重要性与风险评估

调用 `references/workflows/audit/materiality_and_risk_assessment.md`：

- 计算整体重要性、实际执行重要性、明显微小错报临界值；
- 财务趋势与比率分析；
- 识别重要账户、认定与特别风险；
- 生成风险—认定—程序矩阵。

风险矩阵是后续所有科目程序的导航，必须先完成再展开细节测试。

### 步骤4A：按审计策略调度内控了解与控制测试

需要了解关键流程、拟依赖控制或执行内控审计时，调用 `references/workflows/audit/internal_controls_and_walkthroughs.md`：

- 将风险 ID、账户和认定传入，接收唯一 `control_id`、流程描述、穿行记录与控制结论；
- 设计有效性、实施状态与运行有效性分开评价，穿行测试不替代整个期间的运行有效性测试；
- 控制不可靠或证据不足时，回传步骤4更新控制风险和风险应对矩阵；
- 只做必要控制了解且不拟依赖时，记录了解结果，不机械增加控制测试。

### 步骤4B：建立项目级抽样治理

任何专项程序需要正式抽样时，调用 `references/workflows/audit/audit_sampling.md`：

- 风险评估与专项 Workflow 提供审计目标、认定、总体来源和参数；
- `references/workflows/audit/audit_sampling.md` 统一维护 `population_id`、正式样本口径、`sample_id`、可复现选择信息和投射结果；
- 科目或内控 Workflow 执行样本程序并拥有专业结论，不另行编号或重复取样；
- 定向高风险项目、100% 检查项目与代表性样本分开标识，不把定向选取冒充统计抽样。

### 步骤5：调度分录测试并回流分析性程序结果

- 分析性程序已在步骤4 `references/workflows/audit/materiality_and_risk_assessment.md` 步骤3 实施，本步骤只引用其结果，不重复实施；
- 有序时账时调用 `references/workflows/audit/journal_entry_testing.md`：筛出异常凭证、罕见科目组合，形成定向选样候选和风险分层输入；正式总体与样本编号仍由 `references/workflows/audit/audit_sampling.md` 维护；
- 将分析性程序识别的异常波动与分录测试的异常凭证，按业务群共同回流到对应科目程序（采购→应付、销售→应收与收入、生产→存货成本、资产→固定资产、税务→税费）。

### 步骤6：调度科目实质性程序

按重要账户和风险等级，逐个调用可用的科目 Workflow 或按 `references/knowledge/audit/audit_procedures.md` 通用程序执行：

- 每个科目：更新既有 Lead Schedule、执行明细测试、抽样、截止、重算与勾稽；正式抽样使用步骤4B建立的统一样本；
- 记录程序、样本、例外与结论；
- 未实施的现场程序（函证、监盘、访谈、原件检查）单列为待办，标明责任人。

降级：暂无专属科目 Workflow 时，用 `references/knowledge/audit/audit_procedures.md` 的科目程序清单执行，并说明使用的是通用程序。

### 步骤7：调度调整与完成阶段

调用 `references/workflows/audit/audit_adjustments_and_completion.md`：

- 汇总审计调整与重分类分录；
- 编制已更正、未更正错报汇总表；
- 与重要性比较，评价错报影响；
- 检查报表与附注勾稽；
- 汇总未决事项、复核问题与审计结论。

### 步骤8：底稿完整性与复核检查

- 检查索引与交叉索引完整、指向有效；
- 检查每张底稿有编制人、复核痕迹占位、日期、数据来源；
- 检查未审数—调整数—审定数三栏贯通；
- 检查所有"待补充""未实施"事项已进入缺口或待办清单；
- 输出《底稿完整性检查表》和《项目待办与复核问题清单》。

## 工具选择与授权

按顺序发现能力：宿主原生表格/文档能力 → 已验证的 MCP 数据能力 → 本机 Python/PowerShell CLI。

不得把某个工具写成唯一实现。能力不足时退回知识指引模式，提供索引结构、底稿模板、公式和检查清单，并说明哪些未实际生成。

读取用户提供的本地资料属于必要操作。上传第三方、写入外部系统、覆盖源文件、批量改账、删除数据前必须单独确认。所有底稿默认写入新文件，不改动原始账表和报表。

## 异常处理

| 异常 | 处理 |
|---|---|
| 未审数与报表不符 | 单列差异，查映射或过账错误，未查清前不进入细节测试 |
| 上期审定数缺失 | 用未审数并标注"期初未审定"，评估对期初余额程序的影响 |
| 合并与单体混用 | 明确报告层级，分开处理，不混算 |
| 准则不明确 | 请用户确认适用准则，不默认套用 |
| 科目 Workflow 缺失 | 用通用程序执行并说明降级 |
| 资料严重不足 | 输出缺口清单，只做可执行部分，不虚构结论 |
| 重复执行 | 版本化输出，不覆盖既有底稿 |

## 复核检查点

统一复核总闸：工具执行成功不等于审计完成。交付前逐项确认：

- [ ] 主体、期间、准则、报告目的已明确；
- [ ] 底稿索引结构完整、交叉索引有效；
- [ ] 未审数、调整数、审定数三栏贯通且可勾稽；
- [ ] 重要性和风险评估已完成并驱动了科目程序；
- [ ] 异常分录、分析性程序结果已回流到相关科目；
- [ ] 未实施的现场程序（函证/监盘/访谈/原件）已单列待办，未被表述为已完成；
- [ ] 调整与未更正错报已汇总并与重要性比较；
- [ ] 报表与附注勾稽已检查；
- [ ] 资料缺口和复核问题清单齐全；
- [ ] 无未经证据支持的审计意见或舞弊定性；
- [ ] 输出未覆盖源文件，敏感数据未传往未知第三方。

## 产出物

底稿命名建议：`主体_期间_审计底稿_版本_日期`，各科目按索引编号归档。

最低验收标准：

- 底稿索引总表、项目信息表、资料缺口表齐全；
- 数据底座、风险评估、科目程序、完成阶段各有对应底稿；
- 每张底稿可回钻数据来源；
- 未实施程序和数据限制已披露；
- 审计结论以已实施程序和已获证据为界，不越界。

## Mind 写入规则

仅在 Mind 已配置且确有跨会话价值时写入：

- `01_projects/current.md`：主体、期间、准则、当前阶段、已完成与待办、输出路径；
- `01_projects/user_prefs.md`：用户确认的底稿模板与输出偏好，不记录客户敏感数据；
- `04_outputs/`：底稿交付物索引；
- `05_learning/judgments.md`：经确认、可泛化的审计判断；
- `05_learning/error_log.md`：真实的数据或工具错误；
- `05_learning/gotchas.md`：真实发生且可复用的判断错误。

不得把客户完整账套、报表、人员姓名、银行账号或未脱敏底稿写入跨项目记忆。

---

> 末次更新：2026-07-22 [知识补充] 新建审计整套底稿编制总控 Workflow，统筹数据底座、风险评估、分录测试、科目程序与完成阶段
