## Description:

Install and use lnget, a Lightning-native HTTP client with automatic L402 payment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to install and operate lnget for HTTP requests that may require Lightning L402 micropayments, including downloading paid resources, managing cached tokens, checking Lightning backend status, and configuring payment limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real Lightning payments when fetching L402-protected resources.

Mitigation: Use --no-pay first, set conservative --max-cost and --max-fee limits, and keep wallet balances low for automated use.

Risk: The documented LND configuration example points to an admin macaroon, which may grant broader node access than the workflow needs.

Mitigation: Prefer least-privilege Lightning credentials or a limited wallet instead of an LND admin macaroon.

Risk: The default installer path uses an unpinned remote Go module version.

Mitigation: Install only a pinned, reviewed lnget version before using the skill in production workflows.

Risk: Cached L402 tokens and persisted LNC sessions can retain payment authorization state after use.

Mitigation: Periodically clear cached tokens and revoke unused LNC sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roasbeef/skills/lnget)
- [lnget upstream project named in artifact](https://github.com/lightninglabs/lnget.git)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation steps, payment-control options, token-management commands, and Lightning backend configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
