## Description:

LYGO Automation Workflows is a consent-aware playbook and local planner for identifying repetitive steward tasks worth automating, designing trigger-action workflow plans, and choosing local-first tools before SaaS automation platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers, operators, and automation stewards use this skill to audit recurring tasks, compare local-first workflow tools, and produce consent-aware workflow plan JSON before implementing automations that may touch vendors, CRM systems, or personal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow plans may be implemented against real vendors, CRMs, payment systems, or tools that handle personal data.

Mitigation: Review generated plans before implementation, require steward consent for each vendor connection, minimize data fields, and use least-privilege access.

Risk: External automation implementations or separately advertised full zip contents are outside the reviewed release evidence.

Mitigation: Treat external packages as separate artifacts and review or scan them before connecting accounts, credentials, or production systems.

Risk: Optional local planner file output could create local artifacts without sufficient user intent.

Mitigation: Keep writes gated behind both --write and --i-consent, and review any generated JSON before use.

## Reference(s):

- [Security review](references/SECURITY.md)
- [SkillSpector audit](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)
- [ClawHub listing](https://clawhub.ai/deepseekoracle/lygo-automation-workflows)
- [Project homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-automation-workflows)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with optional local CLI output as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local planner writes files only when --write is combined with --i-consent.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
