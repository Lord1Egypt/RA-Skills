## Description:

Integrates MochiPay crypto payments into online stores, backends, and mobile apps with checkout, callbacks, retries, and verified payment states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to install or repair MochiPay integrations for online stores, custom backends, and mobile apps, including checkout and payment verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposed merchant credentials could compromise payment operations.

Mitigation: Keep credentials on the merchant backend and never request secrets in chat.

Risk: Sandbox success can trigger normal order fulfillment.

Mitigation: Test with internal sandbox orders and confirm fulfillment controls before testing.

Risk: Downloaded gateway packages may be unverified.

Mitigation: Verify package hashes before installation.

Risk: Demo authentication and storage may not be suitable for production.

Mitigation: Replace demo authentication and storage with the application's production controls.

## Reference(s):

- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/integrate-mochipay)
- [MochiPay API Reference](https://mochi.bz/Developers/Reference.aspx)
- [MochiPay Developer Examples](https://mochi.bz/Developers/Reference.aspx#code-examples)
- [WooCommerce Guide](https://mochi.bz/Guides/GuideWooCommerce.aspx)
- [OpenCart Guide](https://mochi.bz/Guides/GuideOpenCart2.aspx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown instructions, code snippets, configuration examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific integration guidance; production readiness requires independent verification.]

## Skill Version(s):

1.2.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
