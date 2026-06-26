# 销售沟通纪要：{{client_name}}

**日期**：{{date}} | **参与者**：{{participants}}
**客户公司**：{{client_company}} | **阶段**：{{deal_stage}}

---

## 🎯 客户痛点（Pain Points）
{{#each pain_points}}
- {{this}}
{{/each}}

## 💰 预算信号（Budget Signals）
{{budget_signals}}

## 👥 决策链（Decision Makers）
{{decision_chain}}

## 🏆 竞争对手（Competitive Mentions）
{{#each competitors}}
- {{name}}：{{comment}}
{{/each}}

## 📋 BANT 分析
- **Budget（预算）**：{{bant.budget}}
- **Authority（决策权）**：{{bant.authority}}
- **Need（需求）**：{{bant.need}}
- **Timeline（时间线）**：{{bant.timeline}}

## 🎯 下一步行动
{{#each action_items}}
- [ ] **{{who}}**：{{what}}（{{when}}）
{{/each}}

---
*MeetingOS Sales Intelligence · [clawhub.io/skills/meetingos](https://clawhub.io/skills/meetingos)*
