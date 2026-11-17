## Description:

Philosophy Dialogue helps an agent respond from selected philosopher or thinker perspectives using a catalog of 243 Eastern and Western figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wings229](https://clawhub.ai/user/wings229)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to ask an AI assistant to analyze questions through named philosopher, thinker, scientist, strategist, or writer perspectives. It supports single-perspective prompts, multi-perspective comparisons, debates, and random perspective selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled maintenance script can copy and delete directories based on workspace registry paths.

Mitigation: Review the script before use, run it only in a trusted workspace with backups, and add path validation before execution.

Risk: The authoritative security evidence marks the release suspicious because file-copying and deletion behavior is not safely bounded.

Mitigation: Treat installation as requiring manual review and avoid running maintenance scripts until file scope and path handling are documented.

Risk: The artifact describes referenced perspective content that may be required for full persona coverage.

Mitigation: Confirm the referenced perspective content is packaged or clearly documented before relying on the advertised catalog coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wings229/skills/philosophy-dialogue)
- [Publisher profile](https://clawhub.ai/user/wings229)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text dialogue responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response depends on the selected perspective and agent runtime; the skill does not define a fixed structured output schema.]

## Skill Version(s):

5.0.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
