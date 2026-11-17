## Description:

Classifies clinical trial protocol deviation incidents as major, minor, or critical and provides risk rationale, regulatory basis, and recommended actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical trial operations, quality assurance, and data analysis users use this skill to classify documented protocol deviation events and generate structured rationale or reports for review. Final determinations remain subject to clinical quality assurance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict and notes broader file handling and dependency installation behavior than the documentation promises.

Mitigation: Review the skill before installing, run it only in an isolated workspace or virtual environment, and avoid the documented pip install path unless dependencies are removed or pinned.

Risk: Clinical-trial subject or site data may be written to local output files.

Mitigation: Use controlled output paths and redact or securely store sensitive fields before processing real clinical-trial data.

## Reference(s):

- [Runtime Checklist](references/runtime_checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/protocol-deviation-classifier-1)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [JSON or text summaries, with optional markdown guidance and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce single-event classifications, batch classification results, and summary reports when input and output paths are provided.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
