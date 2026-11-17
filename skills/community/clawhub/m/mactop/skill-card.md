## Description:

mactop retrieves real-time Apple Silicon Mac hardware metrics in TOON format, including CPU, memory, GPU, power, thermal, network, disk I/O, and Thunderbolt information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metaspartan](https://clawhub.ai/user/metaspartan)

### License/Terms of Use:


## Use Case:

Developers, operators, and Mac users use this skill to have an agent run mactop in headless TOON mode and summarize local Apple Silicon hardware metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external local tools, including mactop and Homebrew installation paths.

Mitigation: Install and trust the upstream mactop and Homebrew packages before using the skill, and verify mactop is available on PATH.

Risk: The skill reads local Mac hardware metrics, which may expose device performance, power, thermal, and I/O details.

Mitigation: Use it only when local hardware monitoring is intended, and avoid sharing generated metric summaries outside trusted contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metaspartan/skills/mactop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and readable metric summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mactop and local Apple Silicon Mac hardware metric access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
