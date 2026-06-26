## Description: <br>
Run iPhone mission playbooks for battery, storage, privacy, connectivity, and daily automation with live operator-style guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to receive step-by-step iPhone troubleshooting and optimization guidance for battery drain, storage pressure, privacy hardening, connectivity failures, notifications, and routine automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep local iPhone troubleshooting notes under ~/iphone/ when memory is enabled. <br>
Mitigation: Review or delete the ~/iphone/ folder as needed, and avoid storing passwords, recovery codes, or other sensitive account secrets. <br>
Risk: Guided phone changes such as deletion, profile removal, resets, or automation steps may affect device behavior or data. <br>
Mitigation: Require explicit user confirmation before destructive, profile-related, reset, or automation actions, and prefer reversible steps first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/iphone) <br>
- [Skill homepage](https://clawic.com/skills/iphone) <br>
- [Setup - iPhone](setup.md) <br>
- [Mission Catalog](mission-catalog.md) <br>
- [Tap Script Engine](tap-script-engine.md) <br>
- [Rescue Ladders](rescue-ladders.md) <br>
- [Optimization Ops](optimization-ops.md) <br>
- [Shortcuts Bridge](shortcuts-bridge.md) <br>
- [Memory Template - iPhone](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with step-by-step tap paths, checkpoints, fallback branches, and optional local memory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; may keep local troubleshooting context under ~/iphone/ when memory is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
