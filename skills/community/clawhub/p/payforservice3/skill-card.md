## Description:

Guides an agent through Alipay payment handling by checking wallet authorization, submitting cashier links with the alipay-bot CLI, returning payment links or QR media, and querying payment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhc1111](https://clawhub.ai/user/xhc1111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process explicit Alipay payment requests from cashier links and to check payment status after the user completes payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external payment CLI during payment flows.

Mitigation: Install only when the publisher and Alipay npm package are trusted, keep the package pinned to the evidenced version, and verify package integrity before installation.

Risk: The skill can participate in real payment flows and may display CLI-provided payment links or QR media.

Mitigation: Use only for explicit, current payment requests, verify that cashier links are Alipay links before acting, and avoid logging or forwarding generated payment URLs outside the user-selected channel.

Risk: The skill instructs the agent to repeat CLI payment output exactly, so unexpected CLI output could influence what the user sees.

Mitigation: Review unexpected instructions or non-Alipay links in CLI output before presenting them to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhc1111/skills/payforservice3)
- [Publisher profile](https://clawhub.ai/user/xhc1111)
- [Alipay payment-skills homepage](https://github.com/alipay/payment-skills)
- [Alipay agent-payment npm package](https://www.npmjs.com/package/@alipay/agent-payment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with CLI-derived payment links or media references when required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exact preservation of CLI-provided payment URLs and uses JSON responses internally for payment-flow decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
