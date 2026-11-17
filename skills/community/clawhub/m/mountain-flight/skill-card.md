## Description:

Fly to mountains, search ski resort flights and highland city flights with alpine destination booking; also supports related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to search real-time flights to mountain, ski resort, highland, and alpine destinations, then present bookable options with altitude and fallback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global third-party flyai CLI if it is missing.

Mitigation: Require manual approval before installation and confirm the package source before allowing the agent to proceed.

Risk: Travel-search details may be sent to the flyai service during CLI execution.

Mitigation: Avoid submitting sensitive personal details and review the service handling requirements before use.

Risk: The skill can persist raw travel-query execution logs locally.

Mitigation: Disable, sanitize, or periodically remove local execution logs when queries may contain sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/mountain-flight)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel results with booking links, comparison tables, altitude notes, and concise fallback guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final responses should be based on real-time flyai CLI results and should not expose raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
