## Description:

Has SM been in this token for weeks, or did they just enter? Are they still buying?

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Nansen token flow, holder, and trade data and summarize whether smart-money activity appears sustained, recent, reducing, or distributing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supported x402 payment challenge can spend funds from the configured wallet on each API call, including calls in loops.

Mitigation: Review wallet authorization, payment policy, and spending limits before research; keep repeated calls bounded.

Risk: The workflow requires an explicitly selected API key or saved browser session, and authentication or renewal can fail.

Mitigation: Check authentication status before research and stop on anonymous selection or authentication failure; follow the CLI guidance.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Guidance]

**Output Format:** [Nansen CLI commands and concise textual analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis is based on the selected token, chain, and returned flow, holder, and trade data.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
