## Description:

Answer Monobank balance questions by calling the Monobank API directly with a user-supplied per-request API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftadviser](https://clawhub.ai/user/swiftadviser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Monobank balance questions by calling Monobank's API with a user-supplied token and returning concise masked balance summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Monobank API token can expose private balance data if reused, logged, stored, or shared outside the request that needs it.

Mitigation: Provide the token only for intentional balance retrieval, avoid placing it in visible commands or logs, and do not store it in files, environment variables, summaries, or future context.

Risk: Balance responses may reveal sensitive financial identifiers or account details.

Mitigation: Return only masked account labels and omit raw account IDs, send IDs, full IBANs, client IDs, webhook URLs, raw API errors, and token material.

## Reference(s):

- [Monobank API client-info endpoint](https://api.monobank.ua/personal/client-info)
- [Monobank API token page](https://api.monobank.ua/)
- [Skill homepage](https://monobank-mcp.mandate.md)
- [ClawHub skill page](https://clawhub.ai/swiftadviser/skills/monobank)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Concise Markdown or plain text balance summary, Ukrainian by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks account labels and avoids exposing tokens, raw account IDs, full IBANs, client IDs, send IDs, or webhook URLs.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
