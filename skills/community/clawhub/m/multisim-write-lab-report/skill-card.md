## Description:

基于已注册实验的真实产物撰写中英实验报告；use when producing a lab report, design record, reproducibility package, or formal HTML/PDF output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and electronics lab users use this skill to draft traceable Chinese-English Multisim lab reports from registered experiment summaries, artifacts, measurements, and verification evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report may become misleading if the agent fills in missing measurements or verification results.

Mitigation: Use only registered experiment artifacts and measured summaries, cite verification evidence for PASS/FAIL claims, and label unsupported metrics as unverified.

Risk: Formal report exports or copied artifacts may expose unintended local files if paths are guessed or export boundaries are bypassed.

Mitigation: Export only when requested, use approved Multisim export tools, and rely on tool-returned file references instead of guessed paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown report prose with optional formal HTML/PDF export through approved tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite registered artifacts and SHA-256 values, separate facts from calculations and engineering judgment, and mark unsupported metrics as unverified.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
