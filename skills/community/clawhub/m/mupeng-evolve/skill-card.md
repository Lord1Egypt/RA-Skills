## Description:

Mupeng Evolve guides agents through self-evolution, file-based memory, revenue tracking, communication policy gates, and identity calibration without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a structured autonomy loop for memory maintenance, self-improvement proposals, revenue workflow tracking, communication gating, and identity calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to repeatedly modify memory, tools, skills, heartbeat routines, SOUL.md, AGENTS.md, and permanent memory with insufficient approval boundaries.

Mitigation: Keep tool, skill, heartbeat, SOUL.md, AGENTS.md, and permanent memory changes approval-only, and review diffs before writes.

Risk: Autonomous memory, identity, and routine changes can persist unwanted behavior across sessions.

Mitigation: Document how to disable hooks and roll back memory or identity changes before installing the skill.

Risk: Running the skill on untrusted messages may amplify prompt-injection or unsafe automation requests.

Mitigation: Avoid running it on untrusted messages and require human review for external communication or automation changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/mupeng-evolve)
- [ClawHub publisher profile](https://clawhub.ai/user/mupengi-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, YAML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; advises file-based memory, logging, communication policy gates, and approval controls for sensitive agent changes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
