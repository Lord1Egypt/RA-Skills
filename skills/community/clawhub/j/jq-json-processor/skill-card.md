## Description:

Process, filter, and transform JSON data using jq - the lightweight and flexible command-line JSON processor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnarsson](https://clawhub.ai/user/arnarsson)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to recall and apply jq commands for filtering, transforming, formatting, and debugging JSON data from files and API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-modification examples can overwrite local files when run on real project data.

Mitigation: Review commands before execution, test on disposable copies, and confirm redirects or moves before replacing files.

Risk: curl examples can send requests to endpoints that may expose private data or secrets if copied into a sensitive context.

Mitigation: Use sanitized inputs, avoid private endpoints or secrets unless the network request is intended, and confirm the destination before running commands.

## Reference(s):

- [jq Homepage](https://jqlang.github.io/jq/)
- [jq Manual](https://jqlang.github.io/jq/manual/)
- [jq Interactive Tutorial](https://jqplay.org/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the jq command-line binary; examples are intended for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
