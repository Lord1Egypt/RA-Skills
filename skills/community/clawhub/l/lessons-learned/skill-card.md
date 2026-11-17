## Description:

zxyskill helps OpenClaw agents record mistakes and user preferences, maintain long-term memory files, and require confirmation before risky operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxygeitio](https://clawhub.ai/user/zxygeitio)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users can use this skill to add an agent-wide memory and lessons-learned layer that records preferences, mistakes, prohibited terms, and risk checks before actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to store user habits and generated rules in long-term memory without clear consent or scope limits.

Mitigation: Require confirmation before saving memories or rules, narrow triggers, and provide a way to inspect, edit, and delete stored entries.

Risk: Automatic memory extraction could capture quoted or third-party content as if it were the user's own preference.

Mitigation: Exclude quoted and third-party content from memory extraction and save only direct user preferences or explicitly approved rules.

Risk: Persisted lessons from failed operations could reinforce an incorrect rule after a transient or misdiagnosed error.

Mitigation: Review generated lessons before persistence and allow outdated or incorrect lessons to be edited or removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxygeitio/skills/lessons-learned)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and memory-file update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update long-term memory and lessons files when triggered.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
