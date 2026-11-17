## Description:

Repairs common loose JSON patterns, including trailing commas, single quotes, unquoted keys, comments, and hex or octal numbers, then returns valid JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to normalize malformed JSON-like input or files into valid JSON for configuration, data cleanup, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because the skill requests file-writing and command execution while making overconfident sandbox safety claims.

Mitigation: Review the skill before installing, run it in a constrained workspace, and approve file writes and command execution only for expected JSON repair tasks.

Risk: Repairing untrusted or malicious JSON-like input can produce unsafe assumptions about parsed content.

Mitigation: Use the skill only on inputs you are willing to inspect, prefer writing repaired output to a separate file, and validate the resulting JSON before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-repair-2)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with JSON output examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, execute commands, and write repaired JSON files when directed by the agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
