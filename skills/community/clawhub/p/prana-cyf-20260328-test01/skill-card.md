## Description:

This skill exposes a Prana-hosted TradingView and Pine Script indicator analysis capability through Node.js and Python clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyffeifeifei](https://clawhub.ai/user/cyffeifeifei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit TradingView and Pine Script technical indicator analysis requests to a hosted Prana service from OpenClaw. The packaged clients provide Node.js and Python execution paths for forwarding prompts and receiving remote results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, trading context, and API credentials are sent to the Prana service at claw-uat.ebonex.io.

Mitigation: Use the skill only with data appropriate for that service; avoid private strategies, account data, and secrets in messages.

Risk: The clients can automatically fetch API keys and persist fetched credentials to local config files.

Mitigation: Prefer manually supplied, least-privilege credentials and disable automatic key fetching or disk persistence when possible.

Risk: Security evidence reports that the default Node client routes to a different remote skill than the advertised TradingView indicator toolkit.

Mitigation: Do not rely on the Node client until the publisher fixes the embedded skill-key mismatch and the package is reviewed again.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyffeifeifei/skills/prana-cyf-20260328-test01)
- [ClawHub publisher profile](https://clawhub.ai/user/cyffeifeifei)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON responses and Markdown-style setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Prana API credentials; the artifact documents Node.js as the primary client and Python as a fallback.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
