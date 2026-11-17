## Description:

Human-as-a-Service for OpenClaw - Dispatch verified human agents to perform physical world tasks and sensory validation

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Human-Rent to let an agent dispatch paid, verified human workers for physical-world tasks such as photo evidence, address checks, equipment inspections, phone calls, and document scans.

### Deployment Geography for Use:

United States (select cities)

## Known Risks and Mitigations:

Risk: The skill can create paid real-world tasks and requires API credentials.

Mitigation: Install only when the publisher is trusted, store credentials in a secret manager or a 0600 environment file, and keep explicit confirmation enabled for normal use.

Risk: The security review says the documentation includes an unsafe exec() agent-integration pattern.

Mitigation: Use argument-array process execution or a direct API wrapper instead of the documented exec() pattern.

Risk: Auto-confirm mode can bypass dispatch prompts for real-world tasks.

Mitigation: Leave HUMAN_RENT_AUTO_CONFIRM unset unless the account has tight spending limits and runs in a controlled environment.

## Reference(s):

- [ClawHub Human-Rent Skill Page](https://clawhub.ai/zhenstaff/skills/human-rent)
- [ZhenRent Documentation](https://docs.zhenrent.com)
- [ZhenRent API Credentials](https://www.zhenrent.com/api/keys)
- [ZhenRent API Endpoint](https://www.zhenrent.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON-like task/status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHENRENT_API_KEY and ZHENRENT_API_SECRET; may create paid real-world tasks after user confirmation.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter, package.json, and CHANGELOG report 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
