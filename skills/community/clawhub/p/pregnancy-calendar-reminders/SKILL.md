---
name: pregnancy-calendar-reminders
description: 生成、核对、更新并协助导入完整孕期提醒日历；Generate, verify, update, and help import full pregnancy reminder calendars from a last menstrual period date/LMP or a doctor-adjusted due date after NT/prenatal checkups. Use when Codex needs to calculate an estimated due date, convert gestational weeks into concrete dates, create .ics calendar reminders, revise an existing pregnancy calendar after the doctor changes the due date, check pregnancy calendar dates, or guide iCloud/iPhone calendar sync.
---

# 孕期日历提醒 / Pregnancy Calendar Reminders

## 核心流程 / Core Workflow

Use this skill to produce a checked `.ics` pregnancy reminder calendar. Prefer the bundled generator over manual date arithmetic.

使用本 skill 生成经过核对的 `.ics` 孕期提醒日历。不要手工心算孕周和日期，优先使用内置脚本。

1. 收集日期锚点 / Collect the anchor date.
   - 如果用户只提供末次月经日期，使用 `预产期 = 末次月经 + 280天`。
   - If the user provides only LMP, use `EDD = LMP + 280 days`.
   - 如果用户提供 NT 或产检后的医生校正预产期，以医生日期为准，并使用 `等效末次月经 = 预产期 - 280天`。
   - If the user provides a doctor-adjusted due date, treat it as authoritative and use `equivalent LMP = EDD - 280 days`.
   - 如果 LMP 和医生预产期同时提供且不一致，说明相差天数，使用医生预产期生成新版日历。
   - If both LMP and doctor-adjusted EDD are provided and disagree, state the day difference and use the doctor-adjusted due date.
2. 决定日历范围 / Decide the import range.
   - 默认从今天生成到 `41周+0天`，避免手机里出现大量过去提醒。
   - Default to reminders from today through `41周+0天`.
   - 如果用户明确要完整历史版，从孕期锚点开始生成，传入 `--include-past`。
   - If the user wants a full historical archive, pass `--include-past`.
3. 使用 `scripts/generate_pregnancy_calendar.py` 生成文件 / Generate files.
4. 读取 `_validation.json` 和 `_outline.md` 后再交付 / Read validation and outline before delivery.
5. 交付 `.ics`、核对表和简洁同步说明 / Deliver the `.ics`, outline, and sync instructions.

## 必读参考 / Required Reference

Read `references/pregnancy_rules.md` before changing date-window logic, explaining the medical windows, or investigating validation failures.

在修改日期窗口、解释产检安排、排查校验失败时，必须先读 `references/pregnancy_rules.md`。脚本逻辑和参考规则要保持一致。

## 生成器 / Generator

Run from any writable output directory. 在任意可写目录运行：

```bash
python /Users/wufei/.codex/skills/pregnancy-calendar-reminders/scripts/generate_pregnancy_calendar.py \
  --lmp 2026-04-20 \
  --output-dir ./pregnancy-calendar-output
```

Doctor-adjusted due date after NT. NT/产检后医生校正预产期：

```bash
python /Users/wufei/.codex/skills/pregnancy-calendar-reminders/scripts/generate_pregnancy_calendar.py \
  --lmp 2026-04-20 \
  --doctor-due 2027-01-25 \
  --output-dir ./pregnancy-calendar-output
```

常用参数 / Useful options:

- `--start YYYY-MM-DD`: 指定提醒开始日期 / start reminders on a specific date.
- `--include-past`: 从孕期锚点开始生成完整历史版 / generate from the LMP anchor.
- `--daily-time HH:MM`: 每日提醒时间，默认 `20:30` / daily reminder time.
- `--key-time HH:MM`: 关键产检提醒时间，默认 `09:00` / key event time.
- `--calendar-name "..."`: 设置 `.ics` 中显示的日历名称 / set calendar display name.
- `--prefix name`: 修改输出文件名前缀 / change output filename prefix.

脚本输出 / Script outputs:

- `.ics`: 可导入日历文件 / importable calendar file.
- `.json`: 事件明细 / generated event data.
- `_outline.md`: 人类可读的孕周、预产期、产检窗口核对表 / human-readable summary.
- `_validation.json`: 输入、事件数、文件路径和校验结果 / validation report.

## 强制核对 / Non-Negotiable Checks

Before answering the user, confirm all of these from `_validation.json` and/or the outline.

给用户回复前，必须从 `_validation.json` 或核对表确认：

- `validation_passed` is `true` / 校验结果为 `true`。
- Active LMP anchor and due date are recorded / 实际孕周锚点和预产期已记录。
- Due date is `40周+0天` / 预产期当天必须是 `40周+0天`。
- End date is `41周+0天` / 日历结束日期必须是 `41周+0天`。
- Key windows are present / 关键窗口齐全：NT、NIPT、系统超声、糖耐、胎儿生长评估、孕晚期准备、足月待产。
- `.ics` event count matches the JSON/report event count / `.ics` 事件数和 JSON/报告一致。
- The calendar name is versioned by due date when updating an old calendar / 更新旧日历时，日历名需带预产期版本。

If validation fails, fix the script/input and regenerate. Do not deliver a failed calendar.

如果校验失败，修正输入或脚本后重新生成，不要交付失败日历。

## 日历导入与手机同步 / Calendar Import And Phone Sync

Prefer delivering the `.ics` and asking the user to import it into an iCloud calendar.

默认交付 `.ics`，建议用户导入 iCloud 日历：

1. 在 Mac 上打开 `.ics` 文件 / Open the `.ics` on Mac.
2. 导入弹窗里选择 iCloud 日历，不要选“在我的 Mac 上” / choose an iCloud calendar, not "On My Mac".
3. 在 iPhone 打开 `设置 > Apple ID > iCloud > 日历` / enable iCloud Calendar on iPhone.
4. 在 iPhone 日历 App 中确认该日历已勾选 / make sure the calendar is checked.

When the user asks Codex to directly modify macOS Calendar:

当用户要求直接修改 macOS 日历：

- Request sandbox escalation for `open`/`osascript` / 需要请求权限。
- Only touch calendars whose names clearly match the pregnancy reminder calendar created by this workflow / 只操作名称明确匹配的孕期提醒日历。
- Do not delete older pregnancy calendars unless the user explicitly asks / 未经明确要求，不删除旧版。
- After import/delete, read the calendar list and verify event counts / 导入或删除后读取日历列表并核对事件数。

## 安全说明 / Safety Notes

Use cautious language: this calendar is for family planning, appointment preparation, and reminders. It does not replace diagnosis, prescriptions, or individualized hospital plans.

保持谨慎表述：本日历只用于家庭计划、预约准备和提醒，不替代医生诊断、处方或医院个体化安排。任何危险症状提醒都应建议用户及时联系产科或就医。
