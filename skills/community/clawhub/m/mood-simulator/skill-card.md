## Description: <br>
Mood Simulator estimates a user's current mood state, energy level, and focus, supports real-time mood tracking, and reacts to mood transitions, energy changes, and focus adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to assess mood, energy, and focus signals so an agent can adapt response style and publish local mood or energy alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mood, energy, focus, context, and behavioral-pattern history may be saved under the local OpenClaw workspace. <br>
Mitigation: Install only with informed consent, avoid sensitive health or personal details, and review or delete local mood state, pattern, and history files when retention is not acceptable. <br>
Risk: Mood-derived signals can be made available to other local components. <br>
Mitigation: Use only in trusted local workspaces and review integrations that consume mood-simulator signals before enabling proactive-engine workflows. <br>
Risk: The release does not clearly disclose opt-in, retention, deletion, and sharing behavior for mood-derived data. <br>
Mitigation: Add clearer disclosure, opt-in controls, retention limits, and deletion guidance before broader deployment. <br>


## Reference(s): <br>
- [Energy Calculation Reference](references/energy-calculation.md) <br>
- [Mood State Classification Reference](references/state-classification.md) <br>
- [Time Factor Adjustment Reference](references/time-factor-adjustment.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoguoqiang-hub/mood-simulator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON and JSONL mood state, pattern, history, and signal files when executed.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata; artifact package.json reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
