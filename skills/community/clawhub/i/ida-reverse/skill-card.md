## Description:

ida-reverse standardizes IDA Pro MCP reverse-engineering workflows by requiring decompilation before conclusions, persistent annotations, and cautious naming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holdyounger](https://clawhub.ai/user/holdyounger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security researchers use this skill when reverse engineering binaries through IDA Pro MCP for crash triage, vulnerability research, malware or sample analysis, protocol or algorithm recovery, and state-machine reconstruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can invoke arbitrary IDA MCP tools against the configured endpoint.

Mitigation: Use only with trusted IDA Pro MCP sessions and keep IDA_MCP_URL restricted to loopback unless authenticated HTTPS transport is available.

Risk: Analysis data can be sent to any configured HTTP MCP endpoint.

Mitigation: Avoid remote endpoints unless they are trusted and authenticated, especially when working with sensitive binaries or proprietary analysis data.

Risk: Batch rename, comment, and type operations can persist changes in the IDA database and project notes.

Mitigation: Review proposed operations before use and apply them in small batches so incorrect annotations can be identified quickly.

## Reference(s):

- [ida-reverse ClawHub skill page](https://clawhub.ai/holdyounger/skills/ida-reverse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead an agent to call IDA MCP tools and persist renames, comments, and type declarations in an IDA database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
