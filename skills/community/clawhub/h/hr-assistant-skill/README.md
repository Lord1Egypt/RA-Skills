# 人力助手（HR Assistant）

> 版本：0.1.0  
> 当前目标：通过智能技能辅助高效处理招聘、简历匹配、合同审查和培训考核等HR核心场景。

## 1. 员工定位

通过飞书接收岗位需求、简历、面试记录、合同模板和培训资料，调用 Hermes Agent skills 完成岗位画像、JD、简历筛选、面试支持、录用入职、劳动合同、培训计划和制度问答。

## 2. 场景包与子角色

| 场景包 | 子角色/责任位 | 目标 | 关键 skills |
| --- | --- | --- | --- |
| 招聘需求澄清 | 招聘顾问 | 把部门需求转成岗位画像、能力模型和招聘标准。 | HR01_position_profile, HR02_jd_generate |
| JD 与发布 | 招聘文案员 | 生成 JD、岗位卖点、招聘话术和发布文案。 | HR02_jd_generate, HR01_position_profile |
| 简历筛选 | 简历筛选员 | 解析简历并按岗位要求评分、排序和提示风险。 | HR03_resume_parse, HR04_resume_match_score |
| 面试支持 | 面试助理 | 生成面试题、追问、评估表和面试结论草稿。 | HR05_interview_question_generate, HR06_interview_evaluation |
| 录用与入职 | 入职管理员 | 生成 offer 要点、入职材料清单和流程提醒。 | HR08_onboarding_checklist, HR09_training_plan_generate |
| 劳动合同 | 合同助理 | 初审劳动合同关键条款并提示风险。 | HR07_labor_contract_check |
| 培训学习 | 培训管理员 | 生成岗位培训计划、学习材料和考题。 | HR09_training_plan_generate |
| 员工制度问答 | 制度问答员 | 回答考勤、假期、薪酬、报销等制度问题。 | HR09_training_plan_generate, HR07_labor_contract_check |

## 3. 领域 skills

| Skill ID | 名称 | 用途 | 主要输出 |
| --- | --- | --- | --- |
| HR01_position_profile | 岗位画像生成 | 生成岗位职责、胜任力模型、任职要求、筛选标准和面试关注点。 | position_profile, competency_model, screening_criteria |
| HR02_jd_generate | JD 生成 | 生成招聘 JD、岗位卖点、渠道发布文案和候选人沟通话术。 | jd_draft, channel_copy, candidate_pitch |
| HR03_resume_parse | 简历解析 | 抽取候选人教育、经历、技能、项目、稳定性和风险信息。 | resume_fields, career_timeline, risk_flags |
| HR04_resume_match_score | 简历匹配评分 | 按岗位要求对简历进行匹配评分并给出推荐理由。 | match_score, strengths, gaps, interview_suggestion |
| HR05_interview_question_generate | 面试题生成 | 生成结构化面试题、追问和评分维度。 | question_set, probing_questions, scorecard |
| HR06_interview_evaluation | 面试记录评估 | 根据面试记录生成能力评估、风险提示和下一步建议。 | evaluation_summary, risk_items, next_recommendation |
| HR07_labor_contract_check | 劳动合同初审 | 检查合同期限、试用期、薪酬、岗位、保密、竞业和解除条款。 | contract_risk_list, revision_suggestions, need_legal_review |
| HR08_onboarding_checklist | 入职材料清单 | 生成 offer 要点、入职材料、设备账号、培训和提醒清单。 | onboarding_checklist, reminder_tasks |
| HR09_training_plan_generate | 培训计划生成 | 根据岗位和能力缺口生成培训计划、学习材料和考试题。 | training_plan, quiz_items, tracking_table |

## 4. 关键边界

- 可以生成草稿、建议、清单、摘要、风险提示和归档记录。
- 涉及录用决定、薪酬职级、劳动合同条款、员工敏感信息、对外发送offer时必须人工确认。
- 演示样例必须使用脱敏或虚拟数据，不使用真实客户、员工、财务、合同或技术敏感信息。
- 所有 Hermes Agent skill 调用需要记录输入、输出、确认人和归档位置。

## 5. 文件结构

```text
hr-assistant/
  README.md
  employee.yaml
  system_prompt.md
  workflows.md
  runbook.md
  skills/
  knowledge/
  templates/
  test_cases/
  demo/
```
