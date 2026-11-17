## Description:

Parse academic PDF papers into markdown with figure extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-li-17](https://clawhub.ai/user/chen-li-17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to convert academic PDFs into structured Markdown, JSON metadata, extracted figure images, and a title/authors snapshot for downstream review or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes Markdown, JSON, and PNG files to a user-selected output directory.

Mitigation: Run it in a workspace where the output path cannot overwrite important files, and review the output directory before execution.

Risk: Runtime dependencies are installed through uv from inline script metadata.

Mitigation: Pin or lock dependencies before deployment when reproducible execution is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chen-li-17/skills/paper-parse-figures)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; generated artifact outputs include Markdown, JSON, and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and Python 3.10 or newer; processes local PDF files and writes results to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
