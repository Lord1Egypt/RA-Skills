## Description:

Use this skill when assisting with FortressQuant's peerberry-sdk for PeerBerry investor automation, P2P lending education, and alternative-investment onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortressquant](https://clawhub.ai/user/fortressquant)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate guidance, Python snippets, shell commands, and configuration patterns for PeerBerry account access, portfolio monitoring, loan filtering, guarded purchase automation, exports, and SDK debugging. It is intended for technical and operational assistance, not financial advice or suitability recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may help generate automation that can place live PeerBerry investment purchases.

Mitigation: Keep read-only workflows first, require DRY_RUN for initial runs, set MAX_ORDERS and ticket-size caps, validate available funds, and require explicit approval before disabling dry-run mode.

Risk: The SDK can handle PeerBerry credentials, TOTP seeds, bearer tokens, and exported financial records.

Mitigation: Use isolated environments, avoid printing or committing secrets, use secure token storage, redact logs, and treat exported XLSX files as sensitive financial data.

Risk: The skill relies on an unofficial SDK and PeerBerry API behavior may change without notice.

Mitigation: Pin and review the package version, handle typed SDK exceptions, test with read-only calls after upgrades, and re-check method contracts against the included API reference.

## Reference(s):

- [API Quick Reference](references/api-quickref.md)
- [P2P Lending Primer](references/p2p-primer.md)
- [Task Recipes](references/task-recipes.md)
- [Peerberry SDK Documentation Index](docs/index.md)
- [Client API Reference](docs/api/client.md)
- [Authentication Guide](docs/guides/authentication.md)
- [Error Handling Guide](docs/guides/error-handling.md)
- [ClawHub Skill Page](https://clawhub.ai/fortressquant/skills/peerberry-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guarded real-money automation examples, read-only analysis snippets, troubleshooting steps, and references to SDK methods.]

## Skill Version(s):

1.0.0 (source: release metadata; pyproject.toml reports SDK package version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
