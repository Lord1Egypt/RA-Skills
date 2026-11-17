## Description:

Calculates estimated China pension income through a web form and LLM-accessible MCP tools, including basic pension, enterprise annuity, personal pension, retirement savings, and retirement planning reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hikeryangsz-creator](https://clawhub.ai/user/hikeryangsz-creator)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to estimate retirement income under China pension assumptions, collect pension inputs through a browser UI, and generate concise retirement planning reports through an agent conversation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive pension and financial inputs may be stored in local files and exposed through unauthenticated HTTP endpoints.

Mitigation: Run the server only in a trusted local environment, restrict it to loopback, do not expose the port to a network, and avoid entering real financial data until access controls are added.

Risk: Readable local files and path handling can expand exposure if the web server is reachable by untrusted users.

Mitigation: Add authentication, explicit file allowlists, path traversal protections, and clear retention/delete controls before using the skill with real user data.

Risk: Pension estimates can be incomplete or outdated because policies, wages, returns, and user-provided assumptions may change.

Mitigation: Treat reports as planning estimates only and verify important retirement or financial decisions with current official sources or qualified advisors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hikeryangsz-creator/skills/pension-calculation)
- [Publisher profile](https://clawhub.ai/user/hikeryangsz-creator)
- [Skill documentation](artifact/SKILL.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, local web UI URL guidance, JSON data/status payloads, and short text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces estimates from user-provided pension inputs and can update selected numeric parameters before regenerating a report.]

## Skill Version(s):

1.3.0 (source: server release, package.json, CHANGELOG; artifact/SKILL.md frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
