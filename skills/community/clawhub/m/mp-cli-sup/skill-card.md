## Description: <br>
Debugs a live WeChat Mini Program runtime through the system `vince-mp` JSON CLI, using one persistent session for page data, element query/tap, scan, console, doctor, and log-correlation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to connect an agent to WeChat DevTools, inspect live Mini Program state, act on runtime elements by uid, run diagnostics, and correlate frontend errors with backend logs. It is intended for WeChat Mini Program runtime debugging, not generic browser automation or source-only edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over a live WeChat Mini Program runtime. <br>
Mitigation: Install only when live runtime debugging is intended, prefer dev or test environments, and require explicit user intent for navigation, mutation, media, network, or mocking actions. <br>
Risk: The skill depends on the separate system `vince-mp` CLI. <br>
Mitigation: Use only a trusted installed `vince-mp` CLI and verify actions with the CLI's structured JSON evidence. <br>
Risk: Backend log access may expose production or administrative data. <br>
Mitigation: Confirm before production log access, avoid broad admin tokens, and report request-id log evidence narrowly. <br>


## Reference(s): <br>
- [Skill specification](artifact/SKILL.md) <br>
- [Runtime protocol](artifact/rules/runtime-protocol.md) <br>
- [UI element workflow](artifact/rules/ui-element-workflow.md) <br>
- [CLI contract](artifact/references/cli-contract.md) <br>
- [Skyline media](artifact/references/skyline-media.md) <br>
- [Evidence and failures](artifact/references/evidence-and-failures.md) <br>
- [Release manifest](artifact/assets/release-manifest.json) <br>
- [Metric plan](artifact/assets/metric-plan.json) <br>
- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/mp-cli-sup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Analysis] <br>
**Output Format:** [Markdown with inline shell commands and JSON evidence summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to be verified against JSON CLI output; file outputs require explicit paths under the workspace root.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
