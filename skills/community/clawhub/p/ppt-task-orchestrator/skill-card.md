## Description:

Production orchestration for pptx page task extraction and batch image delivery by reusing main-image-editor + psd-automator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhrxy](https://clawhub.ai/user/dhrxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert structured PPTX page instructions into batch image-editing tasks, execute them with rollback behavior, and package generated PNG delivery artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted PPTX files or request JSON can drive local parsing, OCR, and file handling.

Mitigation: Review inputs before execution and run with dry-run first, especially when handling files from untrusted sources.

Risk: Delivery settings can write outside the intended folder or use unsafe ZIP names.

Mitigation: Keep delivery.outputDir inside a known safe folder and use a simple ZIP filename with no slashes or traversal.

Risk: Delivery may include more generated images than requested.

Mitigation: Inspect dry-run output and delivery settings before executing a production batch.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON result payloads, request configuration JSON, and file delivery artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces parsed page tasks, execution status, failure details, a delivery directory, and an optional ZIP archive.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
