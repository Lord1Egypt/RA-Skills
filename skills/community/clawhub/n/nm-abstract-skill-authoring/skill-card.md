## Description:

Guide creating Claude Code skills with TDD and persuasion principles. Use for new skill development

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers authoring Claude Code skills use this guide to design skill content, descriptions, modular documentation, and validation workflows. It covers TDD-based skill development, testing, troubleshooting, and deployment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an authenticated network request whose purpose may be unclear.

Mitigation: Review the request and establish its purpose before installing the skill.

Risk: Deployment guidance could replace existing files without a clear pre-replacement check.

Mitigation: Review deployment steps and check target files before replacing them.

Risk: Testing workflows may replay or store real prompts containing sensitive information.

Mitigation: Review and sanitize prompts before replaying or storing them.

Risk: Security scan coverage is incomplete because some referenced paths were missing.

Mitigation: Treat the security evidence as incomplete and review the available files before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-abstract-skill-authoring)
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with code examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies with the skill being authored.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
