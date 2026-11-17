## Description:

Auto-diagnose agent failures, extract reusable recovery patterns, and create local skills to fix recurring blockers while keeping all data private and local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Phoenix Loop to diagnose recurring blocked or failed tasks, extract reusable recovery patterns, and create local recovery skills while keeping memory and skill data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter an agent reusable skill set and memory over time.

Mitigation: Require manual review before writes to skills/local/, memory files, or HEARTBEAT.md, and before enabling any generated recovery skill.

Risk: Memory and task logs may contain sensitive or untrusted content.

Mitigation: Apply the documented privacy checklist and verify redaction before storing or reusing failure patterns.

## Reference(s):

- [Phoenix Loop ClawHub page](https://clawhub.ai/dalomeve/skills/phoenix-loop)
- [Privacy Security Checklist](artifact/references/privacy-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline command and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local writes to memory files, HEARTBEAT.md, and skills/local/ recovery files; review before applying.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
