## Description:

Kuaidi100 User helps agents handle shipment creation, logistics tracking, order management, address parsing, package weight lookup, and carrier price comparison through the Kuaidi100 CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuaidi100-api](https://clawhub.ai/user/kuaidi100-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Kuaidi100 shipping workflows, including authenticated shipment creation, logistics tracking, order cancellation, address parsing, weight lookup, and carrier comparison. The skill is intended for stepwise, user-confirmed shipping interactions where sensitive address and order data may be involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed, mutable CLI package that handles shipping PII and login state.

Mitigation: Install only from a trusted package source, prefer a pinned and reviewed CLI version, and review local login and data storage behavior before deployment.

Risk: Unsafe command templates could expose user-supplied fields to shell interpolation issues.

Mitigation: Execute CLI calls with argument arrays or equivalent safe command construction instead of interpolating untrusted values into shell strings.

Risk: Order cancellation and shipment creation can affect real shipping transactions.

Mitigation: Require explicit user confirmation before shipment creation or cancellation and show the final order details before executing the command.

Risk: Unauthenticated local cached order data may expose or mix stale shipping information.

Mitigation: Avoid unauthenticated access to local cached order data unless the deployment owner has reviewed what is stored locally and how it is protected.

## Reference(s):

- [Workflow](artifact/references/workflow.md)
- [Field Reference](artifact/references/fields.md)
- [ClawHub Skill Page](https://clawhub.ai/kuaidi100-api/skills/kuaidi100-user)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown with inline shell commands and JSON-derived CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose global npm installation and authenticated Kuaidi100 CLI commands; shipment creation and cancellation require explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
