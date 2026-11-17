---
workflow: 税费审计
version: 1.0
profession: 审计
output_type: 底稿
risk_level: high
required_inputs:
  - 应交税费明细
  - 各税种纳税申报表
required_capabilities:
  - spreadsheet.read
  - spreadsheet.calculate
optional_capabilities:
  - web.search
  - web.fetch
  - script.execute
external_write: false
mind_write: true
---

# 税费审计

## 触发条件

用户要求：审计应交税费、税金及附加、所得税费用、递延所得税、增值税勾稽、税负分析、纳税申报表核对、税会差异、税费重算、补提所得税时加载。

## 前置条件

必要材料：应交税费明细（分税种）、增值税/企业所得税/附加税等申报表。

推荐材料：税前利润与纳税调整表、递延所得税计算、税收优惠备案、上期审定税费、销项进项台账、完税凭证。

开始前确认：

1. 适用税种、税率与优惠政策；
2. 是否为高新技术企业等特殊税率主体；
3. 增值税一般纳税人还是小规模；
4. 所得税是否已预缴、是否已计提。

涉及具体税率、优惠截止日或文号时，先按 `operations/source_directory.md` 联网核实有效性。

## 专业知识绑定

执行前读取：

- `references/knowledge/tax/tax_core.md`：增值税、企税、个税核心规则；
- `references/knowledge/tax/tax_risk_indicators.md`：税务风险与金税四期；
- `references/knowledge/accounting/accounting_advanced.md`：所得税会计、递延所得税；
- `references/knowledge/audit/audit_procedures.md`：税费循环程序。

## 执行步骤

### 步骤1：税费审定表与勾稽

- 汇总应交税费各明细、税金及附加、所得税费用，与 TB、报表勾稽；
- 生成审定表四栏；
- 借方余额（留抵/预缴）与贷方应交分别列示，不轧差掩盖。

### 步骤2：增值税勾稽与重算

- 销项税与收入勾稽（收入 × 适用税率 vs 账载销项）；
- 进项税与采购、抵扣凭证勾稽；
- 申报表与账载应交增值税核对；
- 关注视同销售、进项转出、免抵退；
- 输出《增值税勾稽表》与差异清单。

### 步骤3：企业所得税重算

- 以税前利润为起点，汇总纳税调整项（业务招待、罚款、加计扣除等）；
- 计算应纳税所得额与应纳所得税；
- 与已计提所得税费用比较；
- 未计提或计提不足的，编制补提调整建议；
- 输出《所得税重算表》。

税前利润 × 适用税率仅为初步测算，必须结合纳税调整，不直接等同应纳税额。

### 步骤4：递延所得税复核

- 识别暂时性差异（减值准备、折旧差异、预计负债等）；
- 复核递延所得税资产/负债确认与计量；
- 递延所得税资产确认关注未来应纳税所得额的支持；
- 输出《递延所得税复核表》。

### 步骤5：税负分析与风险

- 计算增值税税负率、所得税实际税率；
- 与行业参考区间比较；
- 关注税负异常偏低、留抵异常、长期挂账应交税费；
- 输出《税负分析表》与税务风险提示。

### 步骤6：衔接分录测试与其他科目

- 接收 `journal_entry_testing` 的税务群异常凭证；
- 与收入（销项）、采购（进项）、薪酬（个税）科目结论交叉核对；
- 汇总税费例外与调整建议。

## 工具选择与授权

按顺序发现宿主表格/计算能力、已验证 MCP、本机 CLI。政策时效需联网时按官方源核实，不向未知第三方传数据。默认写新文件。工具不可用时退回知识指引，给出勾稽公式、重算模板与税负参考区间。

## 异常处理

| 异常 | 处理 |
|---|---|
| 税率不确定 | 联网核实官方文号，不默认套用 |
| 申报表与账载不符 | 单列差异，查申报或账务错误 |
| 未计提所得税 | 重算并提补提调整，不忽略 |
| 优惠政策到期 | 核实有效期，评估适用性 |
| 留抵长期异常 | 查进项真实性与业务匹配 |
| 数据缺申报表 | 标注证据不足，程序未完成 |

## 复核检查点

统一复核总闸：交付前确认：

- [ ] 税费审定表与 TB、报表勾稽；
- [ ] 借方留抵/预缴与贷方应交未轧差掩盖；
- [ ] 销项与收入、进项与采购勾稽；
- [ ] 申报表与账载核对，差异已查；
- [ ] 所得税经纳税调整重算，非直接税率相乘；
- [ ] 递延所得税确认有依据；
- [ ] 税负分析与行业比较，异常有提示；
- [ ] 涉及税率/优惠已按官方源核实时效；
- [ ] 分录测试税务群异常已回流；
- [ ] 未凭数据直接定性偷漏税；
- [ ] 输出未覆盖源文件。

## 产出物

命名建议：`主体_期间_税费_版本_日期`。

最低验收：税费审定表、增值税勾稽表、所得税重算表、递延所得税复核表、税负分析表齐全且相互勾稽、可回钻。

## 跨 Workflow 协作协议

- 有项目数据底座时，接收并更新 `references/workflows/audit/trial_balance_and_lead_schedules.md` 生成的税费 Lead Schedule，不重复新建；独立运行且无底座时才创建。
- 本流程只输出调整候选，不正式写入审定 TB。候选至少包含 `project_id`、`period`、`entity`、`source_version`、`workpaper_ref`、`candidate_id`、认定、借贷方向与金额、证据状态、建议依据、`source_workflow` 和 `conclusion_owner`；正式过账仅由 `references/workflows/audit/audit_adjustments_and_completion.md` 执行。
- 销项、进项或申报明细需要正式抽样时调用 `references/workflows/audit/audit_sampling.md`；本流程可以提出异常税率、税负或勾稽差异定向项，但不得自行改变正式总体、样本编号和投射口径。
- 销项税与 `references/workflows/audit/receivables_and_revenue.md`、进项税与 `references/workflows/audit/payables_and_purchases.md` 共享 `lead_workflow`、`sample_id`、`evidence_ref`、`cross_reference` 和 `conclusion_owner`。税费流程拥有税额、申报与税会差异结论，交易循环拥有交易发生和截止结论。

## Mind 写入规则

仅在 Mind 已配置且有跨会话价值时写入：

- `01_projects/current.md`：税负水平、补提事项、税务风险；
- `05_learning/judgments.md`：经确认可泛化的税会判断；
- `05_learning/error_log.md`：真实计算或勾稽错误；
- `05_learning/gotchas.md`：真实可复用的税费判断坑。

不写入客户完税凭证、申报明细等敏感数据到跨项目记忆。

---

> 末次更新：2026-07-22 [知识补充] 新建税费审计科目 Workflow，含增值税勾稽、所得税重算、递延所得税与税负分析
