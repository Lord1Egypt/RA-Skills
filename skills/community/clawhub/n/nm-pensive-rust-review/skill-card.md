## Description:

Audits Rust code for unsafe blocks, ownership issues, and Cargo dependency risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review Rust changes for safety, correctness, concurrency, dependency, and idiom issues before merging or during focused audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rated the release suspicious and reported incomplete inspection, with concerns about the relevance of some guidance and file-writing or installation steps.

Mitigation: Review the full skill contents, including commands that write local files and the cargo-mutants installation step, before running the workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown audit report with findings, source locations, evidence anchors, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to include source locations and verbatim anchors; unsupported findings should be removed or labeled UNVERIFIED.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
