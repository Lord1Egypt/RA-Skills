## Description:

FapiaoClaw helps an agent process and organize invoice PDFs by fixing extensions, removing duplicates and invalid files, checking required keywords, moving files into invoice folders, and reporting the total amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jie](https://clawhub.ai/user/jie)

### License/Terms of Use:

MIT-0

## Use Case:

External users or developers use this skill to organize invoice PDF folders around a required company or content keyword, then summarize moved files and invoice totals after processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete duplicate files or files matching invoice-travel naming patterns and can move PDFs within the selected directory.

Mitigation: Run it only on a dedicated invoice-only folder after backing up files; avoid project, home, downloads, or shared directories.

Risk: The security evidence flags unsafe command construction with user-supplied keywords.

Mitigation: Review the exact command before execution, avoid untrusted keyword input, and prefer a revised version that uses shell-free invocation and quotes arguments safely.

Risk: Unexpected file movements or destination collisions may make invoice organization difficult to audit or reverse.

Mitigation: Use a dry-run or quarantine workflow where possible and inspect the resulting invoices and unknown folders before deleting originals or relying on totals.

Risk: The dependency list does not pin PyMuPDF.

Mitigation: Install in an isolated environment and pin a reviewed PyMuPDF version before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jie/skills/invoice-processing)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain-text summary with terminal command execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports extension fixes, duplicate removals, invalid-file removals, invoice folder moves, unknown-folder moves, and grand total amount when available.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
