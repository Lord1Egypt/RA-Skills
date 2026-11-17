## Description:

Extract structured paper records from one or more local PDFs, arXiv links, DOI links, or general paper URLs, then classify the papers and write an academic survey review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang888596](https://clawhub.ai/user/huang888596)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to convert a set of paper PDFs or URLs into structured paper records, a defensible classification table, and an academic survey-style review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can read arbitrary local text, HTML, and PDF paths supplied by the user.

Mitigation: Run the skill in a constrained workspace and avoid private paths or sensitive documents unless their contents are intended to be processed.

Risk: The helper scripts can fetch unrestricted paper URLs.

Mitigation: Use sandboxed network egress controls and review source URLs before running extraction.

Risk: Weak extraction fallbacks can produce incomplete or noisy metadata that may affect classifications and survey claims.

Mitigation: Treat extraction notes as quality signals, reopen weak sources when important details are missing, and keep uncertain claims explicit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huang888596/skills/paper-cluster-survey-v2-2)
- [Extraction Pipeline](artifact/references/extraction-pipeline.md)
- [Output Schema](artifact/references/output-schema.md)
- [Review Paper Style](artifact/references/review-paper-style.md)
- [Taxonomy Guidelines](artifact/references/taxonomy-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown survey review with classification tables, optional JSON paper records, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output order is corpus summary, classification scheme, classification table, formal review article, and references.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
