## Description: <br>
Homebase coordinates household calendars, morning briefings, school email intake, grocery and meal planning, restaurant tracking, medication logs, and trip preparation through an OpenClaw and WhatsApp workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hchawla](https://clawhub.ai/user/hchawla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External household users install this skill to let an OpenClaw agent help manage family logistics, including schedule summaries, school messages, meal planning, shopping lists, trip preparation, restaurant notes, and medication or symptom logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Google Calendar read/write access, Gmail read access for configured school senders, WhatsApp delivery through OpenClaw, and local storage of sensitive family and child health data. <br>
Mitigation: Review the configured OAuth scopes, WhatsApp targets, and scheduled messages before use; restrict permissions on .env, config.json, household/, and calendar_data/. <br>
Risk: Local state can include family calendars, kid profiles, meal history, restaurant notes, shopping lists, and medication or symptom logs. <br>
Mitigation: Run the skill under the intended local user account, keep state directories private on multi-user systems, and avoid committing generated household or calendar data. <br>
Risk: Weather and trip-preparation features may disclose location or trip context to Open-Meteo and to family WhatsApp recipients. <br>
Mitigation: Confirm the configured location, trip-detection behavior, and briefing recipients match the household's privacy expectations. <br>
Risk: Medication logging and dose-window reminders can affect health decisions. <br>
Mitigation: Keep child weights and medicine concentrations current, treat outputs as caregiver aids, and verify medication decisions with appropriate medical guidance. <br>


## Reference(s): <br>
- [Homebase ClawHub Skill Page](https://clawhub.ai/hchawla/homebase) <br>
- [hchawla Publisher Profile](https://clawhub.ai/user/hchawla) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Configuration Example](artifact/config.example.json) <br>
- [Google Calendar OAuth Scope](https://www.googleapis.com/auth/calendar) <br>
- [Gmail Read-Only OAuth Scope](https://www.googleapis.com/auth/gmail.readonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [WhatsApp-ready text, Markdown instructions, JSON-backed local state, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns household coordination outputs through OpenClaw; Python tools return data and formatted strings without bundled LLM calls.] <br>

## Skill Version(s): <br>
0.3.2 (source: ClawHub release evidence; artifact pyproject.toml reports 0.2.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
