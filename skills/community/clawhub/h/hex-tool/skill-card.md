## Description:

Convert data between hexadecimal and other formats. Use for debugging binary data, examining file headers, and working with hex dumps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for byte-level inspection, binary debugging, file header checks, and hex dump workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may pass a sensitive local file path and receive its contents as hexadecimal output.

Mitigation: Run it only on files intended for inspection and avoid sharing generated hex dumps when file contents are sensitive.

Risk: The documentation describes decoding and base conversion examples, while the bundled script evidence only shows hexadecimal encoding.

Mitigation: Verify the installed command supports the needed operation before relying on decode or base conversion examples.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and hexadecimal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads stdin or an explicitly provided local file path and prints hexadecimal text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
