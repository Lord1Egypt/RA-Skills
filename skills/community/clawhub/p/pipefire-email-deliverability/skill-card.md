## Description:

Free Pipefire tools check email deliverability across SPF, DKIM, DMARC, MX, blacklists, headers, DNS records, and cold email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikelovatt](https://clawhub.ai/user/mikelovatt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and email administrators use the skill to diagnose email and domain deliverability, review authentication and blacklist status, generate DNS records, and assess cold-email copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted email headers and drafts may contain personal or confidential information; release evidence provides no retention guarantees.

Mitigation: Use only information you are comfortable sharing with Pipefire, redact unnecessary personal or confidential details, and avoid submitting sensitive content.

## Reference(s):

- [Pipefire MCP server documentation](https://pipefire.ai/mcp-server)
- [Pipefire MCP server](https://pipefire.ai/mcp)
- [ClawHub skill listing](https://clawhub.ai/mikelovatt/skills/pipefire-email-deliverability)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Plain-English diagnostics and guidance, with DNS record text when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks use live DNS results; guessed email addresses are patterns, not verified addresses.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
