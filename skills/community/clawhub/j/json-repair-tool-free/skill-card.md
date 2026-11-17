## Description:

JSON修复工具免费版 helps agents repair common JSON syntax errors such as trailing commas, single quotes, unquoted keys, comments, and hexadecimal numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations engineers, and data practitioners use this skill to have an agent repair malformed JSON files or produce a repair report before reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite local JSON files while repairing them.

Mitigation: Review target file paths before execution and keep the default .bak backup behavior.

Risk: The security evidence says the instructions are broad and inconsistent enough to require review before installation.

Mitigation: Use the skill only for explicit, user-directed JSON repair tasks and avoid unrelated API, networking, deployment, or general agent-orchestration work unless the publisher narrows the instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-repair-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files]

**Output Format:** [Markdown repair guidance with JSON snippets and shell command examples; repair output may include JSON files and .bak backups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is intended for explicit local JSON repair tasks and should validate repaired JSON before reuse.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
