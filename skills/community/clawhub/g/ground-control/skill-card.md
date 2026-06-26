## Description: <br>
Post-upgrade verification system for OpenClaw that defines a model, cron, and channel ground truth file plus a 5-phase automated verification flow with auto-repair for config and cron drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill after OpenClaw upgrades or suspected drift to compare runtime configuration, model routing, cron jobs, sessions, and channels against a maintained ground truth file. It can generate verification reports and, when not in dry-run mode, repair non-sensitive config and cron drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify runtime configuration and recurring cron jobs. <br>
Mitigation: Run in dry-run or report-only mode first, review proposed changes, and require human confirmation when more than three fields need repair in a phase. <br>
Risk: Runtime configuration checks could expose credentials or sensitive settings in reports or memory files. <br>
Mitigation: Use the documented zero-secret logging protocol: strip auth, plugins, and credentials after config reads, redact sensitive mismatches, and validate provider liveness through functional sessions rather than literal key comparison. <br>
Risk: A stale ground truth file could cause incorrect drift reports or repairs. <br>
Mitigation: Keep MODEL_GROUND_TRUTH.md synchronized after config, model, cron, channel, or ACP changes before using auto-fix behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JonathanJing/ground-control) <br>
- [MODEL_GROUND_TRUTH.md template](templates/MODEL_GROUND_TRUTH.md) <br>
- [Post-upgrade verification workflow](scripts/post-upgrade-verify.md) <br>
- [Upgrade SOP](scripts/UPGRADE_SOP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce verification reports, local memory summaries, and proposed or executed OpenClaw config and cron repair actions.] <br>

## Skill Version(s): <br>
0.3.5 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
