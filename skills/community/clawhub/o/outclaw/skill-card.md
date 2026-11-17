## Description:

Outclaw is a B2B outreach orchestrator that routes setup, research, style learning, campaign planning, reply handling, dashboards, and opt-out workflows while enforcing outreach guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milstan](https://clawhub.ai/user/milstan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate managed B2B outreach workflows, including lead research, campaign planning, message drafting, reply handling, and opt-out enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell commands and alter persistent OpenClaw configuration and AGENTS.md instructions.

Mitigation: Install only after reviewing the publisher and expected file changes; run with least-privilege workspace access and keep configuration backups.

Risk: The skill reads persistent user and organization context and stores complete lead batches locally, including in temporary files.

Mitigation: Use only in trusted environments, restrict access to local storage, avoid unnecessary sensitive lead data, and clear temporary files after use.

Risk: The release references sibling skills and shared scripts that were not included in the artifact evidence.

Mitigation: Review the complete installed Outclaw package, including sibling skills and shared scripts, before enabling outreach workflows.

## Reference(s):

- [Outclaw ClawHub listing](https://clawhub.ai/milstan/skills/outclaw)
- [Project homepage](https://github.com/leadbay/outclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with code blocks, generated outreach plans, status guidance, and local file or configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run shell commands and write local JSON, Markdown, memory, knowledge base, campaign, and configuration files when installed.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter reports 2.1.33)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
