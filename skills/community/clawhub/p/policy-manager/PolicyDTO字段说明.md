# PolicyDTO 字段说明

> 基于源码逐一读取生成，字段以实际 Java 源文件为准，不包含任何推测或虚构字段。


---

## 目录

2. [PolicyDTO（保单主对象）](#2-policydto)
3. [PolicyLobDTO（保单产品线）](#3-policylobdto)
4. [PolicyPlanDTO（保单方案）](#4-policylandto)
5. [PolicyPlanClauseDTO（方案条款）](#5-policyplanclausedto)
6. [PolicyPlanClauseExtraDTO（条款扩展）](#6-policyplanclauseextradto)
7. [PolicyPlanClauseLiabilityDTO（条款责任）](#7-policyplanclauseliabilitydto)
8. [PolicyPlanClauseLiabilityExtraDTO（责任扩展）](#8-policyplanclauseliabilityextradto)
9. [PolicyPlanClauseLiabilityInsuredDTO（责任标的）](#9-policyplanclauseliabilityinsureddto)
10. [PolicyPlanClauseLiabilityInsuredExtraDTO（责任标的扩展）](#10-policyplanclauseliabilityinsuredextradto)
11. [PolicyPlanFactorTemplateDTO（方案因子模板）](#11-policyplanfactortemplatedto)
12. [PolicyPlanFactorDTO（方案因子）](#12-policyplanfactordto)
13. [PolicyPlanExtraDTO（方案扩展）](#13-policyplanextradto)
14. [PolicyPlanExtraFromRiskFactorDTO（方案风险要素基类）](#14-policyplanextrafromriskfactordto)
15. [PolicyPlanExtraShortRateDTO（短期费率）](#15-policyplanextrashortratsdto)
16. [PolicyPlanExtraListRiskFactorDTO（列表风险要素）](#16-policyplanextralistrissfactordto)
17. [BaseFactorExtraDTO（基础因子扩展）](#17-basefactorextradto)
18. [BaseOptionFactorDTO（基础可选因子）](#18-baseOptionfactordto)
19. [PolicyCustomerDTO（保单客户基类）](#19-policycustomerdto)
20. [PolicyCustomerPersonDTO（个人客户）](#20-policycustomerpersondto)
21. [PolicyCustomerOrgDTO（企业客户）](#21-policycustomerorydto)
22. [PolicyInsuredPersonDTO（标的人）](#22-policyinsuredpersondto)
23. [PolicyBeneficiaryDTO（受益人）](#23-policybeneficiarydto)
24. [PolicyInsuredObjectDTO（标的物）](#24-policyinsuredobjectdto)
25. [PolicyInsuredAdditionInfoDTO（标的附加属性）](#25-policyinsuredadditioninfodto)
26. [PolicyInsuredTypeFactorDTO（标的类型因子）](#26-policyinsuredtypefactordto)
27. [PolicyLaunderInfoDTO（反洗钱信息）](#27-policylaunderinfodto)
28. [PolicyInvoiceInfoDTO（开票信息）](#28-policyinvoiceinfodto)
29. [PolicySalesInfoDTO（销售信息）](#29-policysalesinfodto)
30. [PolicySalesInfoExtDTO（销售信息扩展）](#30-policysalesinfoextdto)
31. [PolicyAgentSalesmanDTO（代理人业务员）](#31-policyagentsalesmandto)
32. [PolicySalesFeeDTO（销售费用）](#32-policysalesfeedto)
34. [PolicyReinsuranceExtrinfoDTO（再保扩展）](#34-policyreinsuranceextrinfodto)
35. [PolicyCoinsurerDTO（共保人）](#35-policycoinsurerdto)
36. [PolicyCoinsurerFeeDTO（共保费用）](#36-policycoinsuerfeedto)
37. [PolicyPayDTO（缴费信息）](#37-policypaydto)
38. [PolicyPayPlanDTO（缴费计划）](#38-policypaylandto)
39. [PolicyPayPlanPayerDTO（缴费计划付款人）](#39-policypayplandpayerdto)
40. [PolicyAuditRecordDTO（审核意见）](#40-policyauditrecorddto)
41. [PolicyAuditRecordExtraDTO（审核意见扩展）](#41-policyauditrecordextradto)
42. [PolicyEngineerPeriodDTO（工程保障期间）](#42-policyengineerperioddto)
43. [PolicyNoticeDTO（告知信息）](#43-policynoticedto)
44. [PolicyPlateDTO（板块信息）](#44-policylatedto)
45. [PolicySpecialAgreementDTO（特别约定）](#45-policyspecialagreementdto)
46. [PolicyShareDTO（保单共享）](#46-policysharedto)
47. [PolicyShareRelationDTO（共享关联）](#47-policysharerelationdto)
48. [PolicyVasDTO（增值服务）](#48-policyvasdto)
49. [ApsServiceInfoDTO（事故预防服务）](#49-apsserviceinfodto)
51. [PolicyLiabilityPremiumRateConfigDTO（责任费率配置）](#51-policyliabilitypremiumrateconfigdto)

---

## 依赖关系说明

```
PolicyDTO
├─ policyLobList: List<PolicyLobDTO>
│    └─ policyPlanList: List<PolicyPlanDTO>
│         ├─ clauseList: List<PolicyPlanClauseDTO>
│         │    ├─ liabilityList: List<PolicyPlanClauseLiabilityDTO>
│         │    │    ├─ liabilityInsuredList: List<PolicyPlanClauseLiabilityInsuredDTO>
│         │    │    │    └─ extraInfo: PolicyPlanClauseLiabilityInsuredExtraDTO
│         │    │    ├─ planFactorTemplateList: List<PolicyPlanFactorTemplateDTO>
│         │    │    │    └─ planFactorList: List<PolicyPlanFactorDTO>
│         │    │    └─ extraInfo: PolicyPlanClauseLiabilityExtraDTO
│         │    │         └─ calPremiumRateConfigList: List<PolicyLiabilityPremiumRateConfigDTO>
│         │    ├─ planFactorTemplateList: List<PolicyPlanFactorTemplateDTO>
│         │    └─ extraInfo: PolicyPlanClauseExtraDTO
│         ├─ planFactorTemplateList: List<PolicyPlanFactorTemplateDTO>
│         ├─ planNoticeList: List<PolicyNoticeDTO>
│         ├─ planVasList: List<PolicyVasDTO>
│         ├─ planShareList: List<PolicyShareDTO>
│         │    └─ shareRelationList: List<PolicyShareRelationDTO>
│         ├─ planSpecialAgreementList: List<PolicySpecialAgreementDTO>
│         └─ extraInfo: PolicyPlanExtraDTO
│              ├─ extraListRiskFactors: List<PolicyPlanExtraListRiskFactorDTO>
│              └─ extraShortRateDTO: PolicyPlanExtraShortRateDTO
├─ policyHolder: PolicyCustomerDTO
│    ├─ policyCustomerPerson: PolicyCustomerPersonDTO
│    ├─ policyCustomerOrg: PolicyCustomerOrgDTO
│    ├─ launderInfoList: List<PolicyLaunderInfoDTO>
│    └─ additionInfoList: List<PolicyInsuredAdditionInfoDTO>
├─ policyInsurantList: List<PolicyCustomerDTO>  （同上结构）
├─ insuredPersonList: List<PolicyInsuredPersonDTO>
│    ├─ beneficiaryList: List<PolicyBeneficiaryDTO>
│    ├─ insuredObjList: List<PolicyInsuredObjectDTO>
│    │    ├─ additionInfoList: List<PolicyInsuredAdditionInfoDTO>
│    │    └─ insuredTypeFactorList: List<PolicyInsuredTypeFactorDTO>
│    └─ insuredTypeFactorList: List<PolicyInsuredTypeFactorDTO>
├─ insuredObjList: List<PolicyInsuredObjectDTO>
├─ policyInvoice: PolicyInvoiceInfoDTO
├─ policySalesInfo: PolicySalesInfoDTO
│    ├─ agentSalesmanList: List<PolicyAgentSalesmanDTO>
│    └─ salesInfoExt: PolicySalesInfoExtDTO
│         └─ originSalesInfo: PolicyDTO  ← 循环引用
├─ policySalesFeeList: List<PolicySalesFeeDTO>
├─ policySpecialAgreementList: List<PolicySpecialAgreementDTO>
├─ policyShareList: List<PolicyShareDTO>
├─ coinsurerList: List<PolicyCoinsurerDTO>
│    └─ coinsurerFeeList: List<PolicyCoinsurerFeeDTO>
├─ payList: List<PolicyPayDTO>
│    └─ payPlanList: List<PolicyPayPlanDTO>
│         └─ payerList: List<PolicyPayPlanPayerDTO>
├─ auditRecordList: List<PolicyAuditRecordDTO>
│    └─ extra: PolicyAuditRecordExtraDTO
├─ policyEngineerPeriod: PolicyEngineerPeriodDTO
├─ policyFactorTemplateList: List<PolicyPlanFactorTemplateDTO>
├─ policyNoticeList: List<PolicyNoticeDTO>
├─ policyPlateDTO: PolicyPlateDTO
└─ apsServiceInfoDTO: ApsServiceInfoDTO
     └─ projectDTOList: List<ServiceProjectDTO>
```
---

## 2. PolicyDTO

继承自 `PolicyBaseDTO`，保单核心对象。

### 基本信息

| 字段名 | 类型 | 说明 |
|---|---|---|
| id | Long | 主键id（ShardingKey 分库分表键） |
| proposalNo | String | 投保单号，最大长度50 |
| policyNo | String | 保单号，最大长度50 |
| policyVersion | Integer | 保单版本号 |
| parentPolicyId | Long | 父保单id |
| parentPolicyNo | String | 父保单号，最大长度50 |
| quotationNo | String | 询报价单号，最大长度50 |
| tenantNo | String | 渠道商户号，最大长度50 |
| productCode | String | 产品代码，最大长度50 |
| productVersion | String | 产品版本，最大长度20 |
| productName | String | 产品名称 |
| policyCategory | String | 保单类别，最大长度10 |
| productInsuranceCode | String | 险类，最大长度10 |
| policyType | String | 保单类型，最大长度10 |
| indiGroupFlag | String | 个团标志，最大长度10 |
| policyStatus | String | 保单状态，最大长度10 |
| startTime | Date | 保险起期 |
| endTime | Date | 保险止期 |
| signDate | Date | 签单时间 |
| applyTime | Date | 投保时间 |
| operateDate | Date | 录单时间 |
| issueTime | Date | 承保时间 |
| policyEndDate | Date | 终止日期 |
| terminationReason | String | 终止原因代码，最大长度10 |
| uwConclueDate | Date | 核保结论时间 |
| uwConclue | String | 核保结论代码，最大长度10 |
| sumInsured | BigDecimal | 总保险金额 |
| sumPremium | BigDecimal | 总含税保费 |
| sumNetPremium | BigDecimal | 不含税保费 |
| sumSignPremium | BigDecimal | 总签单保费 |
| sumNetSignPremium | BigDecimal | 不含税签单保费 |
| sumTaxFee | BigDecimal | 增值税税额 |
| taxRate | BigDecimal | 增值税税率 |
| coinsFlag | String | 共保标志，最大长度10 |
| jointFlag | String | 联保标识，最大长度10 |
| insuredFlag | String | 记名标志，最大长度10 |
| isPresent | String | 是否赠险，最大长度1 |
| isBatchApply | String | 是否批量投保，最大长度1 |
| isReinsuranceAccept | String | 是否再保分入保单，最大长度1 |
| familyFlag | String | 家庭单标志，最大长度10 |
| resolutionCode | String | 争议解决方式代码，最大长度10 |
| payFlag | String | 见费出单标志，最大长度10 |
| autoTransRenewFlag | String | 自动续保标志，最大长度10 |
| renewFlag | String | 续保标志，最大长度10 |
| jointCoinsFlag | String | 联共保标识，最大长度10 |
| renewTimes | Integer | 续保次数 |
| renewPolicyNo | String | 续保保单号，最大长度50 |
| currency | String | 币种代码，最大长度10 |
| makeCom | String | 出单机构代码，最大长度50 |
| operateSite | String | 签单地点，最大长度100 |
| channelOrderNo | String | 第三方订单号，最大长度50 |
| cardNo | String | 卡单号，最大长度50 |
| emergencyType | String | 紧急程度代码，最大长度10 |
| operateType | String | 录单类型，最大长度10 |
| systemCode | String | 系统来源，最大长度10 |
| remark | String | 备注，最大长度500 |
| operator | String | 录单人（出单人），最大长度32 |
| handler | String | 当前处理人，最大长度32 |
| underwriter | String | 核保人，最大长度32 |
| locker | String | 锁定人，最大长度32 |
| isOriginal | String | 是否是原始保单，最大长度1 |
| arbitrationOrg | String | 劳动仲裁机构 |
| extraInfo | Map\<String, String\> | 扩展信息 |
| policyBizTypeEnum | PolicyBizTypeEnum | 保单场景枚举 |
| productCodes | List\<String\> | 产品代码列表 |
| policyLobList | List\<PolicyLobDTO\> | 保单产品线列表 |
| policyHolder | PolicyCustomerDTO | 保单投保人信息 |
| policyInsurantList | List\<PolicyCustomerDTO\> | 保单被保险人列表（企财类保单） |
| insuredPersonList | List\<PolicyInsuredPersonDTO\> | 保单标的人列表（意健险/雇主责任险） |
| insuredObjList | List\<PolicyInsuredObjectDTO\> | 保单标的物列表 |
| policyInvoice | PolicyInvoiceInfoDTO | 保单开票信息 |
| policySalesInfo | PolicySalesInfoDTO | 保单销售信息 |
| policySalesFeeList | List\<PolicySalesFeeDTO\> | 销售费用信息列表 |
| policySpecialAgreementList | List\<PolicySpecialAgreementDTO\> | 保单特别约定列表 |
| policyShareList | List\<PolicyShareDTO\> | 保单共享信息列表 |
| coinsurerList | List\<PolicyCoinsurerDTO\> | 共保人列表 |
| payList | List\<PolicyPayDTO\> | 保单付款信息列表 |
| auditRecordList | List\<PolicyAuditRecordDTO\> | 审核意见信息列表 |
| policyEngineerPeriod | PolicyEngineerPeriodDTO | 保障期间信息 |
| policyFactorTemplateList | List\<PolicyPlanFactorTemplateDTO\> | 保单限额、免赔列表 |
| policyNoticeList | List\<PolicyNoticeDTO\> | 保单告知列表 |
| policyPlateDTO | PolicyPlateDTO | 板块信息 |
| apsServiceInfoDTO | ApsServiceInfoDTO | 事故预防服务 |

---

## 3. PolicyLobDTO

继承自 `PolicyBaseDTO`，保单产品线信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| productCode | String | 产品代码，最大长度50 |
| productVersion | String | 产品版本，最大长度20 |
| productName | String | 产品名称 |
| productInsuranceCode | String | 险类，最大长度10 |
| productType | String | 产品类型（1-普通，2-建工险），最大长度10 |
| productSubType | String | 产品子类型（1-按工程合同造价，2-按施工建筑面积，3-按被保险人人数），最大长度10 |
| productInfoDef | String | 产品动态字段定义，最大长度65535 |
| productInfo | String | 产品动态字段，最大长度1024 |
| sumInsured | BigDecimal | 保额 |
| premium | BigDecimal | 保费 |
| netPremium | BigDecimal | 不含税保费 |
| signPremium | BigDecimal | 签单保费 |
| netSignPremium | BigDecimal | 不含税签单保费 |
| taxFee | BigDecimal | 增值税税额 |
| shortRateFlag | String | 短期费率标志，最大长度10 |
| shortRate | String | 短期费率，最大长度50 |
| shortRateDesc | String | 短期费率描述（不落库，仅DTO），最大长度36 |
| shortRateTableld | String | 短期费率表id |
| insuredCount | Integer | 被保险人人数 |
| extraInfo | String | 扩展信息，最大长度1024 |
| productPackId | Long | 产品工厂定义的产品Id |
| hasLimitsConfig | String | 产品工厂有限额配置（Y=有配置） |
| hasDeductibleConfig | String | 产品工厂有免赔配置（Y=有配置） |
| policyPlanList | List\<PolicyPlanDTO\> | 方案列表 |

---

## 4. PolicyPlanDTO

继承自 `PolicyBaseDTO`，保单方案信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| lobId | Long | 产品线id |
| serial | String | 序号，最大长度45 |
| planCategory | String | 方案类别，最大长度10 |
| planCategoryName | String | 方案类别名称（同标的大类名称） |
| planCategoryFlag | String | 关联险类标识，最大长度10 |
| planType | String | 方案类型（1-固定方案，2-半固定方案，3-自定义方案），最大长度10 |
| planCode | String | 方案代码，最大长度50 |
| planName | String | 方案名称 |
| planVersion | Integer | 方案版本 |
| originalPlanCode | String | 原始方案代码，最大长度50 |
| originalPlanName | String | 原始方案名称 |
| originalPlanVersion | String | 原始方案版本 |
| premiumCalculateType | String | 保费计算方式（1-按方案总保费，2-按被保人），最大长度10 |
| startOccupationLevel | String | 起始可投保职业类别，最大长度10 |
| endOccupationLevel | String | 截止可投保职业类别，最大长度10 |
| startTime | Date | 保险起期 |
| endTime | Date | 保险止期 |
| startAge | Integer | 起始可投保年龄 |
| startAgeUnit | String | 起始可投保年龄单位，最大长度10 |
| endAge | Integer | 截止可投保年龄 |
| endAgeUnit | String | 截止可投保年龄单位，最大长度10 |
| insuredCount | Integer | 被保险人人数 |
| aoka | BigDecimal | AOKA |
| discountRate | BigDecimal | 折扣率 |
| maxCopies | Integer | 最大可投保份数 |
| copies | Integer | 份数 |
| sumInsured | BigDecimal | 保额 |
| premium | BigDecimal | 保费 |
| signPremium | BigDecimal | 签单保费 |
| perSignPremium | BigDecimal | 每人签单保费 |
| perPremium | BigDecimal | 每份承保保费 |
| netPremium | BigDecimal | 不含税保费 |
| netSignPremium | BigDecimal | 不含税签单保费 |
| taxFee | BigDecimal | 增值税税额 |
| avgMonthSalary | BigDecimal | 平均月薪 |
| extraInfo | PolicyPlanExtraDTO | 扩展信息 |
| clauseList | List\<PolicyPlanClauseDTO\> | 条款列表 |
| planNoticeList | List\<PolicyNoticeDTO\> | 健康告知列表 |
| planVasList | List\<PolicyVasDTO\> | 保障服务列表 |
| planShareList | List\<PolicyShareDTO\> | 方案共享列表 |
| planSpecialAgreementList | List\<PolicySpecialAgreementDTO\> | 保单特别约定列表 |
| planFactorTemplateList | List\<PolicyPlanFactorTemplateDTO\> | 保单方案因子模板列表 |

---

## 5. PolicyPlanClauseDTO

继承自 `PolicyBaseDTO`，保单方案条款信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| clauseCode | String | 条款代码，最大长度50 |
| clauseName | String | 条款名称 |
| clauseCategory | String | 条款一级分类 CD000703，最大长度32 |
| regulatoryReportName | String | 保监报备方案名称 |
| clauseVersion | String | 条款版本号，最大长度50 |
| productClauseId | Long | 产品工厂条款ID |
| riderClauseType | String | 条款类型 CD000817，最大长度4 |
| riskCode | String | 险种代码，最大长度50 |
| reinsuranceRiskCode | String | 再保险种代码，最大长度50 |
| isMain | String | 是否主险，最大长度1 |
| clauseUrl | String | 条款链接，最大长度512 |
| parentClauseCode | String | 父方案条款代码 |
| optionFlag | String | 可选标志，最大长度10 |
| isPresent | String | 是否允许赠险，最大长度1 |
| isIncludeSumInsured | String | 是否计入累计保额，最大长度1 |
| isCanAddPerson | String | 是否可拓展出险人Y/N，最大长度4 |
| extWarrantyPeriod | String | 是否可扩展保证期（Y-是，N-否），最大长度1 |
| isKeyMain | String | 是否关键主险，最大长度1 |
| insuredCategoryCode | String | 标的大类代码，最大长度20 |
| insuredCategoryName | String | 标的大类名称 |
| subInsuredTypeCode | String | 标的附加属性类型代码，最大长度50 |
| dynamicContent | String | 查询工厂定义的条款动态内容，最大长度8192 |
| sumInsured | BigDecimal | 保额 |
| annualPremium | BigDecimal | 年化保费 |
| premium | BigDecimal | 保费 |
| netPremium | BigDecimal | 不含税保费 |
| signPremium | BigDecimal | 签单保费 |
| netSignPremium | BigDecimal | 不含税签单保费 |
| taxRate | BigDecimal | 增值税税率 |
| taxFee | BigDecimal | 增值税税额 |
| isGeneralAdditional | String | 是否为通用附加险，Y/N |
| clauseGroupId | String | 条款组别ID |
| clauseGroupName | String | 条款组别名称 |
| hasLimitsConfig | String | 产品工厂有限额配置 |
| hasDeductibleConfig | String | 产品工厂有免赔配置 |
| extraInfo | PolicyPlanClauseExtraDTO | 扩展信息 |
| liabilityList | List\<PolicyPlanClauseLiabilityDTO\> | 责任列表 |
| planFactorTemplateList | List\<PolicyPlanFactorTemplateDTO\> | 保单方案因子模板列表 |

---

## 6. PolicyPlanClauseExtraDTO

实现 `Serializable`，方案条款扩展对象。

| 字段名 | 类型 | 说明 |
|---|---|---|
| isEditText | String | 是否可编辑条款文本，Y-是，N-否 |
| clauseText | String | 条款文本 |
| originalClauseUrl | String | 可编辑条款原条款文件地址 |
| calculateFlag | String | 保额保费标识：1-有保额有保费，2-无保额无保费，3-有保额无保费，4-无保额有保费 |
| sortNo | Integer | 条款排序序号 |

---

## 7. PolicyPlanClauseLiabilityDTO

继承自 `PolicyBaseDTO`，保单方案条款责任信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| objNo | Integer | 标的序号 |
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| planClauseId | Long | 方案条款id |
| productLiabilityId | Long | 产品工厂责任id |
| liabilityCode | String | 责任代码，最大长度50 |
| liabilityName | String | 责任名称 |
| version | String | 版本号，最大长度50 |
| reinsuranceRiskCode | String | 再保险种代码，最大长度50 |
| isSubLiability | String | 是否是子责任，最大长度1 |
| parentLiabilityCode | String | 父方案条款责任代码 |
| isMain | String | 是否主险，最大长度1 |
| optionFlag | String | 可选标志，最大长度10 |
| isIncludeSumInsured | String | 是否计入累计保额，最大长度1 |
| copies | Integer | 份数 |
| perSumInsured | BigDecimal | 每份保额 |
| perSumInsuredType | String | 每份保额类型，最大长度10 |
| premium | BigDecimal | 保费 |
| maxCopies | Integer | 最大可投保份数 |
| maxDays | Integer | 累计赔付天数 |
| sumInsured | BigDecimal | 保额 |
| annualPremium | BigDecimal | 年化保费 |
| perPremium | BigDecimal | 每份承保保费 |
| premiumConfigType | String | 保费配置类型，最大长度1 |
| perSignPremium | BigDecimal | 每人签单保费 |
| premiumRate | BigDecimal | 费率 |
| signPremium | BigDecimal | 签单保费 |
| netPremium | BigDecimal | 不含税保费 |
| netSignPremium | BigDecimal | 不含税签单保费 |
| taxRate | BigDecimal | 增值税税率 |
| taxFee | BigDecimal | 增值税税额 |
| riskCode | String | 风险小类，最大长度50 |
| copiesPremium | BigDecimal | 份数承保保费 |
| isSpecialRisk | String | 是否特种风险 |
| sumInsuredValueType | String | 保额值类型（1:固定保额\|2:枚举\|3:范围，码表CD000907） |
| sumInsuredEnum | String | 保额（保额值类型为枚举时不为空） |
| salaryTimes | String | 月薪倍数 |
| aggregateDays | String | 累计赔偿天数 |
| rateUnit | String | 费率单位 |
| hasLimitsConfig | String | 产品工厂有限额配置 |
| hasDeductibleConfig | String | 产品工厂有免赔配置 |
| extraInfo | PolicyPlanClauseLiabilityExtraDTO | 扩展信息 |
| planFactorTemplateList | List\<PolicyPlanFactorTemplateDTO\> | 保单方案因子模板列表 |
| liabilityInsuredList | List\<PolicyPlanClauseLiabilityInsuredDTO\> | 责任标的列表 |

---

## 8. PolicyPlanClauseLiabilityExtraDTO

继承自 `PolicyPlanExtraFromRiskFactorDTO`（含 `extraConfigMap`、`extraRiskFactors`），责任层扩展对象。

| 字段名 | 类型 | 说明 |
|---|---|---|
| originalPremiumRate | BigDecimal | 原始费率值 |
| premiumConfigType | String | 保费计算配置 |
| calPremiumRateConfigList | List\<PolicyLiabilityPremiumRateConfigDTO\> | 责任费率配置信息列表 |
| premiumBaseOnMainClause | String | 是否与主险保费相关 |

---

## 9. PolicyPlanClauseLiabilityInsuredDTO

继承自 `PolicyBaseDTO`，保单方案标的信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| objNo | Integer | 标的序号 |
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| planClauseId | Long | 方案条款id |
| planLiabilityId | Long | 方案责任id |
| insuredCategoryCode | String | 标的大类代码，最大长度20 |
| insuredCategoryName | String | 标的大类名称 |
| insuredTypeCode | String | 标的类别代码，最大长度20 |
| insuredTypeName | String | 标的类别名称 |
| insuredCode | String | 标的名称代码，最大长度20 |
| insuredName | String | 标的名称 |
| relRiskFactorCode | String | 关联风险要素代码，最大长度50 |
| relRiskFactorValue | String | 关联风险要素值，最大长度50 |
| sumInsuredConfirmType | String | 保额确认方式，最大长度20 |
| isIncludeSumInsured | String | 是否计入累计保额（N:否\|Y:是），最大长度1 |
| perSumInsured | BigDecimal | 每份保额 |
| perSumInsuredType | String | 每份保额类型（1:固定金额\|2:范围\|3:份数\|4:日津贴\|5:倍月薪\|6:每车每份\|7:每座每份），最大长度10 |
| premiumRate | BigDecimal | 费率 |
| sumInsured | BigDecimal | 保额 |
| copies | Integer | 份数 |
| maxCopies | Integer | 最大可投保份数 |
| maxDays | Integer | 累计赔付天数 |
| copiesPremium | BigDecimal | 份数承保保费 |
| optionFlag | String | 可选标志，最大长度10 |
| perPremium | BigDecimal | 每份承保保费 |
| perSignPremium | BigDecimal | 每人签单保费 |
| premium | BigDecimal | 保费 |
| signPremium | BigDecimal | 签单保费（承保保费×折扣率） |
| netPremium | BigDecimal | 不含税保费 |
| netSignPremium | BigDecimal | 不含税签单保费 |
| annualPremium | BigDecimal | 年化保费 |
| taxRate | BigDecimal | 增值税税率 |
| taxFee | BigDecimal | 增值税税额 |
| totalPremium | BigDecimal | 总承保保费 |
| totalSignPremium | BigDecimal | 总签单保费 |
| sumInsuredValueType | String | 保额值类型（1:固定保额\|2:枚举\|3:范围，码表CD000907） |
| sumInsuredEnum | String | 保额（保额值类型为枚举时不为空） |
| salaryTimes | String | 月薪倍数 |
| aggregateDays | String | 累计赔偿天数 |
| premiumCategory | String | 保费分类（1-固定保费，2-固定费率） |
| premiumConfigType | String | 保费类型，码表CD002057 |
| rateUnit | String | 费率单位 |
| productCode | String | 产品代码 |
| extraInfo | PolicyPlanClauseLiabilityInsuredExtraDTO | 扩展信息 |

---

## 10. PolicyPlanClauseLiabilityInsuredExtraDTO

继承自 `PolicyPlanClauseLiabilityExtraDTO`（含其父类所有字段），责任标的层扩展对象。

| 字段名 | 类型 | 说明 |
|---|---|---|
| originalPremiumRate | BigDecimal | 原始费率值（本层覆盖） |
| mainInsuredId | Long | 主联责任标的id |
| premiumConfigType | String | 保费计算配置（本层覆盖） |
| calPremiumRateConfigList | List\<PolicyLiabilityPremiumRateConfigDTO\> | 责任费率配置信息列表（本层覆盖） |
| premiumBaseOnMainClause | String | 是否与主险保费相关（本层覆盖） |

---

## 11. PolicyPlanFactorTemplateDTO

继承自 `PolicyBaseDTO`，保单方案因子模板信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| relObjType | String | 关联对象类型（1-保单,2-产品线,3-方案,4-条款,5-责任,6-子责任,7-模板），最大长度10 |
| relObjId | Long | 关联对象id |
| insuredTypeCode | String | 标的类别代码，最大长度20 |
| insuredCode | String | 标的名称代码，最大长度20 |
| insuredName | String | 标的名称 |
| templateType | String | 模板类型（1-限额模版，2-免赔模版），最大长度10 |
| templateCode | String | 模板代码，最大长度50 |
| templateContent | String | 模板内容，最大长度1024 |
| canEdit | String | 是否可编辑，最大长度1 |
| planType | String | 方案类型（1-固定方案,2-半固定方案,3-自定义方案） |
| isRequired | String | 是否必选（Y/N） |
| salesArea | String | 销售区域（如：全国、地方） |
| salesOrgs | String | 销售机构列表 |
| relObjCode | String | 关联对象code |
| serialNo | int | 排序序号 |
| keySerialNo | int | 关键字排序 |
| planFactorList | List\<PolicyPlanFactorDTO\> | 方案因子列表 |

---

## 12. PolicyPlanFactorDTO

继承自 `PolicyBaseDTO`，保单方案因子信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| relObjType | String | 关联对象类型（1-保单,2-产品线,3-方案,4-条款,5-责任,6-子责任,7-模板），最大长度10 |
| relObjId | Long | 关联对象id |
| factorType | String | 因子类型（1-费率因子\|2-规则因子\|3-限额因子\|4-免赔因子\|6-附加因子\|7-标的要素），最大长度10 |
| factorCode | String | 因子代码，最大长度50 |
| factorName | String | 因子名称 |
| factorValueType | String | 因子值类型（1-字符串、2-非负整数数字、3-非负数字等），最大长度10 |
| factorValue | String | 因子值，最大长度50 |
| originalFactorValue | String | 产品工厂定义的因子值，最大长度255 |
| factorValueName | String | 因子值名称 |
| originalConvertValue | String | 多币种时原产品工厂金额与保单币种金额映射 |
| factorMoney | BigDecimal | 因子金额 |
| templateContent | String | 模板内容 |
| factorDataType | String | 因子值显示（1-固定值，2-枚举值，3-范围值） |

---

## 13. PolicyPlanExtraDTO

继承自 `PolicyPlanExtraFromRiskFactorDTO`（含 `extraConfigMap`、`extraRiskFactors`），保单方案信息扩展字段对应的对象。

| 字段名 | 类型 | 说明 |
|---|---|---|
| extraListRiskFactors | List\<PolicyPlanExtraListRiskFactorDTO\> | 方案列表风险要素集合 |
| planTableColumnList | List\<BaseFactorExtraDTO\> | 方案表头列集合（为空时只展示条款责任固定字段） |
| extraShortRateDTO | PolicyPlanExtraShortRateDTO | 固定/半固定方案层的短期费率标志集合（自定义方案为空） |
| productExtraFactorMap | Map\<String, String\> | 产品层的扩展因子key-value |

---

## 14. PolicyPlanExtraFromRiskFactorDTO

实现 `Serializable`，保单方案扩展风险要素的基类。

| 字段名 | 类型 | 说明 |
|---|---|---|
| extraConfigMap | Map\<String, Object\> | 额外的配置信息（暂定前端渲染需要） |
| extraRiskFactors | List\<BaseFactorExtraDTO\> | 方案风险要素信息 |

---

## 15. PolicyPlanExtraShortRateDTO

实现 `Serializable`，短期费率信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| shortRateTypes | List\<String\> | 短期费率类型列表 |
| shortRateTableIds | List\<String\> | 短期费率表id列表 |

---

## 16. PolicyPlanExtraListRiskFactorDTO

继承自 `PolicyPlanExtraFromRiskFactorDTO`（含 `extraConfigMap`、`extraRiskFactors`），列表风险要素。

| 字段名 | 类型 | 说明 |
|---|---|---|
| labelId | - | 标签id |
| labelName | - | 标签名称 |
| quoteRequired | - | 投保必填 |
| proposalRequired | - | 投保必填 |
| extraListRiskDataFactors | List\<List\<BaseFactorExtraDTO\>\> | 列表风险要素数据 |

---

## 17. BaseFactorExtraDTO

继承自 `BaseOptionFactorDTO`，基础的因子扩展对象。

| 字段名 | 类型 | 说明 |
|---|---|---|
| labelType | String | 标签类型（见 RiskFactorTypeEnum） |
| labelName | String | 标签名称 |
| isAmount | String | 是否金额类因子，Y/N |
| factorCode | String | 因子code |
| factorName | String | 因子name |
| factorValue | Object | 因子对应的值（可能是具体值\|对象\|数组对象） |
| sortNo | Integer | 顺序 |
| repeatFlag | String | 是否是参与判重因子标志，Y-是，N-否 |

---

## 18. BaseOptionFactorDTO

`BaseFactorExtraDTO` 的父类，基础因子值可操作类型。

| 字段名 | 类型 | 说明 |
|---|---|---|
| factorDataType | String | 因子值显示：1-输入框，2-范围，3-枚举 |
| factorValueList | List\<Object\> | 因子值的操作范围 |
| factorDataValueType | String | 因子数据类型（如：字符串、数值、日期类型等） |
| factorUnitCode | String | 因子值的单位 |
| factorDefaultData | String | 因子默认值 |
| factorAccuracy | Integer | 数值精度 |
| isFillIn | String | 是否必须填写，Y-是，N-否（已废弃） |
| isChange | String | 是否可编辑，Y-是，N-否 |
| quoteRequired | String | 询价必填 |
| proposalRequired | String | 投保必填 |
| originalConvertValue | List\<PolicyPlanFactorConvertDTO\> | 多币种时原产品工厂金额与保单币种金额映射 |
| attribute | String | 产品工厂配置属性信息（JSON存储） |
| multipleSelection | String | 多选标识 |
| factorUnitCodeList | List\<String\> | 因子单位列表 |

---

## 19. PolicyCustomerDTO

继承自 `PolicyBaseDTO`，保单客户信息表（投保人/被保险人基类）。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| userNo | String | 客户编号，最大长度50 |
| type | String | 客户类型（见 CustomerTypeEnum），最大长度10 |
| role | String | 客户角色，最大长度10 |
| relationToAppnt | String | 与投保人关系，最大长度10 |
| isInsurant | String | 是否被保人标志，最大长度1 |
| relationToEnginContract | String | 工程合同关系，最大长度10 |
| relationToEngtractName | String | 工程合同关系扩展名称 |
| name | String | 名称（被保险人姓名/投保人名称） |
| englishName | String | 英文名称 |
| alias | String | 别名，最大长度50 |
| certType | String | 证件类型，最大长度10 |
| certNo | String | 证件号码，最大长度255 |
| certStartDate | Date | 证件有效起期 |
| certEndDate | Date | 证件有效止期 |
| phone | String | 固定电话 |
| mobile | String | 手机号码，最大长度255 |
| email | String | 邮箱 |
| nationality | String | 民族代码 码表CD000005，最大长度10 |
| nativeplace | String | 国籍代码 码表CD000832，最大长度10 |
| province | String | 省代码，最大长度10 |
| city | String | 市代码，最大长度10 |
| county | String | 县/区代码，最大长度10 |
| address | String | 详细地址 |
| postCode | String | 邮编，最大长度20 |
| launderRisk | String | 洗钱风险（1-低,2-中,3-高），最大长度10 |
| payMethod | String | 缴费方式（1-现金,2-转账），最大长度10 |
| startTime | Date | 保险起期 |
| endTime | Date | 保险止期 |
| policyEndDate | Date | 终止日期 |
| benefitType | String | 受益人类型 |
| extraInfo | Map\<String, String\> | 扩展信息（见 CustomerExtraInfoEnum），最大长度1024 |
| policyCustomerPerson | PolicyCustomerPersonDTO | 个人信息 |
| policyCustomerOrg | PolicyCustomerOrgDTO | 企业信息 |
| launderInfoList | List\<PolicyLaunderInfoDTO\> | 反洗钱信息列表 |
| endoChangeFlag | String | 批改操作标识（见 EndoChangeFlagEnum） |
| openId | String | openId |
| unionId | String | unionId |
| productCode | String | 产品Code |
| businessOrgCode | String | 业务归属机构 |
| additionInfoList | List\<PolicyInsuredAdditionInfoDTO\> | 标的附加属性列表 |

---

## 20. PolicyCustomerPersonDTO

继承自 `PolicyCustomerDTO`，保单个人客户信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| customerId | Long | 用户id |
| gender | String | 性别（0-未知，1-男性，2-女性，9-未说明），最大长度10 |
| birthday | Date | 出生日期（格式 yyyy-MM-dd） |
| age | Integer | 年龄 |
| socialInsuFlag | String | 是否有社保（N:否\|Y:是），最大长度10 |
| socialInsuNo | String | 社保登记号，最大长度50 |
| smokeFlag | String | 吸烟标志（N:否\|Y:是），最大长度10 |
| monthSalary | BigDecimal | 月工资 |
| salary | BigDecimal | 个人年收入 |
| stature | BigDecimal | 身高(cm) |
| avoirdupois | BigDecimal | 体重(kg) |
| marriage | String | 婚姻状况代码（10-未婚,20-已婚,30-丧偶,40-离婚,90-未说明），最大长度10 |
| marriageDate | Date | 结婚日期 |
| pyLastName | String | 姓拼音 |
| pyFirstName | String | 名拼音 |
| degree | String | 学历代码 码表CD000006，最大长度10 |
| occupationLevel | String | 职业等级，最大长度10 |
| occupationCategory | String | 职业大类，最大长度10 |
| occupationType | String | 职业分类，最大长度10 |
| occupationCode | String | 职业代码（工种），最大长度10 |
| occupationName | String | 职业名称 |
| extraInfo | Map\<String, String\> | 扩展信息（见 CustomerPersonExtraInfoEnum），最大长度1024 |

---

## 21. PolicyCustomerOrgDTO

继承自 `PolicyCustomerDTO`，保单单位客户信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| customerId | Long | 用户id |
| registMoney | BigDecimal | 注册资本 |
| corporation | String | 法人，最大长度50 |
| businessType | String | 行业分类代码 码表CD000861，最大长度10 |
| orgNature | String | 单位性质代码 码表CD000013，最大长度10 |
| orgType | String | 单位类型代码 码表CD000777，最大长度10 |
| businessScope | String | 经营范围，最大长度100 |
| linkerName | String | 联系人姓名 |
| linkerGender | String | 联系人性别，最大长度10 |
| linkerPhone | String | 联系人固定电话 |
| linkerMobile | String | 联系人移动电话，最大长度255 |
| linkerPosition | String | 联系人职位代码，最大长度10 |
| linkerNativeplace | String | 联系人国籍代码 码表CD000832，最大长度10 |
| linkerProvince | String | 联系人省代码，最大长度10 |
| linkerCity | String | 联系人市代码，最大长度10 |
| linkerCounty | String | 联系人县/区代码，最大长度10 |
| linkerAddress | String | 联系人详细地址 |
| linkerEmail | String | 联系人邮箱 |
| foundDate | Date | 成立日期 |
| extraInfo | Map\<String, String\> | 扩展信息（见 CustomerOrgExtraInfoEnum），最大长度1024 |

---

## 22. PolicyInsuredPersonDTO

继承自 `PolicyCustomerPersonDTO`（再继承 `PolicyCustomerDTO`），保单标的人（意健险/雇主责任险被保险人）。

| 字段名 | 类型 | 说明 |
|---|---|---|
| userNo | String | 客户编号 |
| planId | Long | 方案id |
| planCode | String | 方案code |
| originalPlanId | Long | 原始方案id |
| originalPlanCode | String | 原始方案code |
| proposalVoucherNo | String | 投保凭证号 |
| voucherNo | String | 凭证号 |
| renewFlag | String | 续保标志 |
| renewTimes | Integer | 续保次数 |
| renewPolicyNo | String | 续保保单号 |
| sumInsured | BigDecimal | 总保险金额 |
| totalPremium | BigDecimal | 总含税保费 |
| totalSignPremium | BigDecimal | 总签单保费 |
| planAnnualPremium | BigDecimal | 方案年化保费 |
| planAnnualSignPremium | BigDecimal | 方案年化签单保费 |
| planRealPremium | BigDecimal | 方案实际保费 |
| planRealSignPremium | BigDecimal | 方案实际签单保费 |
| holderCustomerId | Long | 投保人客户id |
| relationToMainInsured | String | 与主被保人关系 |
| mainPersonId | Long | 主被保人id |
| mainPerson | PolicyInsuredPersonDTO | 主被保人信息（自引用） |
| position | String | 职位 |
| benefitType | String | 受益人类型 |
| copies | Integer | 份数 |
| dsFromType | String | 数据来源类型 |
| dsFromNo | String | 数据来源编号 |
| premiumFactorCode1 | String | 保费因子代码1 |
| premiumFactorValue1 | String | 保费因子值1 |
| premiumFactorCode2 | String | 保费因子代码2 |
| premiumFactorValue2 | String | 保费因子值2 |
| premiumFactorCode3 | String | 保费因子代码3 |
| premiumFactorValue3 | String | 保费因子值3 |
| premiumFactorCode4 | String | 保费因子代码4 |
| premiumFactorValue4 | String | 保费因子值4 |
| premiumFactorCode5 | String | 保费因子代码5 |
| premiumFactorValue5 | String | 保费因子值5 |
| beneficiaryInfoList | List\<PolicyBeneficiaryDTO\> | 受益人信息列表 |
| additionInfoList | List\<PolicyInsuredAdditionInfoDTO\> | 附加属性信息列表 |
| endoChangeFlag | String | 批改操作标识 |
| premiumDetail | String | 保费明细 |
| policySince | Date | 保险起期 |

---

## 23. PolicyBeneficiaryDTO

继承自 `PolicyCustomerPersonDTO`（再继承 `PolicyCustomerDTO`），受益人信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| insuredPersonId | Long | 被保险人id |
| relationToInsured | String | 与被保人关系 |
| benefitSerialNo | Integer | 受益顺序号 |
| percentOfBenefit | BigDecimal | 受益比例 |

---

## 24. PolicyInsuredObjectDTO

继承自 `PolicyBaseDTO`，保单标的物信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| planId | Long | 方案id |
| planCode | String | 方案code |
| oneId | String | 唯一标识 |
| proposalVoucherNo | String | 投保凭证号 |
| voucherNo | String | 凭证号 |
| premiumFactorCode1 | String | 保费因子代码1 |
| premiumFactorValue1 | String | 保费因子值1 |
| premiumFactorCode2 | String | 保费因子代码2 |
| premiumFactorValue2 | String | 保费因子值2 |
| premiumFactorCode3 | String | 保费因子代码3 |
| premiumFactorValue3 | String | 保费因子值3 |
| premiumFactorCode4 | String | 保费因子代码4 |
| premiumFactorValue4 | String | 保费因子值4 |
| premiumFactorCode5 | String | 保费因子代码5 |
| premiumFactorValue5 | String | 保费因子值5 |
| sumInsured | BigDecimal | 总保险金额 |
| totalPremium | BigDecimal | 总含税保费 |
| totalSignPremium | BigDecimal | 总签单保费 |
| planAnnualPremium | BigDecimal | 方案年化保费 |
| planAnnualSignPremium | BigDecimal | 方案年化签单保费 |
| planRealPremium | BigDecimal | 方案实际保费 |
| planRealSignPremium | BigDecimal | 方案实际签单保费 |
| insurantCustomerId | Long | 被保险人客户id |
| insurantCustomerName | String | 被保险人名称 |
| insuredPersonId | Long | 标的人id |
| insuredCategoryCode | String | 标的大类代码 |
| insuredCategoryName | String | 标的大类名称 |
| insuredTypeCode | String | 标的类别代码 |
| insuredTypeName | String | 标的类别名称 |
| insuredCode | String | 标的代码 |
| insuredName | String | 标的名称 |
| isMain | String | 是否主标的 |
| startTime | Date | 保险起期 |
| endTime | Date | 保险止期 |
| policyEndDate | Date | 终止日期 |
| copies | Integer | 份数 |
| dsFromType | String | 数据来源类型 |
| dsFromNo | String | 数据来源编号 |
| originalPlanId | Long | 原始方案id |
| originalPlanCode | String | 原始方案code |
| extraInfo | JSONObject | 扩展信息 |
| insuredTypeInfo | JSONObject | 标的类型信息（不序列化，hidden） |
| endoChangeFlag | String | 批改操作标识 |
| premiumDetail | String | 保费明细 |
| insurantName | String | 被保险人姓名 |
| insurantCertType | String | 被保险人证件类型 |
| insurantCertNo | String | 被保险人证件号 |
| insurantGender | String | 被保险人性别 |
| insurantBirthday | Date | 被保险人出生日期 |

---

## 25. PolicyInsuredAdditionInfoDTO

继承自 `PolicyBaseDTO`，标的附加属性信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| planId | Long | 方案id |
| subInsuredTypeCode | String | 附加属性类型代码 |
| subInsuredTypeName | String | 附加属性类型名称 |
| oneId | String | 唯一标识 |
| policyInsuredTypeFactorList | List\<PolicyInsuredTypeFactorDTO\> | 标的类型因子列表 |
| insuredRelationId | Long | 标的关联id |
| insuredRelationType | String | 标的关联类型 |

---

## 26. PolicyInsuredTypeFactorDTO

实现 `Serializable`，标的类型因子。

| 字段名 | 类型 | 说明 |
|---|---|---|
| id | Long | id |
| packageInsuredTypeId | Long | 标的类型id |
| checkbox | String | 是否选中 |
| factorCode | String | 因子代码 |
| factorName | String | 因子名称 |
| factorType | String | 因子类型 |
| factorDataType | String | 因子数据类型 |
| factorDefault | String | 因子默认值 |
| factorDataValueType | String | 因子数据值类型 |
| factorUnitCode | String | 因子单位代码 |
| factorAccuracy | Integer | 精度 |
| isFillIn | String | 是否必填（已废弃） |
| isBuiltIn | String | 是否内置 |
| attribute | String | 属性 |
| factorValue | String | 因子值 |
| quoteRequired | String | 询价必填 |
| proposalRequired | String | 投保必填 |
| repeat | String | 是否重复 |
| sortNo | Integer | 排序号 |

---

## 27. PolicyLaunderInfoDTO

继承自 `PolicyBaseDTO`，反洗钱信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| customerId | Long | 客户id |
| userNo | String | 客户编号 |
| customerType | String | 客户类型 |
| type | String | 类型 |
| name | String | 姓名/名称 |
| certType | String | 证件类型 |
| certNo | String | 证件号码 |
| certStartDate | Date | 证件有效起期 |
| certEndDate | Date | 证件有效止期 |
| extraInfo | String | 扩展信息 |
| province | String | 省代码 |
| city | String | 市代码 |
| county | String | 县/区代码 |
| address | String | 详细地址 |

---

## 28. PolicyInvoiceInfoDTO

继承自 `PolicyBaseDTO`，保单开票信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| invoiceType | String | 发票类型 |
| taxpayerType | String | 纳税人类型 |
| taxpayerNo | String | 纳税人识别号 |
| taxpayerMobile | String | 纳税人手机号 |
| taxpayerRegistAddress | String | 纳税人注册地址 |
| bankCode | String | 开户银行代码 |
| bankName | String | 开户银行名称 |
| branchBankCode | String | 开户支行代码 |
| bankAccNo | String | 银行账号 |
| receiverName | String | 收件人姓名 |
| receiverMobile | String | 收件人手机号 |
| receiverEmail | String | 收件人邮箱 |
| receiverProvince | String | 收件人省代码 |
| receiverCity | String | 收件人市代码 |
| receiverCounty | String | 收件人县/区代码 |
| receiverAddress | String | 收件人详细地址 |

---

## 29. PolicySalesInfoDTO

继承自 `PolicyBaseDTO`，保单销售信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| relObjType | String | 关联对象类型 |
| relObjId | Long | 关联对象id |
| businessOrgCode | String | 业务归属机构代码 |
| businessOrgName | String | 业务归属机构名称 |
| businessType1 | String | 业务类型1（直接/分入） |
| businessType2 | String | 业务类型2（直销/代理/经纪） |
| businessType3 | String | 业务类型3（团队代码） |
| businessType4 | String | 业务类型4（专业化渠道代码） |
| businessType5 | String | 业务类型5 |
| businessType6 | String | 业务类型6 |
| salesmanCode | String | 业务员代码 |
| salesmanName | String | 业务员名称 |
| salesmanCertType | String | 业务员证件类型 |
| salesmanCertNo | String | 业务员证件号 |
| salesmanBusinessCertNo | String | 业务员从业资格证号 |
| agreementCode | String | 协议代码 |
| agreementName | String | 协议名称 |
| subAgreementCode | String | 子协议代码 |
| subAgreementName | String | 子协议名称 |
| agentCode | String | 代理人代码 |
| agentName | String | 代理人名称 |
| agentCertType | String | 代理人证件类型 |
| agentCertNo | String | 代理人证件号 |
| agentBusinessCertNo | String | 代理人从业资格证号 |
| agentSalesmanCode | String | 代理人业务员代码 |
| agentSalesmanName | String | 代理人业务员名称 |
| agentSalesmanCertType | String | 代理人业务员证件类型 |
| agentSalesmanCertNo | String | 代理人业务员证件号 |
| unifiedSocialCreditCode | String | 统一社会信用代码 |
| extraInfo | PolicySalesInfoExtDTO | 扩展信息 |

---

## 30. PolicySalesInfoExtDTO

实现 `Serializable`，销售信息扩展字段。

| 字段名 | 类型 | 说明 |
|---|---|---|
| agreementCode | String | 协议代码 |
| subAgreementCode | String | 子协议代码 |
| cooperPlatform | String | 合作平台 |
| incrementRate | BigDecimal | 增量费率 |
| feeRateMax | BigDecimal | 最大费率 |
| feeRateMin | BigDecimal | 最小费率 |
| businessLine | String | 业务线 |
| businessType | String | 业务类型 |
| businessClassification | String | 业务分类 |
| newBusinessClassification | String | 新业务分类 |
| calcBusinessClassification | String | 计算业务分类 |
| businessNature | String | 业务性质 |
| salesmanRatio | BigDecimal | 业务员比例 |
| businessSmallCode | String | 业务小类代码 |
| businessSmallName | String | 业务小类名称 |
| group | String | 组别 |
| policyResourceConfigDTO | PolicyResourceConfigDTO | 保单资源配置 |
| quotePolicySalesFeeInfoDTO | PolicySalesFeeInfoDTO | 询价保单销售费用信息 |
| productGroupResourceConfigMap | Map | 产品组资源配置映射 |
| productGroupQuotePolicySalesFeeInfoMap | Map | 产品组询价销售费用映射 |
| productGroupPolicySalesFeeInfoMap | Map | 产品组销售费用映射 |
| businessCenterCode | String | 业务中心代码 |
| businessCenterName | String | 业务中心名称 |
| bankCategoryCode | String | 银行类别代码 |
| bankSecondCategoryCode | String | 银行二级类别代码 |
| bankBranchContent | String | 银行支行内容 |
| customerSupportFee | BigDecimal | 客户支持费 |
| salesStaffAllowance | BigDecimal | 销售人员津贴 |
| customerServiceValue2 | BigDecimal | 客户服务价值2 |
| costRate | BigDecimal | 成本率 |
| originSalesInfo | PolicyDTO | **原始保单销售信息（与 PolicyDTO 存在循环引用，慎用）** |
| businessRiskManagementFee | BigDecimal | 业务风险管理费 |
| businessOperationFee | BigDecimal | 业务运营费 |
| agentPattern | String | 代理模式 |
| agentSalesman | PolicyAgentSalesmanDTO | 代理人业务员信息 |

---

## 31. PolicyAgentSalesmanDTO

实现 `Serializable`，代理人业务员信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| agentSalesmanId | Long | 代理人业务员id |
| agentSalesmanCode | String | 代理人业务员代码 |
| agentSalesmanName | String | 代理人业务员名称 |
| agentSalesmanCredentialsNo | String | 代理人业务员资质证号 |
| agentSalesmanCertType | String | 代理人业务员证件类型 |
| agentSalesmanCertNo | String | 代理人业务员证件号 |
| agentSalesmanType | String | 代理人业务员类型 |
| agentSalesmanGender | String | 代理人业务员性别 |
| agentSalesmanBirthday | Date | 代理人业务员出生日期 |
| agentPattern | String | 代理模式 |
| practitionerName | String | 从业人员名称 |

---

## 32. PolicySalesFeeDTO

继承自 `PolicyBaseDTO`，销售费用信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| relObjType | String | 关联对象类型 |
| relObjId | Long | 关联对象id |
| feeTypeCode | String | 费用类型代码 |
| feeTypeName | String | 费用类型名称 |
| feeRate | BigDecimal | 费率 |
| netFeeRate | BigDecimal | 不含税费率 |
| taxRate | BigDecimal | 税率 |
| fee | BigDecimal | 费用 |
| netFee | BigDecimal | 不含税费用 |
| feeRateMax | BigDecimal | 最大费率 |
| feeRateMin | BigDecimal | 最小费率 |
| taxFreeRate | BigDecimal | 免税费率 |
| inputTax | BigDecimal | 进项税 |
| outputTax | BigDecimal | 销项税 |
| isMainAgent | String | 是否主代理 |
| agentCode | String | 代理人代码 |
| agentName | String | 代理人名称 |
| isPremiumIncludeTax | String | 是否含税保费 |
| riskCode | String | 风险代码 |
| productCode | String | 产品代码 |
| clauseCode | String | 条款代码 |
| clauseName | String | 条款名称 |
| canChange | String | 是否可修改 |
| changeComment | String | 修改备注 |
| extraInfo | String | 扩展信息 |
| beforeFee | BigDecimal | 修改前费用 |
| beforeNetFee | BigDecimal | 修改前不含税费用 |
| beforeTaxRate | BigDecimal | 修改前税率 |
| beforeFeeRate | BigDecimal | 修改前费率 |

---

## 34. PolicyReinsuranceExtrinfoDTO

实现 `Serializable`，再保扩展信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| originalOutMdept | String | 原始分出机构 |
| outMdept | String | 分出机构 |
| reinsDate | Date | 再保日期 |
| reinsType | String | 再保类型 |
| businessRegion | String | 业务区域 |
| businessSource | String | 业务来源 |
| itemName | String | 项目名称 |
| originalCurrency | String | 原始币种 |
| lossContent | String | 损失内容 |
| taxRate | BigDecimal | 税率 |
| originalRate | BigDecimal | 原始费率 |
| brokerageTaxRate | BigDecimal | 经纪费税率 |
| brokerageTax | BigDecimal | 经纪费税额 |
| differentDIC | String | 差异DIC |
| otherRate | BigDecimal | 其他费率 |

---

## 35. PolicyCoinsurerDTO

继承自 `PolicyBaseDTO`，共保人信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| bizType | String | 业务类型 |
| bizId | Long | 业务id |
| agreementCode | String | 协议代码 |
| coinsCode | String | 共保人代码 |
| coinsName | String | 共保人名称 |
| coinsRole | String | 共保角色 |
| coinsType | String | 共保类型 |
| coinsRate | BigDecimal | 共保比例 |
| bizNo | String | 业务号 |
| isIssue | String | 是否出单 |
| proceduresPayType | String | 手续费支付类型 |
| feeTaxRate | BigDecimal | 手续费税率 |
| isAgentFee | String | 是否代收手续费 |
| coinsSumInsured | BigDecimal | 共保保额 |
| coinsPremium | BigDecimal | 共保保费 |
| isMainCoinsurer | String | 是否主共保人 |
| isMainClaimer | String | 是否主理赔人 |
| payeeName | String | 收款人名称 |
| bankCode | String | 银行代码 |
| bankAccNo | String | 银行账号 |
| bankName | String | 银行名称 |
| issuerCode | String | 出单人代码 |
| issuerName | String | 出单人名称 |
| currency | String | 币种 |
| isInit | String | 是否初始化 |
| isMainSales | String | 是否主销售 |
| isPremium | String | 是否收取保费 |
| issuerId | Long | 出单人id |
| collectionPremium | BigDecimal | 代收保费 |
| commission | BigDecimal | 佣金 |
| fullCommission | BigDecimal | 满期佣金 |
| isPass | String | 是否通过 |
| unifiedSocialCreditCode | String | 统一社会信用代码 |
| extraInfo | String | 扩展信息 |
| coinsurerFeeList | List\<PolicyCoinsurerFeeDTO\> | 共保费用列表 |
| policySalesInfo | PolicySalesInfoDTO | 保单销售信息 |

---

## 36. PolicyCoinsurerFeeDTO

继承自 `PolicyBaseDTO`，共保费用信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| coinsurerId | Long | 共保人id |
| feeType | String | 费用类型 |
| feeRate | BigDecimal | 费率 |
| feeAmount | BigDecimal | 费用金额 |
| feeTaxRate | BigDecimal | 税率 |
| netFeeAmount | BigDecimal | 不含税费用 |
| feeTax | BigDecimal | 税额 |
| feePaymentType | String | 费用支付类型 |
| isPremiumIncludeTax | String | 是否含税保费 |
| extraInfo | Map\<String, String\> | 扩展信息 |
| beforeFeeAmount | BigDecimal | 修改前费用金额 |
| beforeNetFeeAmount | BigDecimal | 修改前不含税费用 |

---

## 37. PolicyPayDTO

继承自 `PolicyBaseDTO`，保单缴费信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| bizType | String | 业务类型 |
| bizId | Long | 业务id |
| relObjType | String | 关联对象类型 |
| relObjId | Long | 关联对象id |
| payCurrency | String | 缴费币种 |
| exchangeRate | BigDecimal | 汇率 |
| sumInsured | BigDecimal | 保险金额 |
| premium | BigDecimal | 含税保费 |
| netPremium | BigDecimal | 不含税保费 |
| feeTax | BigDecimal | 税额 |
| feeTaxRate | BigDecimal | 税率 |
| signPremium | BigDecimal | 签单保费 |
| netSignPremium | BigDecimal | 不含税签单保费 |
| payFrequency | String | 缴费频率 |
| payNo | String | 缴费号 |
| payGraceDays | Integer | 宽限期天数 |
| unionPay | String | 联合缴费标志 |
| extraInfo | String | 扩展信息 |
| billingCycle | String | 账期 |
| advancePremium | BigDecimal | 预收保费 |
| payPlanList | List\<PolicyPayPlanDTO\> | 缴费计划列表 |

---

## 38. PolicyPayPlanDTO

继承自 `PolicyBaseDTO`，缴费计划信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| payId | Long | 缴费id |
| feeSerialNo | Integer | 费用序号 |
| feeType | String | 费用类型 |
| planDate | Date | 计划日期 |
| planPayDate | Date | 计划缴费日期 |
| planFeeRate | BigDecimal | 计划费率 |
| planFee | BigDecimal | 计划费用 |
| paidFee | BigDecimal | 已付费用 |
| payStatus | String | 缴费状态 |
| paidDate | Date | 实际缴费日期 |
| isOffset | String | 是否冲销 |
| extraInfo | String | 扩展信息 |
| payPlanPayerList | List\<PolicyPayPlanPayerDTO\> | 缴费计划付款人列表 |

---

## 39. PolicyPayPlanPayerDTO

继承自 `PolicyBaseDTO`，缴费计划付款人信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| payPlanId | Long | 缴费计划id |
| payerId | Long | 付款人id |
| payRate | BigDecimal | 付款比例 |
| payAmount | BigDecimal | 付款金额 |
| payNetAmount | BigDecimal | 不含税付款金额 |
| payTax | BigDecimal | 税额 |
| paidFee | BigDecimal | 已付费用 |
| payType | String | 付款类型 |
| payStatus | String | 付款状态 |
| paidDate | Date | 实际付款日期 |
| payOrderNo | String | 付款订单号 |
| payTradeNo | String | 付款交易号 |
| actualPayerName | String | 实际付款人名称 |
| extraInfo | String | 扩展信息 |
| serialNo | String | 序列号 |
| paySubjectType | String | 付款主体类型 |
| sameWithHolder | String | 是否与投保人相同 |
| payerType | String | 付款人类型 |
| relationToAppnt | String | 与投保人关系 |
| payerName | String | 付款人名称 |
| payerCertType | String | 付款人证件类型 |
| payerCertNo | String | 付款人证件号 |
| bankCode | String | 银行代码 |
| bankAccName | String | 银行账户名称 |
| bankAccNo | String | 银行账号 |
| bankMobile | String | 银行预留手机号 |
| bankBranchCode | String | 支行代码 |
| bankBranchName | String | 支行名称 |
| bankProvince | String | 银行省代码 |
| bankCity | String | 银行市代码 |
| payerOrPayee | String | 付款方或收款方 |
| paymentPlatform | String | 付款平台 |
| accountName | String | 账户名称 |
| weChatAccount | String | 微信账号 |
| isPublic | String | 是否公账 |
| abstractNo | String | 摘要号 |
| paymentChannel | String | 支付渠道 |
| isRefundedToOriginal | String | 是否原路退款 |

---

## 40. PolicyAuditRecordDTO

继承自 `PolicyBaseDTO`，审核意见信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| bizType | String | 业务类型 |
| bizId | Long | 业务id |
| auditType | String | 审核类型 |
| afterDays | Integer | 宽限天数 |
| afterEndDate | Date | 宽限止期 |
| sumReplaceRate | BigDecimal | 替换费率合计 |
| attachmentOpinionList | List\<String\> | 附件意见列表 |
| auditCode | String | 审核结论代码 |
| auditContent | String | 审核内容 |
| auditAction | String | 审核动作 |
| auditor | String | 审核人 |
| extraInfo | PolicyAuditRecordExtraDTO | 扩展信息 |

---

## 41. PolicyAuditRecordExtraDTO

实现 `Serializable`，审核意见扩展信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| remark | String | 备注 |

---

## 42. PolicyEngineerPeriodDTO

继承自 `PolicyBaseDTO`，工程保险保障期间信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| installStartTime | Date | 安装期起期 |
| installEndTime | Date | 安装期止期 |
| commissioningStartTime | Date | 试车期起期 |
| commissioningEndTime | Date | 试车期止期 |
| guaranteeStartTime | Date | 保证期起期 |
| guaranteeEndTime | Date | 保证期止期 |
| constructStartTime | Date | 施工期起期 |
| constructEndTime | Date | 施工期止期 |
| projectStartTime | Date | 工程期起期 |
| projectEndTime | Date | 工程期止期 |
| installStartTimeAndEndTime | String | 安装期起止期（合并展示） |
| commissioningStartTimeAndEndTime | String | 试车期起止期（合并展示） |
| guaranteeStartTimeAndEndTime | String | 保证期起止期（合并展示） |
| constructStartTimeAndEndTime | String | 施工期起止期（合并展示） |
| engineeringType | String | 工程类型 |
| waterRelatedEngineerinGroportion | BigDecimal | 涉水工程占比 |
| tunnelEngineerinGroportion | BigDecimal | 隧道工程占比 |

---

## 43. PolicyNoticeDTO

继承自 `PolicyBaseDTO`，保单告知信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| planId | Long | 方案id |
| relObjType | String | 关联对象类型 |
| relObjId | Long | 关联对象id |
| noticeCode | String | 告知代码 |
| noticeName | String | 告知名称 |
| noticeContent | String | 告知内容 |
| noticeType | String | 告知类型 |
| noticeObject | String | 告知对象 |
| noticePosition | String | 告知位置 |
| labelCode | String | 标签代码 |
| labelName | String | 标签名称 |
| sortNo | Integer | 排序号 |
| planType | String | 方案类型 |

---

## 44. PolicyPlateDTO

实现 `Serializable`，板块信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id |
| plan | String | 方案 |
| isOverallBusiness | String | 是否整体业务 |
| overallProtocolNo | String | 整体协议号 |
| biddingBusiness | String | 招标业务 |
| agricultureFlag | String | 农业标志 |
| techInsurance | String | 科技保险 |
| threeAgriculture | String | 三农标志 |
| isRemoteBusiness | String | 是否远程业务 |
| newCitizenSign | String | 新市民标志 |
| isPackageBusiness | String | 是否套餐业务 |
| greenInsurance | String | 绿色保险 |
| specificBusiness | String | 特定业务 |
| isBankMortgage | String | 是否银行抵押 |
| outCode | String | 外部代码 |
| goodsCode | String | 货物代码 |
| planCode | String | 方案代码 |
| interPlatform | String | 交互平台 |
| interBusinessChannel | String | 交互业务渠道 |
| selfBusiness | String | 自营业务 |
| thirdPartyNetwork | String | 第三方网络 |
| handleBusiness | String | 经办业务 |
| handleFee | BigDecimal | 经办费用 |
| channelSubClass | String | 渠道子类 |
| referrerNo | String | 推荐人编号 |
| referrerName | String | 推荐人名称 |
| referrerPhone | String | 推荐人电话 |
| bankMortgage | String | 银行抵押 |
| technologyEnterprise | String | 科技企业 |
| technologyDomain | String | 科技领域 |
| governmentBusiness | String | 政府业务 |
| largeCommerceRisk | String | 大商贸险 |

---

## 45. PolicySpecialAgreementDTO

继承自 `PolicyBaseDTO`，保单特别约定信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| relObjType | String | 关联对象类型（1-保单,2-产品,3-方案,4-条款,5-责任,6-子责任,7-模板），最大长度10 |
| relObjId | Long | 关联对象id |
| code | String | 特约代码，最大长度50 |
| name | String | 特约名称 |
| content | String | 特约内容，最大长度5000 |
| type | String | 特约类型（0:固定,1:半固定-可编辑,2:可编辑,3:半固定-参数），最大长度10 |
| labelCode | String | 标签代码，最大长度50 |
| labelName | String | 标签名称 |
| sortNo | Integer | 排序号 |
| planType | String | 方案类型（1-固定方案,2-半固定方案,3-自定义方案） |

---

## 46. PolicyShareDTO

继承自 `PolicyBaseDTO`，保单共享信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planCodes | String | 方案code（多个以,分隔） |
| planIds | String | 方案id（多个以,分隔），最大长度50 |
| shareLevel | String | 共享层级（liability-责任层，subLiability-责任因子层），最大长度20 |
| shareType | String | 共享类型（1-共享保额,2-共享免赔,3-公共保额,4-共享限额），最大长度10 |
| shareDimension | String | 共享维度（1-家庭,2-保单,3-个人,4-多人），最大长度10 |
| shareRelations | String | 共享关系（多个以,分隔，1-主被保人,2-附属被保人,3-配偶,4-子女,5-父母），最大长度100 |
| shareAmount | BigDecimal | 共享金额 |
| isEditable | String | 是否可编辑，最大长度1 |
| remark | String | 备注，最大长度255 |
| shareRelationList | List\<PolicyShareRelationDTO\> | 保单共享关联列表 |
| planNames | String | 方案名称（逗号分割） |
| liabilityNames | String | 责任名称（逗号分割） |

---

## 47. PolicyShareRelationDTO

继承自 `PolicyBaseDTO`，保单共享关联信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| planCode | String | 方案code |
| shareId | Long | 共享id |
| planLiabilityId | Long | 方案责任id |
| planLiabilityCode | String | 方案责任code |
| factorId | Long | 因子id |

---

## 48. PolicyVasDTO

继承自 `PolicyBaseDTO`，保单增值服务信息表。

| 字段名 | 类型 | 说明 |
|---|---|---|
| policyId | Long | 保单id（ShardingKey） |
| planId | Long | 方案id |
| relObjType | String | 关联对象类型，最大长度10 |
| relObjId | Long | 关联对象id |
| serviceCode | String | 服务code，最大长度100 |
| serviceName | String | 服务名称 |
| parentServiceCode | String | 父服务code，最大长度100 |
| serviceMode | String | 服务方式，最大长度100 |
| serviceNum | String | 服务次数，最大长度100 |
| serviceDesc | String | 服务说明，最大长度255 |
| serviceUrl | String | 服务地址，最大长度255 |
| allowEditing | String | 是否可编辑，最大长度1 |
| sortNo | Integer | 排序号 |
| insuranceType | String | 健康保险产品类别，最大长度10 |

---

## 49. ApsServiceInfoDTO

实现 `Serializable`，事故预防服务信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| isVaApsProject | String | 是否自愿放弃事故预防服务 |
| isApsProject | String | 是否有事故预防服务项目 |
| apsRatio | BigDecimal | 约定事故预防服务非比例 |
| serviceTime | Date | 客户指定服务时间 |
| serviceContractNumber | String | 服务合同打印份数 |
| originalNumber | String | 正本份数 |
| duplicateNumber | String | 副本份数 |
| PartyAOriginalNumber | String | 甲方正本份数 |
| PartyADuplicateNumber | String | 甲方副本份数 |
| PartyBOriginalNumber | String | 乙方正本份数 |
| PartyBDuplicateNumber | String | 乙方副本份数 |
| projectDTOList | List\<ServiceProjectDTO\> | 服务项目集合 |

---

## 51. PolicyLiabilityPremiumRateConfigDTO

实现 `Serializable`，责任费率配置信息。

| 字段名 | 类型 | 说明 |
|---|---|---|
| rateUnit | String | 费率单位 |
| rateInputType | String | 费率输入类型 |
| rateValue | BigDecimal | 费率值 |
| rateRange | DataRangeDTO\<BigDecimal\> | 费率范围 |

---
