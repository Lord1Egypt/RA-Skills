## Description:

A command-line activity journal for recording and exporting machine learning data pipeline, schema, validation, profiling, and visualization notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to log ML data preparation, validation, profiling, and visualization activity from the command line. It is best treated as a local workflow journal rather than a real visualization or model-selection engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags this skill as suspicious because it is presented as an ML visualization or model-selection tool while behaving as a local plaintext logging tool.

Mitigation: Review the artifact before installing and set user expectations that it records notes and command activity rather than generating model diagnostics.

Risk: Users may enter secrets, customer data, private dataset paths, proprietary schema details, credentials, or sensitive model notes into logs stored in plaintext.

Mitigation: Avoid entering sensitive information and redirect ML_VISUALIZER_DIR to an approved local location with appropriate access controls when logging is necessary.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output with optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext logs under ~/.local/share/ml-visualizer by default; ML_VISUALIZER_DIR can override the data directory.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
