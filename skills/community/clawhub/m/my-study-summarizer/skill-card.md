## Description:

Processes supported files to extract key information and produce concise, structured summaries for school study.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iuri-siqueira](https://clawhub.ai/user/iuri-siqueira)

### License/Terms of Use:

MIT-0

## Use Case:

Students and educators use this skill to summarize study materials and extract structured notes from supported documents, code, data files, images, audio, video, and archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad authority to read many file types, recurse through archives, run parsing code, and create outputs.

Mitigation: Review the skill before installation, run it with least-privilege file access, and restrict it to known study materials and output locations.

Risk: The skill may use web or external transcription services while processing files.

Mitigation: Disable or control network access for confidential materials, and confirm external-service behavior before processing sensitive files.

Risk: The skill's broad auto-activation triggers and retention details are too broad for automatic use.

Mitigation: Require explicit user confirmation before processing files and define cleanup and retention expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iuri-siqueira/skills/my-study-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text, with JSON or generated files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summaries, extracted data, comparisons, citations, confidence notes, and file outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
