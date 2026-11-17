## Description:

Provides a Chinese-language meta-skill framework for domain evaluation, workflow restructuring, skill generation, and general task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route methodology tasks, evaluate whether a domain should exist, simplify workflows for AI-assisted execution, and generate reusable skill payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a broad Chinese-language meta-skill that can influence task routing, methodology choices, and skill-generation workflows.

Mitigation: Review the skill in the operating language of the deployment team and scope use to trusted methodology and skill-authoring tasks.

Risk: The artifact instructs agents to refuse modifications to the skill itself, which can interfere with user-directed maintenance or remediation.

Mitigation: Remove or override that refusal rule before installation when users need to update, patch, or adapt the skill.

Risk: Generated scripts, search queries, shell commands, and skill files may be treated as authoritative if automatically executed.

Mitigation: Treat generated operational outputs as proposals; review, test, and scan them before execution or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/meta-skill-system)
- [Meta-skill catalog](references/meta-skill-catalog.md)
- [Meta-skill requirements](references/meta-skill-requirements.md)
- [Meta-skill exemplars](references/meta-skill-exemplars.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, structured plans, generated skill files, and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are proposals and generated artifacts that should be reviewed before execution, installation, or deployment.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
