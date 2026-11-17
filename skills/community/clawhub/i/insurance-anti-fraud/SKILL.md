---
name: Insurance Anti-Fraud Expert
description: AI-powered insurance anti-fraud analysis skill — detects and prevents insurance fraud across all major insurance types. Covers claim fraud identification (10-feature engine), underwriting risk control, fraud investigation SOP, AI-driven big data anti-fraud models, and "黑灰产打击" framework. Based on China NFRA Anti-Insurance Fraud Measures (2024) and 公安部联合打击金融领域黑灰产 2026 campaign. Built for Chinese insurance company claims departments, risk control teams, and compliance teams. Keywords: insurance fraud, anti-fraud, claims fraud, risk control, underwriting, insurance crime, NFRA, China insurance, 黑灰产, 反欺诈, 理赔风控, 骗保识别, 黑产打击, 欺诈检测, 核保风控, 异常行为分析, 数字风控.
slug: insurance-anti-fraud
version: "5.0.0"
---

# Insurance Anti-Fraud Expert / 保险反欺诈分析专家


### 保险监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 保险监管 | 2026年Q1反洗钱监管力度加大，洗钱风险评估要求提升 | 反欺诈模型需整合合规审查和快速理赔风控逻辑 |
| 保险监管 | NFRA 2026年Q1保险业处罚数据更新，合规管理持续深化 | 反欺诈模型需整合合规审查和快速理赔风控逻辑 |
| 保险监管 | 车险理赔提速：5000元以下小额事故'一键理赔、24小时到账' | 反欺诈模型需整合合规审查和快速理赔风控逻辑 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered insurance anti-fraud analysis expert — the definitive skill for detecting and preventing insurance fraud in the Chinese insurance market. Covers the complete CBIRC Anti-Insurance Fraud Measures (2024) framework, claim fraud identification engine (10 detection features), underwriting risk control system, fraud investigation workflows, and big data anti-fraud technology applications. Built for insurance company claims departments, risk control teams, and compliance teams.
>
> **中文:** 保险反欺诈分析专家——中国《反保险欺诈工作办法》合规垂直Skill。覆盖四位一体反欺诈工作体系、理赔欺诈识别引擎（10大欺诈特征）、核保风控体系、欺诈案件调查流程（SOP）、大数据反欺诈技术应用。适用：保险公司理赔部、风控部、合规部、反欺诈调查员、保险公司核保岗。

---

## Trigger Keywords / 触发关键词

**English:** anti-fraud, insurance fraud, claims fraud, fraud detection, risk control, underwriting risk, fraud investigation, money laundering, CBIRC compliance, claim review, insurance crime, fraud prevention, China insurance

**中文触发词（优先）：** 反保险欺诈、保险欺诈识别、理赔欺诈、反欺诈调查、理赔风控、核保风控、道德风险、保险诈骗、欺诈特征、异常理赔、保险黑产、虚假投保、带病投保、理赔调查、欺诈渗漏、反欺诈模型

---

## Core Capabilities / 核心能力

### 0. 最新监管动态（截至2026年5月）

| 时间 | 事项 | 反欺诈影响 |
|------|------|---------|
| **2024年7月22日** | 国家金融监督管理总局《反保险欺诈工作办法》发布实施 | 四位一体体系正式确立，险企主体责任强化 |
| **2026年3月** | 公安部、金融监管总局联合部署新一轮金融领域"黑灰产"打击工作 | 专业化欺诈团伙（骗保黑产）打击力度加强 |
| **2025年起** | 银保信反欺诈平台升级，接入医保数据 | 跨机构理赔记录共享更全面，重复索赔识别率提升 |
| **2025年** | 大数据反欺诈建模纳入险企风控体系评估（SARM评级） | 反欺诈能力影响偿二代风险综合评级 |

### 1. Regulatory Framework: Anti-Insurance Fraud Measures / 监管框架：《反保险欺诈工作办法》全解

**法规来源**：国家金融监督管理总局，2024年7月22日发布实施

#### 四位一体反欺诈工作体系

```text
┌─────────────────────────────────────────────────┐
│                   四位一体体系                        │
├─────────────────────────────────────────────────┤
│  ① 行业反欺诈：银保信/精算师协会/保险行业协会协同    │
│  ② 公司主体责任：各保险公司反欺诈组织架构           │
│  ③ 公安司法机关：涉嫌犯罪的移送公安                │
│  ④ 监管部门：日常监管+专项检查+处罚                │
└─────────────────────────────────────────────────┘
```

#### 欺诈类型分类

| 类型 | 定义 | 典型场景 | 涉案险种 |
|------|------|---------|---------|
| **投保欺诈** | 故意不告知/虚假告知 | 带病投保、职业虚报 | 健康险、意外险 |
| **理赔欺诈** | 虚假索赔/夸大损失 | 伪造事故、虚构身份 | 车险、意外险、健康险 |
| **团伙欺诈** | 有组织犯罪团伙 | 专业碰瓷、产业链欺诈 | 医疗险、意外险 |
| **内部欺诈** | 内部人员参与 | 内外勾结、虚假理赔 | 各险种 |
| **洗钱型欺诈** | 借保险洗白资金 | 趸交高额寿险退保 | 寿险 |

### 2. Claims Fraud Identification Engine / 理赔欺诈识别引擎

#### 健康险理赔欺诈十大特征

| 特征序号 | 欺诈特征 | 识别信号 |
|---------|---------|---------|
| 1 | **短时间内集中投保** | 等待期刚过即集中大量理赔 |
| 2 | **带病投保隐瞒病史** | 健康告知全为"否"，理赔时发现既往症 |
| 3 | **虚假医院就诊** | 病历签名笔迹不一致、无实际治疗记录 |
| 4 | **过度医疗/过度检查** | 费用远超同类疾病平均水平的3倍以上 |
| 5 | **团伙作案特征** | 同一天、同一家医院、同一病种的群体报案 |
| 6 | **非正常高保额** | 收入与投保金额严重不符（意外险高保额） |
| 7 | **频繁小额理赔** | 利用免赔额规则反复小额索赔 |
| 8 | **跨公司重复索赔** | 利用信息不对称在多家公司重复索赔 |
| 9 | **职业骗保** | 特定高风险职业频繁出险（矿工/高危行业） |
| 10 | **重大事故造假** | 死亡/伤残事故真实性存疑 |

#### 欺诈风险量化评分模型

```python
# Fraud Risk Scoring Model (simplified / 简化示例）
def fraud_score(case):
    score = 0
    
    # 等待期观察（权重30%）
    if case.waiting_period_days < 30:
        score += 30
    elif case.waiting_period_days < 90:
        score += 15
    
    # 投保保额异常（权重25%）
    if case.coverage_to_income_ratio > 10:
        score += 25
    elif case.coverage_to_income_ratio > 5:
        score += 15
    
    # 就诊医院异常（权重20%）
    if case.hospital_fraud_history:
        score += 20
    elif case.is_chain_hospital == False and case.amount > 50000:
        score += 10
    
    # 既往理赔记录（权重15%）
    if case.past_fraud_record:
        score += 15
    elif case.past_claim_count > 5:
        score += 8
    
    # 同案关联（权重10%）
    if case.linked_to_suspected_cases:
        score += 10
    
    # 返回风险等级
    if score >= 60: return "HIGH_RISK - 立即调查"
    elif score >= 30: return "MEDIUM_RISK - 重点审核"
    else: return "LOW_RISK - 正常流程"
```

### 3. Underwriting Risk Control / 核保风控体系

#### 核保风险分级表

| 风险等级 | 评估条件 | 核保决策 | 附加条件 |
|---------|---------|---------|---------|
| **标准体** | 健康告知全否、无异常记录 | 标准承保 | - |
| **次标准体A** | 轻微异常（BMI偏高/脂肪肝） | 加费承保 | +10%-30%保费 |
| **次标准体B** | 中等异常（高血压/糖尿病早期） | 有条件承保 | 除外责任+加费 |
| **延期体** | 病情不稳定或待确诊 | 延期观察 | 6-12个月后重核 |
| **拒保体** | 重大既往症/高风险职业 | 拒保 | 不予承保 |

### 4. Fraud Investigation Workflow / 欺诈案件调查流程

```text
受理报案
    ↓
初步审核（24小时内）
  ├─ 资料完整性检查
  ├─ 基本逻辑校验
  └─ 欺诈特征快速筛查（AI模型打分）
         ↓
风险分级
  ├─ LOW_RISK → 正常理赔流程
  ├─ MEDIUM_RISK → 理赔调查（7天内）
  └─ HIGH_RISK → 深度调查+报案
         ↓
调查阶段
  ├─ 医疗数据核实（医保/医院调取）
  ├─ 既往投保记录查询（银保信平台）
  ├─ 现场走访/面访
  └─ 第三方数据核查（大数据风控）
         ↓
结论处置
  ├─ 正常赔付 → 快速支付
  ├─ 协议赔付 → 减少金额达成和解
  ├─ 拒赔处理 → 发拒赔通知+说明
  └─ 报案追究 → 移送公安（涉嫌犯罪）
```

### 5. Anti-Fraud Capability Benchmark / 反欺诈能力建设

| 指标 | 行业平均水平 | 先进水平 | 说明 |
|------|------------|---------|------|
| **欺诈渗漏率** | 15%-20% | <5% | 欺诈+渗漏（过度理赔）占保费比例 |
| **欺诈识别率** | 30%-40% | >70% | 实际欺诈案件中被识别的比例 |
| **案件调查周期** | 15-30天 | <7天 | 从报案到结论 |

### 5. 黑灰产打击专项 / "黑灰产" Insurance Crime Crackdown|

#### 2026年金融领域黑灰产打击重点

| 黑产类型 | 作案方式 | 识别特征 | 打击措施 |
|---------|---------|---------|---------|
| **职业骗保团伙** | 组织专业人员批量刷单出险 | 同一手机号/IP反复关联不同被保人 | 设备指纹+关系网络图谱 |
| **医院内外勾结** | 内部人员虚开发票、虚假病历 | 同一医生名字大量出现、异常诊断码 | 医保数据交叉验证 |
| **理赔中介代办黑产** | 伪造材料专业代理索赔 | 同一律所/代理人反复代理多个客户 | 代理人反欺诈黑名单 |
| **网络刷单骗保** | 利用电商平台虚假交易配套保险 | 退货率异常高、退款时间规律性 | 电商平台数据共享 |
| **趸交退保洗钱** | 高额趸交保险快速退保洗钱 | 超大额保单+短期退保+频繁汇款 | 反洗钱大额交易报告 |

#### 黑名单管理体系

```python
# 黑名单多维度关联查询框架
def blacklist_check(claimant_info):
    checks = {
        "银保信欺诈黑名单": query_nfra_blacklist(claimant_info.id),
        "公安人口信息核查": query_police_id(claimant_info.id),
        "医保异常名单": query_medical_insurance(claimant_info.id),
        "法院失信被执行人": query_court_dishonesty(claimant_info.id),
        "跨公司理赔记录": query_cross_company_claims(claimant_info.id),
        "设备指纹关联": query_device_fingerprint(claimant_info.device_id),
        "关联人身份": query_related_persons(claimant_info.id),
    }
    hit_count = sum(1 for v in checks.values() if v.is_hit)
    risk_level = "HIGH" if hit_count >= 3 else "MEDIUM" if hit_count >= 1 else "LOW"
    return {"checks": checks, "hit_count": hit_count, "risk_level": risk_level}
```

### 6. AI-Driven Anti-Fraud Technology / AI大数据反欺诈技术|

#### 主流反欺诈建模技术栈

| 技术 | 应用场景 | 效果 |
|------|---------|------|
| **图神经网络 GNN** | 团伙欺诈识别，挖掘关联关系 | 检出率提升40%以上 |
| **异常检测算法 Isolation Forest** | 无监督欺诈信号发现 | 适合样本不均衡场景 |
| **NLP票据真实性识别** | 发票/病历文本特征提取 | 伪造材料识别准确率>90% |
| **设备指纹 + IP画像** | 识别同设备多账号欺诈 | 有效拦截批量刷单 |
| **时序行为分析** | 投保→理赔时间序列异常 | 等待期欺诈识别 |

---

## Reference Files / 参考文件

| File / 文件 | Content / 内容说明 |
|------|---------|
| `references/anti_fraud_guide.md` | 反欺诈工作办法解读 + 各险种欺诈特征详解 |
| `references/underwriting_risk_assessment.md` | 核保风控体系，含风险分级表和异常标记规则 |
| `references/claim_investigation_sop.md` | 理赔欺诈调查 SOP，含调查话术和流程图 |
| `references/fraud_case_study.md` | 典型欺诈案例分析（含真实案例改编） |
| `references/data_model_guide.md` | 反欺诈数据模型构建指南，含评分卡示例 |

---

## 附录G：阿里点金(Dianjin)融合精华 — 理赔欺诈检测与异常模式识别

### G.1 核心工作流程（Dianjin融合版）

#### 步骤1：理赔欺诈特征识别
| 欺诈类型 | 识别特征 | 风险信号 |
|---------|---------|---------|
| **虚构事故** | 事故时间/地点/天气交叉验证 | 事故描述矛盾、天气不符、地点异常 |
| **夸大损失** | 维修估价vs市场价、定损单比对 | 估价超市场价30%、定损单不一致 |
| **重复索赔** | 历史索赔记录、跨公司查询 | 同一事故多公司索赔、相似事故频繁 |
| **团伙作案** | 关系图谱、IP/MAC地址聚类 | 多案件关联同一修理厂/医院 |

#### 步骤2：风险量化评分
| 评分维度 | 评分指标 | 权重 | 风险阈值 |
|---------|---------|------|---------|
| 材料异常 | 伪造检测得分、交叉验证结果 | 30% | 伪造检测得分<60分 |
| 行为异常 | 索赔频率、跨公司记录 | 25% | 12个月内索赔>3次 |
| 损失异常 | 损失程度与事故匹配度 | 20% | 损失程度异常超30% |
| 关联异常 | 与修理厂/医院关联关系 | 15% | 关联修理厂/医院历史欺诈率>10% |
| 合规异常 | 理赔时效、客户服务合规 | 10% | 超理赔时效或客户投诉 |

#### 步骤3：异常模式挖掘
- **关系网络分析**：被保险人-修理厂-医院关系图谱
- **时空模式分析**：事故时间/地点聚类分析
- **金额模式分析**：索赔金额分布异常检测
- **行为序列分析**：索赔前行为模式异常

#### 步骤4：处置决策与报告
- **处置决策**：正常赔付/加强调查/拒赔/报警
- **调查报告**：欺诈调查报告、证据链文档
- **监管报送**：重大欺诈案件监管报送

---

### G.2 风险评分机制（Dianjin精髓）

**综合风险等级**：
- 低风险（0-20分）：正常赔付，标准流程
- 中风险（21-40分）：加强调查，必要时现场查勘
- 高风险（41-60分）：重点调查，必要时外调或第三方公估
- 极高风险（61-80分）：疑似欺诈，移交反欺诈部门或报警

---

### G.3 合规约束（Dianjin精髓）

1. **不适用边界**：本技能不适用于法律诉讼代理、刑事责任认定，此类需求需转交法律合规部门
2. **禁止承诺**：不使用"一定拒赔""guaranteed denial"等承诺性表述
3. **禁止替代决策**：仅输出分析建议，最终理赔决策由理赔主管/核赔师出具
4. **数据溯源**：医疗数据、事故证据必须标注来源和获取日期
5. **隐私保护**：客户信息、调查细节必须保密
6. **客观中立**：分析不得受绩效考核影响，须客观呈现风险

---

### G.4 测试用例（Dianjin精髓）

| 用例ID | 输入场景 | 预期输出 | 验证点 |
|--------|---------|---------|---------|
| TC001 | 车险：事故损伤轻微但定损5万，关联修理厂历史欺诈率15% | 极高风险（70分），建议移交反欺诈调查 | 关联异常识别准确 |
| TC002 | 医疗险：诊断感冒但发票2万，患者12个月内索赔5次 | 极高风险（75分），建议医院调查+费用核查 | 行为异常识别准确 |
| TC003 | 财产险：火灾索赔500万，同类事故3次，关系网含3家修理厂 | 极高风险（80分），建议公安报案 | 团伙模式识别准确 |

---

### G.5 关联技能（Dianjin精髓）

- **保险理赔专家**（`insurance-claims-intelligence`）：提供理赔材料分析、责任认定、理赔流程
- **保险核保专家**（`insurance-actuarial-cn`）：提供核保规则、健康核验、风险分类
- **保险代理人**（`insurance-agent-trainer`）：提供客户画像、保障缺口分析

---

*融合来源：阿里点金(Dianjin) claim-expert*
*融合时间：2026-05-31*
