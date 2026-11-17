## Description:

Discover Ghost payment requirements, execute real x402 calls, report x402 settlements, and run GhostWire quote, prepare, and status flows for direct escrow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghostprotoinfra](https://clawhub.ai/user/ghostprotoinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect OpenClaw agents to Ghost Protocol payment discovery, x402 paid requests, settlement reporting, and GhostWire escrow job flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real wallet signing keys for paid x402 calls and settlement reporting.

Mitigation: Install only in a trusted server runtime, keep the signer key in protected secret storage, never pass it on the command line, and use a dedicated low-balance key.

Risk: Live requests can spend funds or prepare payment-related GhostWire transaction data.

Mitigation: Prefer dry-run first, use only approved service slugs and merchant roles, and restrict base URLs to trusted HTTPS Ghost endpoints.

Risk: The npm dependency graph participates in payment and signing flows.

Mitigation: Review and pin dependencies before using the skill for real payments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghostprotoinfra/skills/openclaw-ghost-pay)
- [ClawHub publisher profile](https://clawhub.ai/user/ghostprotoinfra)
- [Project homepage](https://github.com/Ghost-Protocol-Infrastructure/GHOST_PROTOCOL/tree/main/integrations/openclaw-ghost-pay)
- [README.md](README.md)
- [INSTALL.md](INSTALL.md)
- [QUICKSTART.md](QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can call Ghost HTTPS endpoints, perform x402 payment flows, and emit structured JSON success or error payloads.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
