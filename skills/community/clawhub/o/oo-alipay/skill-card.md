## Description:

Operate Alipay through an OOMOL-connected account to create payment checkout links, query payments and refunds, and request refunds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Alipay account can create checkout links, verify transaction and refund status, and request full or partial refunds. Confirm the exact refund details before running a refund action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned remote installer runs immediately, and the partial scan could not resolve two local references or determine what the downloaded script does.

Mitigation: Avoid installing or using the skill until the installer is reviewed and verified through a trusted source; resolve the local references and inspect the installer behavior first.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Alipay](https://www.alipay.com/)
- [Alipay API documentation](https://opendocs.alipay.com/open/0go80l)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector actions return structured data and execution metadata.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
