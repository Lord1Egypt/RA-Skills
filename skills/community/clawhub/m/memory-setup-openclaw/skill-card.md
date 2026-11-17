## Description:

Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syajask](https://clawhub.ai/user/syajask)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure durable OpenClaw memory files, enable memory search, validate recall behavior, and troubleshoot low-quality or unavailable memory results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory files can contain private decisions, preferences, todos, or prior work context that may be indexed for recall.

Mitigation: Review the contents of MEMORY.md and memory/*.md before enabling memory search, and avoid storing sensitive information that should not be recalled.

Risk: Using a remote memory provider can send memory content to an external embedding provider.

Mitigation: Use the local provider when memory content should remain local, or confirm remote provider handling before configuring API keys.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration examples and command-line verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides memory setup and validation; it does not generate files directly.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
