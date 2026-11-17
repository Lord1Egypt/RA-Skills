## Description:

Record double-entry bookkeeping for personal finances. Use when logging transactions, categorizing accounts, balancing ledgers, trending expenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to log personal finance notes, categorize spending, inspect recent activity, search logs, and export simple reports. It is best treated as a local plaintext note logger rather than a full accounting system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial notes in plaintext under ~/.local/share/personal-bookkeeper.

Mitigation: Use local file permissions and avoid entering secrets, account numbers, or regulated financial records unless plaintext local storage is acceptable.

Risk: The security summary says the skill overstates its bookkeeping capability.

Mitigation: Treat outputs as notes and lightweight reports; verify balances, taxes, and accounting decisions with a real bookkeeping system or qualified reviewer.

Risk: CSV exports may be imported into spreadsheets with user-provided text intact.

Mitigation: Review exported CSV content before opening or sharing it, especially entries beginning with formula-like characters.

## Reference(s):

- [Personal Bookkeeper on ClawHub](https://clawhub.ai/ckchzh/skills/personal-bookkeeper)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local file/export descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read plaintext log and export files under ~/.local/share/personal-bookkeeper.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
