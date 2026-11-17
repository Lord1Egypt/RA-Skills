## Description:

Max Banking lets an agent connect to a Max Bank account, check balances, create PIX payment requests, pay boletos, and process PIX or boleto codes from text or images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonatancosta](https://clawhub.ai/user/jonatancosta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to operate Max Bank workflows through OpenClaw, including balance lookup, account pairing, PIX payment request creation, boleto payment request creation, and local QR or barcode extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real MaxBank PIX and boleto payment requests from pasted codes, QR images, or barcode images.

Mitigation: Install only after review, require explicit final confirmation before each payment request, and validate recipient and amount before execution.

Risk: Account pairing stores a long-lived local banking credential and configures MCP access for future sessions.

Mitigation: Protect the local secrets directory, rotate or revoke the credential when no longer needed, and avoid shared machines for paired accounts.

Risk: Setup modifies OpenClaw permissions and installs or configures dependencies used for command execution and hosted MCP calls.

Mitigation: Review permission changes before setup, pin dependencies where possible, and restrict MCP endpoints to trusted HTTPS hosts.

Risk: Diagnostic behavior can expose session configuration or credential metadata.

Mitigation: Remove or restrict debug output before production use and avoid sharing command logs from paired environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonatancosta/skills/max-banking)
- [Publisher profile](https://clawhub.ai/user/jonatancosta)
- [Max website](https://max.com.br)
- [MaxBank MCP health check](https://maxbank-mcp.max.com.br/health)
- [Homepage](https://github.com/maxter/mcp-payment-skill)
- [Support](https://github.com/maxter/mcp-payment-skill/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown and natural-language responses with internal shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create real banking payment requests and may store a long-lived local banking credential after account pairing.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
