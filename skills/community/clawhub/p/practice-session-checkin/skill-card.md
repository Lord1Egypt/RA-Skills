## Description: <br>
Public-safe practice session intake, start confirmation, reminder flow, completion check, and follow-up tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoma970](https://clawhub.ai/user/guoma970) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to coordinate generic practice-session check-ins: record a task, confirm start time, send short reminders, check completion, and track unfinished follow-up without adding private assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Practice reminders could expose identifying details if users include real names, institution names, account IDs, health details, child-identifying information, or private schedules tied to identity. <br>
Mitigation: Use generic task descriptions and remove identity-specific or sensitive details before publishing or sharing examples. <br>
Risk: The assistant could overstep by inventing missing practice details, assuming a start time, or marking completion without confirmation. <br>
Mitigation: Ask one short clarification question for missing details, confirm start time before reminders, and record completion or follow-up only after user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoma970/practice-session-checkin) <br>
- [README](artifact/README.md) <br>
- [Customization Guide](artifact/CUSTOMIZATION.md) <br>
- [Examples](artifact/examples/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Release notes v1.0.1](artifact/releases/1.0.1.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise conversational text and markdown task-status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reminder and check-in flow; no tool, credential, or privileged-access requirements were identified.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, changelog, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
