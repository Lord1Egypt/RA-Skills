---
name: Insurance Industry Bidding Expert
description: AI-powered insurance bidding expert for China market — covers the complete insurance bid lifecycle including solvency disclosure (C-ROSS Rules II 2024), reinsurance arrangements, NFRA compliance, policy clause comparison, risk reserve explanations, and 2026 procurement law changes. Built for insurance companies, brokers, and insurtech companies. Keywords: insurance bid, group insurance bid, solvency, reinsurance, NFRA compliance, China insurance, 招投标法修订, 团险投标, 保险标书撰写, C-ROSS合规, 再保险安排, 银保监会, 政府采购, 电子投标, 标书生成, 废标检查, 保费报价, 条款比对.
slug: insurance-bidding-pro
version: "5.0.0"
---

# Insurance Industry Bidding Expert (Insurance Bidding Pro) / 保险行业投标专家

> **English:** AI-powered insurance bidding expert — the definitive vertical skill for insurance companies, brokers, and insurtech companies participating in China government and corporate procurement bids. Covers solvency disclosure (C-ROSS), reinsurance arrangements, CBIRC regulatory compliance, policy clause comparison, and risk reserve explanations. Unique to this skill: insurance-specific bid modules that generic tools cannot provide.
>
> **中文:** 保险行业投标专家——保险公司、保险经纪公司、保险科技企业参与招标的必备垂直工具。覆盖偿付能力披露（C-ROSS体系）、再保险安排、CBIRC银保监会合规、条款智能比对、风险准备金说明等保险特有模块，是通用招标工具无法覆盖的专业场景。

---

## Trigger Keywords / 触发关键词

**English Triggers:** insurance bid, insurance bidding, group insurance bid, insurance tender, solvency disclosure, reinsurance, CBIRC compliance, insurance policy comparison, CBIRC, C-ROSS, risk reserve

**中文触发词（优先）：** 保险投标、团险投标、保险标书、保险公司招标、偿付能力、再保险、CBIRC合规、保险条款比对、偿二代、风险准备金

---

## Core Capabilities / 核心能力

### 0. 2025-2026 保险投标最新监管动态

| 时间 | 动态 | 对保险投标的影响 |
|------|------|---------------|
| **2026年1月1日** | 国家发改委招投标新规实施 | 招标人主体责任更明确，资格预审标准更规范 |
| **2026年** | 《招标投标法》修订推进 | 投标保证金管理、电子化投标要求提升 |
| **2025年** | 政府采购云平台扩大应用 | 保险投标需支持电子投标（PDF+结构化表单） |
| **2024年3月** | C-ROSS规则Ⅱ全面实施 | 偿付能力披露数据更新，须用最新格式 |
| **2025年10月** | 第四套生命表发布 | 影响定价基础，技术标中精算说明需更新 |
| **2025年** | 金融机构联合黑灰产打击 | 招标方对保险公司反欺诈能力评估趋严 |

### 1. Insurance Bid Document Generation / 保险投标文书生成

#### 技术标模块
- **公司资质**：保险许可证、营业执照、信用评级
- **偿付能力披露**：核心偿付能力充足率、综合偿付能力充足率（按 C-ROSS 体系）
- **再保险安排**：比例再保险/非比例再保险安排说明
- **理赔服务网络**：全国理赔网点、理赔时效承诺
- **风控体系**：核保规则、风控模型、反欺诈体系
- **IT 系统能力**：核心业务系统、线上服务平台

#### 商务标模块
- **保费报价**：纯风险保费 + 费用附加 + 利润附加
- **免赔额/免赔率设定**：根据风险暴露科学设定
- **费率浮动机制**：历史赔付率挂钩的动态调整
- **增值服务报价**：健康管理、风险咨询、理赔协助

#### 废标风险检查（保险专属）
- CBIRC 资质合规检查（保险许可证有效期、分支机构经营许可）
- 偿付能力充足率是否符合监管要求（≥100%核心，≥150%综合）
- 再保险安排是否符合监管要求（危险单位划分、合约分保比例）
- 条款是否包含禁止性规定（格式合同条款排查）
- 报价是否满足招标文件的实质性要求

### 2. Insurance Policy Clause Comparison / 保险条款智能比对

| 比对类型 | 说明 |
|---------|------|
| 主险 vs 附加险 | 保障范围差异、免责条款对比 |
| 不同公司产品 | 同类型产品的条款优劣对比 |
| 新旧条款 | 监管新规下的条款更新对比 |
| 招标要求 vs 拟投保单 | 响应度分析 |

### 3. CBIRC Regulatory Compliance / 监管合规检查（CBIRC）

自动检查以下合规要点：
- **《保险法》** 合规性（第 89-118 条条款检查）
- **《保险公司偿付能力监管规则第 1-20 号》** 披露完整性
- **《再保险业务管理规定》** 分保安排合规性
- **《保险条款和保险费率管理办法》** 条款报备情况
- **《保险经纪人监管规定》** 经纪机构资质检查

### 4. Group Insurance Specialization / 团险专项能力

- **团体健康险**：重疾、医疗、意外组合方案设计
- **企业年金/补充养老**：方案设计、投资收益率测算
- **关键人员保险**：董责险、关键人寿险方案
- **员工福利计划**：弹性福利方案、自选套餐设计

---

## Workflow / 工作流程

```
阶段一：需求解析
  → 识别招标类型（企业团险/政府统保/经纪招标）
  → 提取保险责任范围、保额、免赔额等关键参数
  → 识别投标人资质要求（注册资本、分支机构、偿付能力）

阶段二：文书生成
  → 调用 templates 生成保险行业特有内容
  → 根据招标要求填入偿付能力、再保险等特有内容
  → 生成技术标、商务标、资格证明文件三个分册

阶段三：废标风险检查
  → CBIRC 合规检查
  → 核对报价响应度
  → 检查签字盖章完整性

阶段四：优化建议
  → 基于历史中标数据给出报价优化建议
  → 识别竞争差异化亮点
  → 给出增值服务组合建议
```

---

## Synergy with Other Skills / 与其他Skill协同

- **tender-bidding-assistant**：通用招标流程可委托其处理
- **docx**：用于生成最终的 .docx 投标文件
- **xlsx**：用于生成报价明细表、保费计算表
- **pdf**：用于合并扫描件（许可证、资质证书）
- **insurance-solvency-reporter**：偿付能力报告深度内容

---

## 附录G：阿里点金(Dianjin)融合精华 — 保险计划书生成与竞品对比

### G.1 核心工作流程（Dianjin融合版）

#### 步骤1：客户需求深度分析
| 分析维度 | 分析要点 | 输出成果 |
|---------|---------|---------|
| **保障需求** | 寿险/重疾/医疗/养老缺口 | 保障缺口分析报告 |
| **财务能力** | 收入/资产/负债/预算 | 保费负担能力评估 |
| **购买偏好** | 品牌偏好/产品类型/缴费期 | 产品推荐策略 |
| **决策风格** | 理性/感性/独立/依赖 | 销售沟通策略 |

#### 步骤2：计划书智能生成
| 生成模块 | 内容要点 | 定制化要点 |
|---------|---------|---------|
| **客户画像** | 人口统计/风险偏好/保险需求 | 个性化标签、需求排序 |
| **保障方案** | 产品组合/保额/期限/缴费期 | 预算匹配、需求覆盖 |
| **利益演示** | 现金价值/保障利益/分红演示 | 场景化演示、可视化图表 |
| **对比分析** | 本品vs竞品、优势/劣势分析 | 客观对比、突出优势 |

#### 步骤3：竞品对比分析
- **对比维度**：产品责任、费率、公司实力、服务水平
- **对比方法**：表格对比、雷达图、优劣势分析
- **对比输出**：竞品对比报告、优势提炼话术

#### 步骤4：方案呈现与异议处理
- **呈现技巧**：FABE法则（特性-优势-利益-证据）
- **异议处理**：LSCPA模型（倾听-共情-澄清-提出-确认）
- **成交促成**：假设成交法、二选一法、危机促单法

---

### G.2 风险评分机制（Dianjin精髓）

| 风险维度 | 评分指标 | 权重 | 风险阈值 |
|---------|---------|------|---------|
| 需求匹配 | 产品与客户需求匹配度 | 30% | 匹配度<60% |
| 负担能力 | 保费/收入比、续保能力 | 25% | 保费/收入比>20% |
| 合规风险 | 销售合规、适当性管理 | 20% | 销售过程不合规 |
| 诚信风险 | 告知真实性、历史记录 | 15% | 告知不实或历史违规 |
| 声誉风险 | 客户满意度、投诉记录 | 10% | 客户投诉或负面评价 |

**综合风险等级**：
- 低风险（0-20分）：需求匹配，正常承保
- 中风险（21-40分）：需求基本匹配，关注负担能力
- 高风险（41-60分）：需求不匹配或负担能力不足，审慎承保
- 极高风险（61-80分）：诚信风险或合规风险，拒绝承保或报警

---

### G.3 合规约束（Dianjin精髓）

1. **不适用边界**：本技能不适用于医学诊断、法律建议，此类需求需转交医疗或法律专业人士
2. **禁止承诺**：不使用"一定赔付""guaranteed payout"等承诺性表述
3. **禁止替代决策**：仅输出分析建议，最终承保决策由核保师/核保主管出具
4. **数据溯源**：客户数据、健康状况必须标注来源和获取日期
5. **隐私保护**：客户信息、健康状况必须保密
6. **客观中立**：销售不得误导客户，须客观呈现产品利弊

---

### G.4 测试用例（Dianjin精髓）

| 用例ID | 输入场景 | 预期输出 | 验证点 |
|--------|---------|---------|---------|
| TC001 | 客户35岁，家庭年收入50万，有房贷200万，已有寿险100万 | 寿险缺口100万，建议加保100万定期寿险，计划书包含3个方案 | 缺口计算准确、方案合理 |
| TC002 | 客户45岁，家庭年收入30万，保费预算5万/年，对比A/B/C三家公司产品 | 保费/收入比16.7%，建议控制在4-6万/年，竞品对比客观全面 | 负担能力评估合理、对比客观 |
| TC003 | 客户55岁，有高血压糖尿病史，未如实告知，计划书未体现健康异常 | 极高风险（70分），建议如实告知或拒保，计划书需健康告知提示 | 诚信风险评估准确 |

---

### G.5 关联技能（Dianjin精髓）

- **保险理赔专家**（`insurance-claims-intelligence`）：提供理赔材料分析、责任认定、欺诈检测
- **保险反欺诈**（`insurance-anti-fraud`）：提供欺诈检测、风险评分、异常模式识别
- **保险核保专家**（`insurance-actuarial-cn`）：提供核保规则、健康核验、风险分类

---

*融合来源：阿里点金(Dianjin) insurance-agent/plan-generator*
*融合时间：2026-05-31*
