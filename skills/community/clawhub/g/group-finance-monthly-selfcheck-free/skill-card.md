## Description:

A Chinese-language local finance self-check skill that runs three monthly reconciliation checks for group intercompany balances, supplier payables, and accounts receivable aging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, treasury, and accounting staff use this skill during monthly close or reconciliation cycles to check segmented finance tables for arithmetic, total-line, duplicate, and missing-field issues. Outputs are reconciliation aids and should not be treated as accounting, audit, tax, or legal conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on arithmetic reconciliation findings as accounting, audit, tax, or legal conclusions.

Mitigation: Treat results as reconciliation aids and have qualified finance or compliance reviewers validate any business conclusion.

Risk: The skill reads files supplied to the local Node script.

Mitigation: Run it only on files intentionally provided for the monthly finance self-check.

Risk: Missing or incomplete materials can make finance checks misleading if conclusions are forced.

Mitigation: Use the skill's insufficient-input output as a stop condition and provide the requested table sections before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/group-finance-monthly-selfcheck-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable terminal text or JSON summaries with findings, source-line evidence, per-check status, scope, and omitted checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided files; reports insufficient input instead of inferring conclusions from missing materials.]

## Skill Version(s):

1.0.49 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
