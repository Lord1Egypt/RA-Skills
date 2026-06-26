# Agent Profile & Skill Assessment Framework / 代理人画像与能力评估体系

## 一、代理人画像标准模板 / Agent Profile Standard Template

```json
{
  "agent_id": "AG_XXXX_XXXX",
  "basic_info": {
    "name": "[化名，保护隐私]",
    "gender": "男/女",
    "age": 32,
    "education": "本科",
    "certifications": [
      "保险代理人资格证书（必选）",
      "健康险销售资质（可选）",
      "理财规划师（可选）",
      "CFP国际金融理财师（可选）"
    ],
    "entry_date": "2024-03-01",
    "tenure_months": 14,
    "agency": "[营业部和团队名称]"
  },
  "skill_level": {
    "current": "L2",
    "label": "进阶级",
    "certified_date": "2025-06-01",
    "last_assessment_date": "2026-03-15",
    "target_level": "L3",
    "target_date": "2026-12-31"
  },
  "performance_metrics": {
    "quarterly": {
      "premium_target": 150000,
      "premium_actual": 128000,
      "target_achievement_rate": 0.853,
      "policy_count": 8,
      "avg_policy_size": 16000,
      "new_customers": 5,
      "existing_customers": 3,
      "closing_rate": 0.32,
      "visit_count": 25
    },
    "historical": {
      "months_1_3_premium": 45000,
      "months_4_6_premium": 68000,
      "months_7_12_premium": 142000,
      "months_13_plus_trend": "+12%"
    }
  },
  "product_mastery_radar": {
    "term_life": {
      "score": 0.85,
      "label": "熟练",
      "details": "条款清晰，能独立完成产品对比"
    },
    "whole_life": {
      "score": 0.72,
      "label": "良好",
      "details": "万能账户理解较好，传承功能讲解有提升空间"
    },
    "critical_illness": {
      "score": 0.58,
      "label": "薄弱",
      "details": "病种定义理解不足，脑中风后遗症与同类产品对比不熟悉"
    },
    "medical_insurance": {
      "score": 0.80,
      "label": "熟练",
      "details": "社保对比算账能力强"
    },
    "annuity": {
      "score": 0.45,
      "label": "薄弱",
      "details": "IRR计算不熟练，年金转换逻辑讲解不够清晰"
    },
    "investment_linked": {
      "score": 0.38,
      "label": "薄弱",
      "details": "净值波动解释不够形象，高端客户需求识别不足"
    }
  },
  "competency_assessment": {
    "needs_identification": {
      "score": 0.75,
      "label": "良好",
      "evidence": "能通过提问识别客户基础需求"
    },
    "product_presentation": {
      "score": 0.68,
      "label": "及格",
      "evidence": "讲解清晰但缺乏个性化，客户参与度一般"
    },
    "objection_handling": {
      "score": 0.62,
      "label": "薄弱",
      "evidence": "异议处理反应较慢，算账说服力不足"
    },
    "closing_technique": {
      "score": 0.78,
      "label": "良好",
      "evidence": "促成时机把握较好，促成后跟单能力强"
    },
    "compliance_awareness": {
      "score": 0.92,
      "label": "优秀",
      "evidence": "双录操作规范，合规话术使用到位"
    },
    "customer_relationship": {
      "score": 0.88,
      "label": "优秀",
      "evidence": "老客户复购率高，转介绍渠道稳定"
    }
  },
  "training_history": [
    {
      "date": "2026-03-15",
      "product": "健康险",
      "type": "情景对练",
      "duration_minutes": 30,
      "score_before": 65,
      "score_after": 78,
      "improvement": "+13"
    },
    {
      "date": "2026-04-01",
      "product": "终身寿险",
      "type": "案例研讨",
      "duration_minutes": 45,
      "score_before": 70,
      "score_after": 74,
      "improvement": "+4"
    }
  ],
  "personalized_weak_points": [
    "健康险条款定义讲解不够通俗，需要案例化表达",
    "IRR计算不够熟练，高净值客户对收益率敏感时容易卡壳",
    "竞品对比知识储备不足，主要竞品（平安、太平洋）产品线不熟悉"
  ],
  "personalized_strong_points": [
    "缘故市场开发能力强，信任背书效果好",
    "老客户维护细致，复购率高于团队平均",
    "合规意识强，从未发生投诉"
  ],
  "daily_schedule_sample": {
    "workday_pattern": "标准工作日（09:00-18:00）",
    "meeting_hours": "09:00-09:30（晨会）",
    "avg_visits_per_day": 3.5,
    "travel_pattern": "以市区客户拜访为主，偶尔郊区"
  }
}
```

---

## 二、能力评估量表 / Competency Assessment Rubric

### L1 → L2 晋升评估标准

| 能力维度 | L1入门标准 | L2进阶标准 | L3专家标准 |
|---------|-----------|-----------|-----------|
| **产品知识** | 能复述产品基本信息（名称、保障、缴费期）| 能对比3款以上同类产品，能解释条款差异 | 能做竞品逐条对比，能处理复杂条款解释 |
| **需求挖掘** | 能问出客户"要买什么类型" | 能通过追问发现客户"真实担心和期望" | 能挖掘高净值客户资产隔离/传承/税务需求 |
| **异议处理** | 能处理2-3个高频异议（有固定话术）| 能灵活运用算账、类比、共情等方法 | 能反客为主，将异议转化为成交契机 |
| **促成技巧** | 有促成意识，能做1次标准促成 | 能识别多个促成信号，能做2-3次渐进式促成 | 促成无痕自然，让客户感觉是自己在决定买 |
| **合规意识** | 双录操作规范 | 合规话术灵活运用，能识别客户误导风险 | 能主动向团队新人传授合规经验 |
| **客户经营** | 能维护老客户，基础问候 | 能做老客户加保需求激活，转介绍开发 | 能建立高净值客户长期顾问关系，跨品类经营 |
| **数字能力** | 保额保费简单计算 | IRR、内部收益率、节税计算熟练 | 能做综合财务规划方案（保险+理财+税务） |

---

## 三、能力雷达图数据 / Competency Radar Chart Data

```python
def get_radar_chart_data(agent_profile):
    """
    Generate radar chart data for agent competency visualization.
    Each dimension scores 0-100.
    """
    return {
        "labels": [
            "产品知识",
            "需求挖掘",
            "异议处理",
            "促成技巧",
            "合规意识",
            "客户经营",
            "数字规划"
        ],
        "L1_threshold": [70, 60, 50, 55, 80, 65, 40],
        "L2_threshold": [80, 75, 70, 75, 90, 80, 65],
        "L3_threshold": [90, 88, 85, 88, 95, 90, 80],
        "current_scores": [
            int(agent_profile["competency_assessment"]["product_knowledge"]["score"] * 100),
            int(agent_profile["competency_assessment"]["needs_identification"]["score"] * 100),
            int(agent_profile["competency_assessment"]["objection_handling"]["score"] * 100),
            int(agent_profile["competency_assessment"]["closing_technique"]["score"] * 100),
            int(agent_profile["competency_assessment"]["compliance_awareness"]["score"] * 100),
            int(agent_profile["competency_assessment"]["customer_relationship"]["score"] * 100),
            65  # 数字规划维度（需单独评估）
        ]
    }
```

---

## 四、成长路径模板 / Development Roadmap Template

```markdown
# 代理人成长路径 / Agent Development Roadmap

## 张明 — L2 → L3 专家级成长计划（90天）

### 当前状态（基线）
- 综合得分：72/100
- 主要短板：健康险异议处理（58分）、IRR计算（45分）
- 主要优势：客户关系（88分）、促成技巧（78分）

### 30天目标（第一阶段）
**主题**：健康险专项突破

| 周次 | 训练内容 | 训练量 | KPI目标 |
|------|---------|--------|--------|
| 第1周 | 健康险产品知识巩固（每日10题） | 50题 | 正确率≥75% |
| 第2周 | 健康险异议处理情景对练 | 5个场景 | 时效<45秒 |
| 第3周 | 健康险算账练习（社保管控vs商业险） | 10个案例 | 能独立算出差异 |
| 第4周 | 综合演练：健康险完整销售流程 | 3次完整陪练 | 综合得分≥72 |

### 60天目标（第二阶段）
**主题**：高净值客户专项 + IRR计算

| 周次 | 训练内容 | 训练量 | KPI目标 |
|------|---------|--------|--------|
| 第5周 | IRR计算原理与演示练习 | 20个算例 | 3分钟内完成计算 |
| 第6周 | 年金险IRR对比（vs定期存款/国债） | 10个场景 | 能清晰讲解 |
| 第7周 | 高净值客户情景对练（私企业主） | 5个场景 | 方案设计≥3产品 |
| 第8周 | 竞品对比（平安/太平洋/新华/泰康）| 各产品线1份对比表 | 熟练程度≥80% |

### 90天目标（第三阶段）
**主题**：综合实战 + 晋升评估

| 周次 | 训练内容 | 训练量 | KPI目标 |
|------|---------|--------|--------|
| 第9周 | 综合案例分析（家庭综合保障方案）| 10个案例 | 方案完整度≥85% |
| 第10周 | 导师带教（指导1名L1新人）| 2次实战带教 | 教学评分≥80 |
| 第11周 | 模拟晋升评估 | 3套综合试卷 | 总分≥85 |
| 第12周 | **正式晋升评估** | 实战考核 | 达标则晋升L3 |

### 成功标准
| 指标 | 当前值 | 30天目标 | 60天目标 | 90天目标 |
|------|--------|---------|---------|---------|
| 综合得分 | 72 | 75 | 80 | 85 |
| 健康险异议处理 | 58 | 70 | 78 | 82 |
| IRR计算 | 45 | 60 | 78 | 85 |
| 竞品对比 | 55 | 65 | 80 | 85 |
| 促成综合得分 | 78 | 80 | 82 | 85 |
```
