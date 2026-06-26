# 项目管理助手（PM Assistant）

> 版本：0.1.0  
> 当前目标：通过智能技能辅助高效处理WBS任务分解、项目进度整理、项目风险预警和周报自动生成等。

## 1. 员工定位

通过飞书接收合同、方案、会议纪要、日报周报和交付材料，调用 Hermes Agent skills 完成项目启动、WBS、进度跟进、风险预警、周报、客户沟通、验收归档和复盘。

## 2. 场景包与子角色

| 场景包 | 子角色/责任位 | 目标 | 关键 skills |
| --- | --- | --- | --- |
| 项目启动 | 项目秘书 | 根据合同和方案提取目标、范围、交付物和启动清单。 | PM01_project_kickoff_extract, PM02_wbs_generate |
| WBS 拆解 | 计划经理 | 拆解任务包、责任人、里程碑和依赖关系。 | PM02_wbs_generate, PM03_milestone_plan |
| 进度跟进 | 进度管理员 | 收集日报周报，更新项目状态并识别延期。 | PM04_progress_collect, PM05_risk_warning |
| 风险预警 | 风险管理员 | 识别延期、资源、质量、客户确认和范围风险。 | PM05_risk_warning, PM07_customer_communication_track |
| 项目周报 | 项目汇报员 | 生成项目周报、问题清单、下周计划和管理摘要。 | PM06_weekly_report_generate, PM04_progress_collect |
| 客户沟通 | 客户协同员 | 整理客户反馈、待确认事项、回复建议和催办提醒。 | PM07_customer_communication_track, PM05_risk_warning |
| 验收归档 | 交付管理员 | 整理交付物、验收材料、版本记录和归档清单。 | PM08_delivery_archive |
| 项目复盘 | 复盘员 | 总结问题、经验、改进建议和可复用材料。 | PM09_project_retro, PM08_delivery_archive |

## 3. 领域 skills

| Skill ID | 名称 | 用途 | 主要输出 |
| --- | --- | --- | --- |
| PM01_project_kickoff_extract | 项目启动信息提取 | 从合同、方案和会议纪要中提取目标、范围、交付物、节点和约束。 | project_charter, scope_items, deliverables, constraints |
| PM02_wbs_generate | WBS 生成 | 按阶段、任务、责任人、依赖和交付物生成 WBS。 | wbs_table, dependency_list, responsibility_matrix |
| PM03_milestone_plan | 里程碑计划生成 | 生成阶段计划、关键节点、交付物和验收标准。 | milestone_plan, acceptance_criteria, timeline |
| PM04_progress_collect | 进度填报整理 | 汇总日报、周报和任务反馈，形成进度状态。 | progress_summary, delayed_tasks, status_table |
| PM05_risk_warning | 项目风险预警 | 识别延期、资源不足、质量、范围、客户确认和验收风险。 | risk_register, risk_level, response_suggestions |
| PM06_weekly_report_generate | 项目周报生成 | 生成本周进展、问题风险、下周计划、需协调事项和管理摘要。 | weekly_report, management_summary, coordination_items |
| PM07_customer_communication_track | 客户沟通跟踪 | 整理客户反馈、待确认事项、回复建议和催办提醒。 | confirmation_list, reply_suggestions, reminders |
| PM08_delivery_archive | 交付物归档 | 按项目阶段归档交付物、验收材料、版本和审批记录。 | archive_index, acceptance_checklist, version_record |
| PM09_project_retro | 项目复盘 | 总结延期、质量、协同、客户沟通和交付经验，沉淀改进建议。 | retro_report, lessons_learned, improvement_actions |

## 4. 关键边界

- 可以生成草稿、建议、清单、摘要、风险提示和归档记录。
- 涉及范围变更、交付承诺、项目延期、客户正式回复、验收结论时必须人工确认。
- 演示样例必须使用脱敏或虚拟数据，不使用真实客户、员工、财务、合同或技术敏感信息。
- 所有 Hermes Agent skill 调用需要记录输入、输出、确认人和归档位置。

## 5. 文件结构

```text
project-management-assistant/
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
