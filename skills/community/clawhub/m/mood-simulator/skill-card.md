## Description:

Mood Simulator estimates a user's mood state, energy level, and focus, then supports real-time mood tracking for mood transitions, energy changes, and focus adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assess conversational mood signals, estimate user energy and focus, and adjust response posture or publish local mood-related signals for other OpenClaw components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores inferred mood, energy, routine, context, and history data locally with unclear user control.

Mitigation: Review before installing; use only when local storage of these inferences is acceptable, and prefer a release that documents opt-in, retention, deletion, and signal-sharing controls.

Risk: The skill writes inferred mood and energy signals for other local components to consume.

Mitigation: Limit use to trusted OpenClaw workspaces and review which components can read local signal files before enabling signal publishing.

## Reference(s):

- [Mood Simulator ClawHub listing](https://clawhub.ai/zhaoguoqiang-hub/skills/mood-simulator)
- [Energy Calculation Reference](references/energy-calculation.md)
- [State Classification Reference](references/state-classification.md)
- [Time Factor Adjustment Reference](references/time-factor-adjustment.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [CLI text with local JSON and JSONL state, history, configuration, and signal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes inferred mood, energy, focus, routine, history, configuration, and signal data under the local OpenClaw workspace when executed.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
