## Description: <br>
Scans personal to-dos, calendar summaries, and deadline notes to identify upcoming deadline risks and scheduling conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and personal productivity agents use this skill to turn supplied task lists, meeting summaries, and deadline notes into a reviewable deadline-risk brief with conflicts, omissions, rescheduling suggestions, and a daily action list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs may contain personal scheduling details or other sensitive material. <br>
Mitigation: Use the skill only on files intended for analysis, minimize unnecessary personal details, and redact sensitive content when possible. <br>
Risk: Incomplete task or calendar data can produce misleading deadline or conflict summaries. <br>
Mitigation: Keep the review-first workflow, verify detected deadlines and conflicts, and preserve explicit confirmation items when information is missing. <br>
Risk: The helper can write to a user-provided output path. <br>
Mitigation: Check the --output path before running the helper and use --dry-run when reviewing behavior. <br>
Risk: The bundled script contains unused generic audit utilities. <br>
Mitigation: Review artifact/scripts/run.py before installation when strict minimal code is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/personal-deadline-radar) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Structured Output Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown by default, with optional JSON from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review-first output; the local helper reads supplied files or directories and does not modify external systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
