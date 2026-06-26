## Description: <br>
Helps agents turn home-lab or personal server change notes into structured, reviewable ops logs with summary, prior state, actions, observations, rollback plan, and follow-up tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and home-lab operators use this skill to convert change notes, machine context, results, and risks into audit-friendly Markdown drafts for review, rollback planning, and follow-up tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python helper can read user-selected local inputs and write to a user-selected output path. <br>
Mitigation: Use intended change-log inputs, review the output path before writing, and use dry-run or stdout output when file writes are not needed. <br>
Risk: Home-lab logs can contain sensitive hostnames, tokens, passwords, or private infrastructure details. <br>
Mitigation: Redact sensitive infrastructure and credential details before providing inputs or sharing generated logs. <br>
Risk: Generated operations logs may omit missing facts or present draft follow-up actions that still require human review. <br>
Mitigation: Review the draft, resolve listed confirmation items, and verify rollback details before using the output as an operational record. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/home-lab-ops-log) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown drafts, optional JSON reports, and local shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a chosen local output file when the bundled Python helper is run with --output.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
