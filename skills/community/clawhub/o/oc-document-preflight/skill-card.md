## Description: <br>
Prepare local documents for OpenClaw review without losing source anchors, redaction notes, or validation checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiepu110](https://clawhub.ai/user/jiepu110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and document owners use this skill to plan local document conversion into reviewable Markdown while preserving source anchors, redaction notes, and validation checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive information in local documents may be exposed in generated Markdown, notes, or anchors. <br>
Mitigation: Process only approved files and define redaction rules for credentials, account IDs, personal data, and revealing local file paths before producing public output. <br>
Risk: Converted document sections may become difficult to verify if source context is lost or extraction uncertainty is hidden. <br>
Mitigation: Preserve page, section, row, heading, or timestamp anchors for every extracted section and mark uncertain extraction results instead of filling gaps. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with plans, maps, notes, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Markdown conversion plan, source anchor map, redaction notes, and validation checklist for explicitly approved local files.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
