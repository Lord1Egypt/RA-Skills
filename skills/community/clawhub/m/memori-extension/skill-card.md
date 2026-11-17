## Description:

Memory augmentation and LLM call interception using the Memori Python library with optional Zhipu API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ian-at](https://clawhub.ai/user/ian-at)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use this skill to add local memory search, prompt augmentation, and optional LLM-call interception to an agent workflow. It can also call Zhipu AI for conversation analysis when explicitly configured with an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM interception can replace original system instructions with retrieved memory content.

Mitigation: Use only after review in agents that rely on strong system or tool-use policies; preserve original system messages and treat retrieved memories as untrusted reference material.

Risk: Setting ZHIPUAI_API_KEY enables external transmission of conversation text to Zhipu AI.

Mitigation: Leave ZHIPUAI_API_KEY unset by default, enable it only with explicit consent, and test external API behavior in a sandbox or restricted environment.

Risk: The skill reads and writes a local SQLite memory database and optional technical-terms file that may retain sensitive content.

Mitigation: Use a dedicated MEMORI_DB_PATH, apply appropriate file permissions, and avoid storing sensitive or untrusted text unless retention is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ian-at/skills/memori-extension)
- [Memori library repository](https://github.com/MemoriLabs/Memori)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python API results and Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write a local SQLite memory database and optional technical-terms file; optional Zhipu AI augmentation requires ZHIPUAI_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
