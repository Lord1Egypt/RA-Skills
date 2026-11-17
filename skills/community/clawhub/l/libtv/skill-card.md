## Description:

Converts UTF-8 story text into web-toon style PNG comic pages with text descriptions using the libtv backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[treelounge](https://clawhub.ai/user/treelounge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn a supplied novel or chapter text file into generated comic page assets and accompanying page descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports vulnerable or under-verified Python dependencies.

Mitigation: Install only in an isolated OpenClaw virtual environment or container, verify the libtv package source, and update or audit pinned dependencies before use.

Risk: The entrypoint appears malformed and may not run as packaged.

Mitigation: Review and correct the entrypoint packaging before installation or execution.

Risk: Story files may be processed by the libtv backend.

Mitigation: Do not provide private or sensitive story files unless that processing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/treelounge/skills/libtv)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime entrypoint returns JSON containing PNG image paths and text descriptions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
