# 保险客户分层模型完整手册

> 本文件为 `insurance-private-domain-ops` Skill 配套参考

## 一、RFM+生命周期双维分层体系

### 1.1 RFM评分标准（保险行业适配版）

| 维度 | 计算口径 | 评分逻辑 | 分值标准 |
|------|---------|---------|---------|
| **R（最近投保距今天数）** | 客户最近一张有效保单生效日期距今天数 | 天数越少越好 | ≤90天=5分，91-180=4分，181-365=3分，366-730=2分，>730=1分 |
| **F（持单件数）** | 客户当前持有的有效保单数量（含已失效宽限期内的） | 件数越多越好 | ≥3件=5分，2件=4分，1件=3分，0件（脱保）=1分 |
| **M（年缴保费）** | 客户当前有效保单的年缴保费合计（趸交折算） | 金额越高越好 | ≥5万=5分，1-5万=4分，3000-1万=3分，<3000=2分，0=1分 |

**综合得分公式**：`总分 = R×0.3 + F×0.3 + M×0.4`

**分层阈值**：
- 4.0-5.0分 → `VIP-HIGH` 高价值客户
- 3.0-3.9分 → `VIP-MID` 中价值客户
- 2.0-2.9分 → `GENERAL` 一般客户
- 1.0-1.9分 → `LOW-VALUE` 低价值/流失客户

### 1.2 生命周期七层模型

```
潜在客户 → 新客户 → 活跃客户 → 沉默客户 → 流失预警
                                         ↓
                                   脱保客户（>30天宽期）
                                         ↓
                                   长期流失（>1年）
```

| 阶段 | 触发条件 | 标签 | 运营策略 |
|------|---------|------|---------|
| 潜在客户 | 未投保但有交互记录 | `PROSPECT` | 教育培育，需求激发 |
| 新客户 | 投保<1年 | `NEW-POLICY` | 激活信任，服务满意 |
| 活跃客户 | 1-3年，有理赔/加保记录 | `ACTIVE` | 交叉销售，家庭拓客 |
| 沉默客户 | ≥18个月无任何互动 | `SILENT` | 触达激活，防止流失 |
| 流失预警 | 保单到期前60天内 | `RENEWAL-WARN` | 续期优先触达 |
| 脱保客户 | 宽限期已过 | `CHURNED` | 盘活激活，二次转化 |
| 长期流失 | 脱保>1年 | `LONG-CHURN` | 年度触达，特殊活动 |

### 1.3 脱保客户专项激活分层

| 评估维度 | 权重 | 评分标准 |
|---------|-----|---------|
| **历史保费贡献** | 25% | 年均保费≥5万=5分，1-5万=4分，3000-1万=3分，<3000=2分，0=1分 |
| **历史保障缺口** | 25% | 原有保额/保费比<10=3分，10-50=4分，>50=5分 |
| **经济能力指标** | 20% | 城市+职业+年龄综合评估，高收入职业=5分 |
| **购买意愿信号** | 15% | 曾主动咨询产品=5分，被动接受=3分，明确拒绝=1分 |
| **产品匹配度** | 15% | 有更优产品可替代=5分，产品同质=3分，无合适产品=1分 |

**激活名单优先级**：
- 优先激活：综合得分≥70分
- 次优先激活：综合得分50-69分
- 常规触达：综合得分30-49分
- 低优先级：综合得分<30分

## 二、客户标签体系（企微/SCRM适配）

### 基础属性标签
- [年龄段] 25-30 / 31-40 / 41-50 / 51-60 / 60+
- [城市] 一线城市 / 新一线 / 二线 / 三线及以下
- [职业] 企业主 / 管理层 / 白领 / 蓝领 / 自由职业
- [家庭状况] 已婚有子女 / 已婚无子女 / 未婚 / 独居

### 价值分层标签
- [价值层] VIP-HIGH / VIP-MID / GENERAL / LOW-VALUE
- [生命周期] PROSPECT / NEW-POLICY / ACTIVE / SILENT / RENEWAL-WARN / CHURNED / LONG-CHURN

### 行为标签（自动打标规则）
- [互动行为] 浏览产品页 / 参与活动 / 填写问卷 / 咨询顾问
- [购买行为] 新单 / 加保 / 续期 / 复效 / 退保
- [服务行为] 申请理赔 / 领取红利 / 变更保单

## 三、存量客户数据SQL查询模板

```sql
SELECT 
    customer_id,
    name, phone, city, occupation_level, family_status,
    DATEDIFF(CURDATE(), MAX(policy_effective_date)) AS recency_days,
    COUNT(DISTINCT policy_id) AS policy_count,
    SUM(annual_premium) AS total_annual_premium,
    MAX(interaction_date) AS last_interaction_date,
    SUM(claim_amount) AS total_claim_amount,
    CASE 
        WHEN DATEDIFF(CURDATE(), MAX(policy_effective_date)) > 365 THEN 'CHURNED'
        WHEN DATEDIFF(CURDATE(), MAX(interaction_date)) > 540 THEN 'SILENT'
        WHEN COUNT(DISTINCT policy_id) >= 3 THEN 'VIP-HIGH'
        WHEN SUM(annual_premium) >= 10000 THEN 'VIP-HIGH'
        ELSE 'GENERAL'
    END AS customer_segment
FROM customer_policy_data
GROUP BY customer_id;
```
