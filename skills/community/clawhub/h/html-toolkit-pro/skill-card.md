## Description:

HTML 工具箱专业版 guides agents through full-site HTML, WCAG 2.1, component-rule, structured-data, and hreflang audits for local or authorized websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, accessibility reviewers, and web teams use this skill to plan and run HTML quality and WCAG audits, generate rule configurations, and summarize remediation findings for authorized sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive command-line and network-based site audits, which may reach unauthorized targets if the target URL is not approved.

Mitigation: Confirm authorization for each target and run audits only against local, owned, or contract-approved sites.

Risk: Authenticated crawling may expose credentials or sensitive site data if secrets are pasted into prompts, command lines, or reports.

Mitigation: Use environment variables or approved secret handling for credentials, and redact audit reports before sharing.

Risk: Broad trigger wording may cause the skill to be selected for tasks outside HTML quality and WCAG auditing.

Mitigation: Tighten deployment routing and usage descriptions to local or authorized HTML/WCAG audit work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/html-toolkit-pro)
- [Schema.org](https://schema.org)
- [Schema Markup Validator](https://validator.schema.org/validate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, HTML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce audit plans, command lines, configuration snippets, and structured JSON report examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
