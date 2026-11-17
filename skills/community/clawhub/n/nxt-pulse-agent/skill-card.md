## Description:

An adaptive proactive agent skill that manages user energy levels and task prioritization using semantic pulse checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adnxone](https://clawhub.ai/user/adnxone)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to let an agent adapt task nudges, recovery suggestions, and priority prompts based on recent conversation cues and configured context sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can infer a user's energy state from recent conversations and configured local context files.

Mitigation: Limit CONTEXT_SOURCES to a dedicated non-sensitive directory and avoid credentials, full journals, medical records, or broad logs unless that data is intentionally in scope.

Risk: Local pulse history and state files can retain sensitive activity or energy-state information.

Mitigation: Review or clear memory/pulse-state.json and memory/pulse-history.jsonl when local pulse history should not persist.

Risk: The provided security evidence marks the release as requiring review because local file analysis and privacy scoping may be insufficient.

Mitigation: Review the configured file scope and privacy expectations before enabling proactive pulse checks.

## Reference(s):

- [NXT Pulse Agent on ClawHub](https://clawhub.ai/adnxone/skills/nxt-pulse-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command text, configuration examples, and pulse status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local pulse state and pulse history when enabled.]

## Skill Version(s):

0.5.0 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
