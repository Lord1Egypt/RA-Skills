## Description:

Portal helps agents use the PKU campus portal CLI to query free classrooms and academic calendars, check network-fee status, recharge balances, and monitor low balances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and PKU campus users use this skill to operate the Portal CLI for classroom availability, academic calendar lookup, network-fee status, recharges, and low-balance monitoring. Netfee commands require the user's PKU network credentials and should be used only on trusted hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Netfee recharge commands can initiate payment flows and display payment QR codes.

Mitigation: Confirm recharge amounts and payment method before execution, and require user approval before scanning or completing payment.

Risk: Netfee commands use PKU network credentials and persist session data under ~/.config/info/portal/ with keyring entries.

Mitigation: Use the skill only on trusted hosts, avoid shared machines, and clear or protect stored portal session and keyring data after use.

Risk: Calendar parsing is best-effort and may fail if the PKU simso Vue bundle structure changes.

Mitigation: Treat calendar output as operational guidance, and verify important dates against the official campus calendar when accuracy is critical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjsoj/skills/pku-portal)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI command examples for querying campus data, checking balances, recharging network fees, and monitoring low balances.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
