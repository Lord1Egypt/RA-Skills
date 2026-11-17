## Description:

灵枢·Agent设计师 helps users design industry-specific AI Agent plans, create runnable baseline Agents from configuration and dedicated skill packages, and plan enterprise Agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and teams use this skill to convert customer requirements, enterprise descriptions, websites, documents, or industry reports into a 7-part Agent scenario outline, MVP rollout guidance, baseline OpenClaw configuration, and dedicated skill-package plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish workflow can rewrite a GitHub main branch and publish externally with too little scoping.

Mitigation: Use the skill for planning and design unless the release commands have been manually audited; remove forced push behavior, verify the repository and branch, and allowlist staged files before publishing.

Risk: Enterprise descriptions, websites, documents, or industry reports may contain sensitive business information.

Mitigation: Process sensitive enterprise inputs only with explicit approval, avoid external publication of private material, and keep human review on governance and data-sharing boundaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/lingshu-agent-architect)
- [Artifact README](artifact/README.md)
- [Root skill definition](artifact/SKILL.md)
- [Ling Shu Agent Designer skill definition](artifact/ling-shu-agent-designer/SKILL.md)
- [Enterprise Agent Planner skill definition](artifact/enterprise-agent-planner/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans, configuration snippets, file manifests, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Agent workspace files and publish commands when explicitly confirmed by the user.]

## Skill Version(s):

1.4.0 (source: server release metadata, root SKILL.md frontmatter, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
