## Description:

HUDC Bidding Information Capture analyzes locally stored SGCC bidding documents in Word, PDF, and Excel formats and produces a structured 23-column Excel report with qualification backfilling, keyword matches, deadlines, bid bonds, evaluation methods, and contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jktllsqaq](https://clawhub.ai/user/jktllsqaq)

### License/Terms of Use:

MIT

## Use Case:

External users and business analysts use this skill to process manually downloaded SGCC tender files from a local desktop folder, identify bid opportunities matching configured keywords, and review the generated Excel report for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer can automatically install unpinned Python packages into the user's environment.

Mitigation: Run it in a dedicated virtual environment or container, and manually install reviewed or pinned dependencies before execution.

Risk: Rows sourced from Word/PDF body fallback can be lower confidence than rows extracted from structured tables or Excel attachments.

Mitigation: Manually review records marked as Word/PDF body fallback and any unresolved qualification placeholders before relying on them for bidding decisions.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Samples README](artifact/samples/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance and terminal-style summaries, with a generated Excel workbook at ~/Desktop/sgcc_result.xlsx]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Excel report contains 23 structured columns and color-coded bidding deadlines.]

## Skill Version(s):

6.0.0 (source: server release metadata; artifact frontmatter lists 6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
