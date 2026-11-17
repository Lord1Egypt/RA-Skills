## Description:

SZZZ Case Study Lite helps an agent turn a user's local PDF, DOCX, and DOC Chinese civil judgment files into a deduplicated, incrementally maintained case library with source-grounded summaries, Master Reports, question answering, and raw-text traceability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzzcode](https://clawhub.ai/user/szzzcode)

### License/Terms of Use:

MIT

## Use Case:

External users and legal-document workflow developers use this skill to organize local Chinese civil judgment materials, remove duplicates, generate per-case expert summaries, prepare source-linked topic reports, and answer follow-up questions against the local case library. It is intended for user-provided local materials and does not perform external case-law retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive legal text may be copied into the generated case library, including from symlinked documents outside the chosen folder.

Mitigation: Run the skill only in a trusted, clean project folder without symlinks, and review generated raw text before sharing or moving results.

Risk: Dependency installation can introduce supply-chain or environment risk.

Mitigation: Install dependencies in a dedicated virtual environment from a trusted package index before running the scripts.

Risk: The reset workflow deletes generated analysis results.

Mitigation: Use reset only after confirming that deleting law_analysis_results is intended and that any needed outputs are retained elsewhere.

Risk: Generated legal summaries and reports may contain mistakes or unsupported conclusions.

Mitigation: Verify case numbers, amounts, outcomes, evidence quotations, legal bases, and report conclusions against the raw extracted text before relying on or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szzzcode/skills/szzz-case-study-lite)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)
- [Analyzer prompt logic](prompts/analyzer-logic.md)
- [Master report prompt logic](prompts/master-report-logic.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated text, Markdown, and JSON files under law_analysis_results/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces raw extracted text, deduplication reports, status JSON, per-case Markdown summaries, master_data.json, and Master_Report.md for the user's local project folder.]

## Skill Version(s):

3.0.1 (source: server release metadata, README, CHANGELOG released 2026-07-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
