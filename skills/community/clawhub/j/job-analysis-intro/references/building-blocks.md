# 工作分析方法的四大构件（Building Blocks）

设计或评估一项工作分析方法时，所有选择最终落在四类构件上：

1. **Kinds of job *data* collected**（收集什么类型的数据 = Descriptors）
2. **Methods of *gathering* data**（用什么方法收集）
3. **Sources of job analysis data**（数据来源是谁 / 什么）
4. **Units of *analysis*** — what gets analyzed，including 细节层级（如何汇总 / 切分数据）

> 课本还提到第五个隐性构件：**information management**（信息如何存储、流通、检索、更新）。

## 四块之间的关系

- 先定 **purpose**（见 `uses.md`）→ purpose 决定 descriptors → descriptors 部分决定 methods 与 sources → 最后选 units of analysis 来汇报。
- 但 **descriptors 和 units 会重合**。例：可以收 "work activities"（descriptor 12）却按 "worker characteristic requirements"（unit 6）汇总——用活动反推 KSAOs。
- 常见做法：收 duties 和 tasks 的数据，但按 *job dimensions* 聚类汇总（例："领导力"维度 = 分配工作 + 评价他人 + 辅助他人进步 这些任务的合集）。

## 教学脚手架

引入四块时，建议用**一个具体例子**跑完全流程。课本提供两个完整范例（详见 `examples.md`）：

1. **电力输配工（lineman）培训项目评估**
   - Purpose：showing how training content matched job requirements（内容效度证据）
   - Descriptors：tasks（#12）+ KSAOs（#13）
   - Methods：group interviews（SMEs 集体审核）+ reviewing records（历史任务清单）
   - Sources：supervisors, jobholders, trainer, planner analyst
   - Units：tasks, KSAOs, ratings thereof
   - 结果：242 个培训模块覆盖 385 个任务中的 93%，34 个 KSAOs 中的 79%。

2. **医院药房技术员（PT）最低任职资格（MQ）诉讼**
   - Purpose：developing **valid** minimum qualifications
   - Descriptors：tasks + KSAs（不含 Os，因人格等无法从申请表判断）
   - Methods：SME panels；发明了"Yes/No 是否连刚达标员工都需"的筛选尺度
   - Sources：job experts panels（tasks panel 6–9 人，KSAs panel 6–9 人）
   - Units：tasks, KSAs, scales applied to them；最终汇总为 6 套"MQ 档案"供替代原 MQ
   - 结果：原 MQ（两年协助执业药师经验）被替换为 6 种可选档案，扩大合格面而不牺牲效度，法院接受。

## 推导顺序（建议与学生共同走一遍）

当拿到一个实际问题时：
1. **问 purpose**：要解决哪一条 HR 问题？（对照 12 用途清单）
2. **问 descriptors**：这条 purpose 最关心哪些描述子？（对照 15 种）
3. **问 methods**：这些描述子最容易从哪种方法拿到？（对照 11 种）
4. **问 sources**：谁最有此信息？（对照 10 种来源）
5. **问 units**：交付物需要在什么粒度？（对照 10 种汇总单位）

> 课本反复提醒："the purpose we have in mind and our limits in terms of money, resources, and time will dictate the type of job analysis we do."

## Table 1.3（课本的"购物清单"）

| Descriptors (15) | Methods (11) | Sources (10) | Units (10) |
|---|---|---|---|
| 1. Organizational philosophy and structure | 1. Observing | 1. Job analyst | 1. Duties |
| 2. Licensing and other government-mandated requirements | 2. Interviewing individuals | 2. Jobholder's immediate supervisor | 2. Tasks |
| 3. Responsibilities | 3. Group interviews | 3. High-level executive or manager | 3. Activities |
| 4. Professional standards | 4. Technical conference | 4. Jobholder | 4. Elemental motions |
| 5. Job context | 5. Questionnaires | 5. Technical expert | 5. Job dimensions |
| 6. Products and services | 6. Diaries | 6. Organizational training specialist | 6. Worker characteristic requirements |
| 7. Machines, tools, equipment, work aids, and checklists | 7. Equipment-based methods | 7. Clients or customers | 7. Scales applied to units of work |
| 8. Work performance indicators | 8. Reviewing records | 8. Other organizational units | 8. Scales applied to worker characteristic requirements |
| 9. Personal job demands | 9. Reviewing literature | 9. Written documents | 9. Competencies |
| 10. Elemental motions | 10. Studying equipment design specifications | 10. Previous job analyses | 10. Qualitative vs. quantitative analysis |
| 11. Worker activities | 11. Doing the work | | |
| 12. Work activities | | | |
| 13. Worker characteristic requirements | | | |
| 14. Future changes | | | |
| 15. Critical incidents | | | |

明细分别见 `descriptors.md` / `methods.md` / `sources.md` / `units-of-analysis.md`。
