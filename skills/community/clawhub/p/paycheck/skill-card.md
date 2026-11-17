## Description:

Records, searches, and exports paycheck-related entries for salary breakdowns, deductions, comparisons, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use Paycheck to maintain a local audit trail of paycheck-related notes, comparisons, deduction analyses, reports, and exports. Treat it as a local plaintext record keeper rather than a payroll or tax calculation engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive salary, tax, benefit, or offer details may be stored as plaintext local logs and exports.

Mitigation: Do not enter real sensitive pay data unless local retention is acceptable; review file permissions and delete logs or exports when no longer needed.

Risk: The skill is paycheck-branded but primarily records, searches, and exports pay-related text instead of calculating pay.

Mitigation: Treat outputs as a note log, not payroll or tax advice; verify paycheck calculations with a trusted payroll system or calculator.

## Reference(s):

- [Paycheck ClawHub skill page](https://clawhub.ai/ckchzh/skills/paycheck)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text on stdout plus local log files and optional JSON, CSV, or TXT exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries under ~/.local/share/paycheck/ and appends actions to history.log.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
