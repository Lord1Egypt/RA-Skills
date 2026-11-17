## Description:

Narrative Memory helps an agent capture meaningful life events as structured personal narrative records using layered filtering, signal detection, pattern recognition, and decision reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to identify milestones, decisions, values, emotional turning points, first experiences, and reflections from text, then store and review them as a personal narrative memory timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store personal reflections, emotional context, values, and decision history as plaintext local files.

Mitigation: Use it only with informed consent, avoid highly sensitive entries, restrict filesystem access to the .soul directory, and add external encryption or access controls where needed.

Risk: Documented privacy protections may overstate what the reviewed code implements.

Mitigation: Treat stored memories as plaintext records, verify retention and deletion procedures outside the skill, and review the code before relying on privacy claims.

Risk: Automatic signal processing may capture content the user did not intend to preserve.

Mitigation: Require explicit confirmation before automatic capture and review generated narrative records before retaining them.

Risk: Runtime dependencies may be outdated by the time of installation.

Mitigation: Update and audit dependencies before use, then rerun security scanning in the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaoguoqiang-hub/skills/narrative-memory)
- [Narrative Guidelines](references/narrative-guidelines.md)
- [Narrative Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown guidance, JSON configuration, and JSONL narrative records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the scripts persist narrative, accumulation, daily-context, user-values, and configuration files under ~/.openclaw/workspace/.soul.]

## Skill Version(s):

0.6.0 (source: server release metadata; artifact/package.json reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
