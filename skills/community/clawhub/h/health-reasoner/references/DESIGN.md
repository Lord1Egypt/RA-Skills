"""
health_reasoner.py — 日常状态健康推理引擎
=========================================

设计文档：
- 设计思路：规则引擎驱动的健康推理，而不是 ML 模型
- 原因：可解释性（每条建议都可溯源到具体规则）、零部署成本（无需模型权重）、隐私安全（本地运行）

核心设计决策：
1. dataclass 数据结构（UserHealthProfile / HealthAssessment）而不是 dict
   - 原因：类型安全、IDE 自动补全、__post_init__ 自动校验
2. 评分分5个维度（睡眠/饮食/运动/压力/烟酒）加权合成
   - 原因：可解释——用户能看到哪方面扣分最多
3. 风险等级先基于症状（紧急标志），再基于总分
   - 原因：症状是直接信号，评分是长期信号

架构：
```
UserHealthProfile → HealthAgent.assess()
                    ├── _calc_sleep_score()
                    ├── _calc_diet_score()
                    ├── _calc_exercise_score()
                    ├── _calc_stress_score()
                    ├── _calc_substance_score()
                    ├── _assess_risks()
                    ├── _generate_suggestions()
                    └── → HealthAssessment
```

第三方依赖：
- 核心模块：零依赖（纯 Python 标准库）
- REST API：Flask（可选，仅 API 模式需要）

历史：
- v1.0: 初始版本
- v2.0: 规则库重构，增加校验
