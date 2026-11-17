## Description:

Safely install and run the bundled 00001 Grid Trading Bot in demo or sandbox mode, preview grid parameters, and generate paste-ready key=value or JSON configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frederica123](https://clawhub.ai/user/frederica123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, start, stop, and troubleshoot a local demo grid trading bot while keeping exchange credentials out of chat. It helps generate grid parameters for sandbox trading and requires confirmation before starting the strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local bot handles exchange API credentials in memory.

Mitigation: Use demo or testnet keys only, enter credentials only in the local page, and stop the server when finished.

Risk: Unauthenticated local controls can start or stop sandbox trading while the service is running.

Mitigation: Keep the service bound to 127.0.0.1, do not expose it through tunnels or port forwarding, and avoid visiting untrusted sites while it is running.

Risk: Trading results from demo or sandbox mode may be mistaken for live trading expectations.

Mitigation: Keep demo mode enabled and clearly state that sandbox results do not predict live performance or profits.

Risk: Runtime dependencies may change or carry their own vulnerabilities.

Mitigation: Review or update dependencies before use and run the bundled security test when evaluating the package.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/frederica123/skills/grid-trading-params-00001)
- [Publisher Profile](https://clawhub.ai/user/frederica123)
- [Bot README](artifact/bot/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, key=value configuration blocks, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid credentials, require explicit confirmation before starting the strategy, and keep trading guidance limited to demo or sandbox mode.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
