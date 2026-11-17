## Description:

Guides agents through a design-first brainstorming workflow that turns an idea into an approved design spec before implementation planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to clarify project intent, compare approaches, produce a design document, review it for planning readiness, and transition only after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The visual companion can expose session content if it is bound beyond localhost.

Mitigation: Use localhost when possible, avoid sensitive content when binding to 0.0.0.0, and stop the companion server when finished.

Risk: The workflow directs repository commits for generated design specs.

Mitigation: Require explicit user approval before any git commit and have the user review the written spec before implementation planning.

Risk: Incomplete or incorrect assumptions can be carried into the generated design document.

Mitigation: Ask clarifying questions, present trade-offs, obtain design approval section by section, and run the spec self-review before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/idea-to-design)
- [Publisher profile](https://clawhub.ai/user/dizhu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, design spec documents, inline shell commands, and optional local HTML companion screens.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect project context, write a design spec, start a local visual companion, capture browser choices, and commit the approved spec when explicitly allowed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
