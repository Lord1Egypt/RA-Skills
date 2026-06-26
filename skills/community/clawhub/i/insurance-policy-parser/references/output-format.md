# 保险条款结构化输出格式规范

## 目录
- [概述](#概述)
- [完整JSON结构](#完整json结构)
- [level1-绝对核心字段](#level1-绝对核心字段)
- [level2-对比增强字段](#level2-对比增强字段)
- [提取规则](#提取规则)
- [数据类型转换规则](#数据类型转换规则)
- [示例输出](#示例输出)

## 概述
本文档定义医疗险条款解析的标准JSON输出格式，分为两个优先级：
- **Level 1：绝对核心字段（14个）** - 任何医疗险条款必须明确表述的基础参数
- **Level 2：对比增强字段（18个）** - 体现产品差异化，允许部分产品为null

## 完整JSON结构
```json
{
  "level1_core_fields": {
    "total_annual_limit": null,
    "deductible_amount": null,
    "deductible_unit": null,
    "reimbursement_ratio_with_social_security": null,
    "reimbursement_ratio_without_social_security": null,
    "renewal_guaranteed": null,
    "renewal_guarantee_years": null,
    "premium_adjustment_cap": null,
    "hospital_level_requirement": null,
    "public_hospital_required": null,
    "waiting_period_days": null,
    "inpatient_medical_covered": null,
    "drug_coverage_scope": null,
    "proton_heavy_ion_covered": null
  },
  "level2_enhancement_fields": {
    "deductible_family_shared": null,
    "social_security_offset_allowed": null,
    "special_outpatient_covered": null,
    "outpatient_surgery_covered": null,
    "pre_post_hospital_outpatient_days": null,
    "critical_disease_deductible_zero": null,
    "critical_disease_separate_limit": null,
    "out_of_hospital_drug_covered": null,
    "targeted_drug_covered": null,
    "car_t_covered": null,
    "designated_drug_list_required": null,
    "emergency_hospital_exception": null,
    "overseas_treatment_covered": null,
    "renewal_requires_health_recheck": null,
    "post_stop_transfer_right": null,
    "green_channel_covered": null,
    "claim_direct_billing_available": null,
    "family_plan_available": null
  }
}
```

## Level 1：绝对核心字段（14个）

| 字段名 | 数据类型 | 字段说明 | 示例 |
|--------|----------|----------|------|
| `total_annual_limit` | DECIMAL(15,2) | 年度总赔付限额，保单最高赔付天花板 | 1000000.00 |
| `deductible_amount` | DECIMAL(15,2) | 免赔额金额，被保险人自付门槛 | 0.00 或 10000.00 |
| `deductible_unit` | ENUM | 免赔额单位：年/次/疾病/住院 | "年" 或 "次" |
| `reimbursement_ratio_with_social_security` | DECIMAL(5,4) | 经医保报销后的赔付比例 | 1.0000（表示100%） |
| `reimbursement_ratio_without_social_security` | DECIMAL(5,4) | 未经医保时的赔付比例 | 0.6000（表示60%） |
| `renewal_guaranteed` | BOOLEAN | 是否承诺保证续保 | true 或 false |
| `renewal_guarantee_years` | INT | 保证续保年限 | 6、20、999（终身） |
| `premium_adjustment_cap` | DECIMAL(5,4) | 单次费率上调上限，无限制则为1.0 | 0.3000（表示30%） |
| `hospital_level_requirement` | ENUM | 医院等级要求 | "二级" / "三级" / "二级及以上" / "无限制" |
| `public_hospital_required` | BOOLEAN | 是否仅限公立医院 | true 或 false |
| `waiting_period_days` | INT | 疾病等待期天数 | 30、90、180 |
| `inpatient_medical_covered` | BOOLEAN | 是否保障住院医疗 | true 或 false |
| `drug_coverage_scope` | ENUM | 药品保障范围 | "全部" / "清单内" / "社保目录" / "未明确" |
| `proton_heavy_ion_covered` | BOOLEAN | 是否涵盖质子重离子治疗 | true 或 false |

## Level 2：对比增强字段（18个）

| 字段名 | 数据类型 | 字段说明 | 示例 |
|--------|----------|----------|------|
| `deductible_family_shared` | BOOLEAN | 家庭投保是否共享免赔额 | true 或 false |
| `social_security_offset_allowed` | BOOLEAN | 医保报销是否可抵扣免赔额 | true 或 false |
| `special_outpatient_covered` | BOOLEAN | 是否保障特殊门诊（放化疗/透析等） | true 或 false |
| `outpatient_surgery_covered` | BOOLEAN | 是否保障门诊手术 | true 或 false |
| `pre_post_hospital_outpatient_days` | INT | 住院前后门急诊保障天数 | 30 或 0 |
| `critical_disease_deductible_zero` | BOOLEAN | 重疾是否0免赔 | true 或 false |
| `critical_disease_separate_limit` | BOOLEAN | 重疾是否有独立保额 | true 或 false |
| `out_of_hospital_drug_covered` | BOOLEAN | 是否保障院外购药 | true 或 false |
| `targeted_drug_covered` | BOOLEAN | 是否保障靶向药 | true 或 false |
| `car_t_covered` | BOOLEAN | 是否保障CAR-T治疗 | true 或 false |
| `designated_drug_list_required` | BOOLEAN | 药品是否必须在指定清单内 | true 或 false |
| `emergency_hospital_exception` | BOOLEAN | 紧急情况是否可突破医院等级限制 | true 或 false |
| `overseas_treatment_covered` | BOOLEAN | 是否涵盖海外就医 | true 或 false |
| `renewal_requires_health_recheck` | BOOLEAN | 续保是否需重新健康告知 | true 或 false |
| `post_stop_transfer_right` | BOOLEAN | 停售后是否允许转保其他产品 | true 或 false |
| `green_channel_covered` | BOOLEAN | 是否含就医绿色通道 | true 或 false |
| `claim_direct_billing_available` | BOOLEAN | 是否支持直付服务 | true 或 false |
| `family_plan_available` | BOOLEAN | 是否支持家庭单投保 | true 或 false |

## 提取规则

### 通用原则
1. **准确提取**：忠实于原文，不添加不存在的信息
2. **Level 1 优先**：优先保证14个核心字段的准确性
3. **合理归纳**：对分散的信息进行整合和概括
4. **标注未明**：文档未明确说明的字段使用null表示

### 字段定位技巧

#### 基础信息类
- `waiting_period_days`：查找"等待期"、"观察期"、"免责期"章节
- `renewal_guaranteed` / `renewal_guarantee_years`：查找"续保"、"保证续保"章节
- `premium_adjustment_cap`：查找"费率调整"、"保费上调"相关描述

#### 赔付规则类
- `total_annual_limit`：查找"年度限额"、"保额"、"总保额"
- `deductible_amount` / `deductible_unit`：查找"免赔额"、"起付线"
- `reimbursement_ratio_with_social_security`：查找"经社保报销"、"医保报销后"
- `reimbursement_ratio_without_social_security`：查找"未经社保"、"未使用医保"

#### 医院要求类
- `hospital_level_requirement`：查找"医院等级"、"二级及以上"、"三级医院"
- `public_hospital_required`：查找"公立医院"、"私立医院是否可赔"

#### 保障范围类
- `inpatient_medical_covered`：查找"住院医疗"、"住院费用"
- `drug_coverage_scope`：查找"药品范围"、"药品目录"、"社保内外"
- `proton_heavy_ion_covered`：查找"质子重离子"、"质子治疗"

#### 增值服务类（Level 2）
- `out_of_hospital_drug_covered` / `targeted_drug_covered`：查找"院外购药"、"靶向药"
- `car_t_covered`：查找"CART"、"CAR-T"
- `green_channel_covered`：查找"绿色通道"、"就医绿通"
- `claim_direct_billing_available`：查找"直付"、"直赔"

### 常见关键词映射

#### 免赔额单位
- "每年"、"年度" → "年"
- "每次"、"单次" → "次"
- "每种疾病"、"每病种" → "疾病"
- "每次住院" → "住院"

#### 医院等级
- "二级及二级以上"、"二级及以上" → "二级及以上"
- "三级医院"、"三甲医院" → "三级"
- "二级医院" → "二级"
- "不限医院等级"、"不限" → "无限制"

#### 药品保障范围
- "不限社保目录"、"不限社保" → "全部"
- "清单内药品"、"指定药品" → "清单内"
- "社保目录内"、"医保目录内" → "社保目录"
- 未明确说明 → "未明确"

#### 赔付比例转换
- "100%" → 1.0000
- "80%" → 0.8000
- "60%" → 0.6000
- "30%" → 0.3000

#### 费率调整上限
- "无限制"、"不限" → 1.0
- "不超过30%" → 0.3
- "最高20%" → 0.2

#### 保证续保年限
- "终身"、"不限制" → 999
- "20年" → 20
- "6年" → 6

## 数据类型转换规则

### DECIMAL 类型
- 金额字段（如 `total_annual_limit`）转换为数字，单位为元
  - "100万" → 1000000.00
  - "200万元" → 2000000.00
  - "50万" → 500000.00
- 比例字段转换为0-1之间的小数
  - "100%" → 1.0000
  - "80%" → 0.8000
  - "30%" → 0.3000

### ENUM 类型
- 严格使用枚举值，不得自定义
- 枚举值见各字段定义说明

### BOOLEAN 类型
- 以下表述视为 true：
  - "保障"、"包含"、"涵盖"、"享有"、"支持"、"可"
  - "是"、"有"
- 以下表述视为 false：
  - "不保障"、"不包含"、"不涵盖"、"不享有"、"不支持"、"不可"
  - "否"、"无"、"除外"
- 未明确说明使用 null

### INT 类型
- 天数字段：直接提取数字
- "30天" → 30
- "90天" → 90

## 示例输出

```json
{
  "level1_core_fields": {
    "total_annual_limit": 2000000.00,
    "deductible_amount": 10000.00,
    "deductible_unit": "年",
    "reimbursement_ratio_with_social_security": 1.0000,
    "reimbursement_ratio_without_social_security": 0.6000,
    "renewal_guaranteed": true,
    "renewal_guarantee_years": 20,
    "premium_adjustment_cap": 0.3000,
    "hospital_level_requirement": "二级及以上",
    "public_hospital_required": true,
    "waiting_period_days": 30,
    "inpatient_medical_covered": true,
    "drug_coverage_scope": "全部",
    "proton_heavy_ion_covered": true
  },
  "level2_enhancement_fields": {
    "deductible_family_shared": false,
    "social_security_offset_allowed": true,
    "special_outpatient_covered": true,
    "outpatient_surgery_covered": true,
    "pre_post_hospital_outpatient_days": 30,
    "critical_disease_deductible_zero": true,
    "critical_disease_separate_limit": false,
    "out_of_hospital_drug_covered": true,
    "targeted_drug_covered": true,
    "car_t_covered": true,
    "designated_drug_list_required": true,
    "emergency_hospital_exception": true,
    "overseas_treatment_covered": false,
    "renewal_requires_health_recheck": false,
    "post_stop_transfer_right": true,
    "green_channel_covered": true,
    "claim_direct_billing_available": false,
    "family_plan_available": true
  }
}
```
