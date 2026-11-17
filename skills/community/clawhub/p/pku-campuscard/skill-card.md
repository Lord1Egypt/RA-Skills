## Description:

PKU Campus Card (校园卡) CLI tool built in Rust for working on the campuscard crate, debugging campus card commands, adding features, and handling campus-card workflows such as balance, recharge, payment QR, transaction history, monthly spending, and authentication constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with a Rust CLI for PKU campus-card operations, including authentication, balance lookup, payment QR display, recharge, transaction history, monthly statistics, and OTP management. It is most relevant when maintaining or operating the campuscard crate against PKU's Synjones campus-card platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through authenticated PKU campus-card operations, including login, payment QR generation, recharge, OTP changes, and transaction-history access.

Mitigation: Require explicit user confirmation before login, payment QR generation, recharge, OTP changes, or viewing transaction history.

Risk: The skill describes auto-login with stored credentials.

Mitigation: Review how the underlying CLI stores and clears sessions before using real credentials, and avoid exposing credentials or session data in agent-visible logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjsoj/skills/pku-campuscard)
- [Publisher profile](https://clawhub.ai/user/wjsoj)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and code identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve authenticated campus-card operations and Chinese-language CLI output.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
