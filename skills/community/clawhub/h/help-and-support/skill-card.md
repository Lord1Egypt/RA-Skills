## Description:

Get contextual help, onboarding guidance, app version details, and issue-reporting support for the Finance District agent wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt)

### License/Terms of Use:

MIT-0

## Use Case:

External wallet users and support agents use this skill to answer Finance District wallet questions, guide onboarding, check app version details, and submit issue reports when a user encounters a problem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form support text may include sensitive wallet, account, transaction, or recovery information.

Mitigation: Review support text before submission and omit seed phrases, private keys, passwords, recovery codes, full personal details, and unnecessary account or transaction data.

Risk: Issue reporting can submit authenticated support reports from user-provided descriptions.

Mitigation: Check authentication status and confirm the report title, description, severity, and category before submitting an issue.

Risk: User text is routed through shell command arguments for Finance District support commands.

Mitigation: Pass user input as structured command arguments rather than interpolating it into shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/skills/help-and-support)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Finance District support commands; issue reporting requires authentication.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
