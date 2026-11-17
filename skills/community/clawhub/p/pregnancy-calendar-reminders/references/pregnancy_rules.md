# 孕期提醒规则 / Pregnancy Reminder Rules

Use these rules as the canonical source for generating pregnancy reminder calendars. Treat all output as planning reminders, not medical diagnosis or individualized medical advice.

以下规则是生成孕期提醒日历的标准依据。所有输出只作为家庭计划和产检提醒，不作为诊断、处方或个体化医疗方案。

## 日期锚点 / Date Anchors

- If the user provides only the last menstrual period (LMP), calculate the estimated due date (EDD) as `LMP + 280 days`.
- 如果用户只提供末次月经日期，按 `预产期 = 末次月经 + 280天` 推算。
- If the user provides a doctor-adjusted due date after NT or another clinical assessment, treat that due date as authoritative and set an equivalent LMP anchor as `EDD - 280 days`.
- 如果用户提供 NT 或产检后的医生校正预产期，以医生日期为准，并将 `预产期 - 280天` 作为等效末次月经锚点。
- If both LMP and doctor-adjusted EDD are provided and they disagree, state the difference, use the doctor-adjusted EDD, and record the equivalent LMP in the outline/report.
- 如果同时提供 LMP 和医生预产期且不一致，说明相差天数，使用医生预产期生成新版日历，并在核对表中记录等效末次月经。
- Gestational age on a date is `(date - LMP_anchor)` expressed as weeks + days. The due date must be `40周+0天`; the 41-week follow-up date must be `EDD + 7 days`.
- 任意日期孕周按 `(日期 - 末次月经锚点)` 换算为周+天。预产期必须是 `40周+0天`；41周复诊提醒为 `预产期 + 7天`。

## 核心产检窗口 / Core Medical Windows

Calculate windows from the active LMP anchor. 所有窗口都从当前生效的末次月经锚点换算：

| 窗口 / Window | 开始 / Start | 结束 / End | 提醒重点 / Reminder Focus |
| --- | --- | --- | --- |
| 早孕确认期 / Early pregnancy confirmation | 5周+0天 | 8周+0天 | 预约产科门诊；按医生安排早孕超声，确认宫内妊娠及胚胎发育；出血或腹痛及时就诊。Schedule obstetric visit and early ultrasound per doctor; seek care for bleeding or abdominal pain. |
| 首次系统产检/建档 / First checkup and registration | 6周+0天 | 13周+6天 | 13周+6前建档，完成首次产检、风险评估和基础化验。Establish records/registration and complete baseline checkup/labs. |
| NT筛查窗口 / NT ultrasound | 11周+0天 | 13周+6天 | 完成 NT 超声，讨论后续产前筛查/诊断路径；NT 与 NIPT 不是同一项。Complete NT and discuss screening/diagnosis pathway. |
| 无创DNA适用窗口 / NIPT applicable window | 12周+0天 | 22周+6天 | NIPT 是血液筛查，需正规机构、知情同意和产科指导。NIPT is a blood screening test under informed consent and obstetric guidance. |
| 孕中期随访 / Mid-pregnancy follow-up | 14周+0天 | 19周+6天 | 常规产检；按医生方案做血清学筛查或相关评估。Routine follow-up and screening as directed. |
| 胎儿系统超声 / Fetal anatomy ultrasound | 20周+0天 | 24周+0天 | 完成胎儿结构筛查超声，建议提前预约。Complete anatomy ultrasound; book early. |
| 妊娠期糖尿病筛查 / Gestational diabetes screening | 24周+0天 | 28周+0天 | 通常为 75 g OGTT；按医院要求准备，不擅自节食“控结果”。Usually 75 g OGTT; follow hospital prep instructions. |
| 生长评估期 / Growth assessment | 29周+0天 | 32周+0天 | 常规随访；医生按情况评估胎儿生长、胎位、羊水。Assess growth, position, and amniotic fluid as arranged. |
| 孕晚期准备 / Late pregnancy preparation | 33周+0天 | 36周+6天 | 关注胎动、血压、临产风险；GBS、胎心监护等按医院安排；准备证件、住院包和路线。Prepare for delivery and follow late-pregnancy monitoring plan. |
| 足月待产 / Full-term waiting period | 37周+0天 | 41周+0天 | 按产科频率复诊；评估胎动、宫缩、胎心和分娩时机；超过预产期听医生安排。Follow obstetric visit frequency and delivery timing guidance. |

## 每日提醒内容 / Daily Reminder Content

Include stable daily reminders, stage-adapted. 每日提醒应包含长期稳定事项，并根据孕周调整：

- Medication/supplement safety: folic acid or prenatal vitamins per doctor; in early pregnancy check folic acid content and avoid duplicate excess intake.
- 药物和补充剂安全：叶酸或孕妇复合维生素按医嘱；孕早期核对叶酸含量，避免重复超量。
- Danger signs: vaginal bleeding, persistent or severe abdominal pain, fainting/significant dizziness, severe vomiting with inability to eat/drink, fever, dyspnea, chest pain, or marked discomfort require prompt medical contact.
- 危险信号：阴道出血、持续或剧烈腹痛、晕厥/明显头晕、严重呕吐无法进食饮水、发热、呼吸困难、胸痛或明显不适，应尽快联系产科或就医。
- Food/lifestyle baseline: avoid alcohol, smoking, and secondhand smoke; fully heat meat, eggs, seafood; maintain food hygiene; count caffeine from coffee, tea, energy drinks, and chocolate and keep it under 200 mg/day unless doctor says otherwise.
- 饮食生活底线：避免酒精、吸烟和二手烟；肉蛋水产充分加热；注意食品卫生；咖啡因总量通常控制在每天 200 mg 以下，除非医生另有要求。
- Activity: low-risk pregnancy can usually continue moderate activity as tolerated; start gently if previously inactive; avoid high fall-risk, collision-heavy, or exhausting activities.
- 活动：低风险妊娠通常可在身体允许下适量活动；此前无运动习惯者从温和活动开始；避免易摔倒、强对抗或过度疲劳项目。
- Heat: avoid overheating, sauna, and very hot baths, especially in early pregnancy.
- 体温：避免过热、桑拿和过热热水浴，尤其在孕早期。
- Father's checklist: keep exam reports, maternal-child handbook, symptoms, medication/supplement list, and questions for the doctor organized before each appointment.
- 准爸爸清单：产检前整理检查单、母子健康手册、近期症状、药物/保健品清单和想问医生的问题。
- In late pregnancy, add fetal movement reminder: learn the baby's usual movement pattern; if movement is clearly reduced, absent, or very different, contact obstetrics instead of long home observation.
- 孕晚期加入胎动提醒：了解宝宝日常胎动规律；明显减少、消失或和平时显著不同，不要在家长时间观察，应联系产科。

## 关键事件提醒 / Key Event Reminders

Generate key events at the start and near the end of clinically important windows when those dates are on or after the calendar start date.

在关键产检窗口开始和临近结束时生成关键提醒；如果日期早于日历开始日期，则跳过过去事件。

- Current-day anchor summary / 当前孕周与待办核对。
- Early pregnancy confirmation start/end / 早孕确认期开始和结束。
- NT start and 13周+6 end / NT 开始和 13周+6 截止。
- NIPT start and 22周+6 end / NIPT 开始和 22周+6 截止。
- Fetal anatomy ultrasound start / 系统超声窗口开始。
- OGTT start and 28周 end / 糖耐窗口开始和 28周截止。
- Growth assessment start / 生长评估开始。
- Late pregnancy preparation start / 孕晚期准备开始。
- Full-term waiting period start / 足月待产开始。
- Due date / 预产期。
- 41-week follow-up / 41周复诊提醒。

For future key events, use display alarms at 7 days before, 1 day before, and event time when applicable. For current-day events, use event-time alarm only.

未来关键事件默认设置提前 7 天、提前 1 天和事件当时提醒；当天事件只设置当时提醒。

## 校验清单 / Validation Checklist

Every generated calendar must pass these checks before delivery. 每次生成日历，交付前必须通过：

- `EDD - LMP_anchor == 280 days`.
- Gestational age on EDD is `40周+0天` / 预产期当天是 `40周+0天`。
- End date is `41周+0天` / 结束日期是 `41周+0天`。
- Every window start/end matches the table above / 所有产检窗口起止日期与上表一致。
- No generated event is before the requested calendar start unless the user explicitly requested past reminders / 除非用户明确要求历史版，否则不生成开始日期之前的事件。
- Event UIDs are unique / 事件 UID 不重复。
- `BEGIN:VEVENT` and `END:VEVENT` counts match in the `.ics`.
- The generated JSON/report event count matches the `.ics` event count / JSON/报告事件数与 `.ics` 一致。
- The outline records input LMP, doctor-adjusted due date if any, active LMP anchor, EDD, timezone, daily reminder time, event count, and key windows / 核对表记录输入 LMP、医生校正预产期、实际锚点、预产期、时区、每日提醒时间、事件数和关键窗口。

## 日历同步安全 / Calendar Sync Safety

- Prefer producing a versioned `.ics` file and instructing the user to import it into an iCloud calendar for phone sync.
- 优先生成带版本的 `.ics` 文件，并让用户导入 iCloud 日历以同步手机。
- When modifying live macOS Calendar, request approval and only touch calendars whose names clearly match the pregnancy reminder calendar created by this workflow.
- 直接修改 macOS Calendar 时必须请求权限，只操作名称明确匹配的孕期提醒日历。
- Do not delete old calendars unless the user explicitly asks. When deleting, match the exact family marker and preserve unrelated calendars.
- 未经用户明确要求不要删除旧日历；删除时必须精确匹配孕期提醒标记，保留无关日历。
