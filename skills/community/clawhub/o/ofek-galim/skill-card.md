## Description: <br>
Check, monitor, and summarize student homework/tasks from Webtop (SmartSchool), Galim Pro, and Ofek. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaike1](https://clawhub.ai/user/shaike1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents or authorized caretakers use this skill to fetch, review, and summarize children's school tasks from Webtop, Galim Pro, and Ofek. It can also support local reminders by syncing Galim due dates into a configured Google Calendar. <br>

### Deployment Geography for Use: <br>
Israel <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles children's school account credentials and task details. <br>
Mitigation: Install and run it only when authorized, keep credentials in a local restricted env file, and avoid exposing raw command output or env values. <br>
Risk: Calendar sync can write homework details to Google Calendar, including the default primary calendar if left unchanged. <br>
Mitigation: Use a dedicated restricted calendar, set OFEK_GALIM_CALENDAR_ID explicitly, and run sync with --dry-run before enabling writes. <br>
Risk: Combined Webtop reporting depends on an external local Webtop helper. <br>
Mitigation: Review that helper before relying on combined reports and treat Webtop failures separately from Galim or Ofek results. <br>
Risk: Automated WhatsApp or daily report flows may send children's task information to a group. <br>
Mitigation: Enable automation only after confirming the destination group and reviewing exactly what data is sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaike1/ofek-galim) <br>
- [Environment credentials format](references/env-example.md) <br>
- [Ofek students portal](https://students.myofek.cet.ac.il/he) <br>
- [Galim Pro task portal](https://lms.galim.org.il/personal?lang=he) <br>
- [Google Calendar API](https://www.googleapis.com/calendar/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Hebrew plain text or Markdown summaries, optional JSON reports, and calendar sync result JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Google Calendar events when the sync command is used; otherwise outputs task reports and setup guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
