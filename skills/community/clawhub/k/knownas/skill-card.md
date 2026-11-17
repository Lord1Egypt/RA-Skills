## Description:

Give this OpenClaw a stable public name on knownas.dev: HTTPS, a public record of who runs it, and webhook and API addresses that survive tunnel restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[authecity](https://clawhub.ai/user/authecity)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw gateway owners and operators use this skill to set up, repoint, monitor, and remove a public knownAs.dev name and stable HTTPS routes for gateway APIs and channel webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An overly broad or exposed API key could allow unauthorized changes to public identity and routes.

Mitigation: Use a narrowly scoped, expiring KNOWNAS_API_KEY stored as a secret; never paste it into chat.

Risk: Incorrect public routes or webhook updates could expose or disrupt the gateway.

Mitigation: Review the intended public record and approve each route or webhook change before applying it.

Risk: Custom API destinations or secret-store commands could redirect credentials or secrets.

Mitigation: Do not set KNOWNAS_API_URL or KNOWNAS_SECRET_STORE_CMD unless the destination and command are trusted.

## Reference(s):

- [knownAs.dev](https://knownas.dev)
- [knownAs.dev FAQ](https://knownas.dev/faq.md)
- [knownas ClawHub release](https://clawhub.ai/authecity/skills/knownas)
- [Bundled FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports public identity and route addresses, verification outcomes, and traffic status.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
