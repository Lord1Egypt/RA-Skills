## Description: <br>
Audit, clean, and optimize Clawdbot's vector memory (LanceDB) when memory is bloated with junk, token usage is high from irrelevant auto-recalls, or memory maintenance automation is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanbaker24](https://clawhub.ai/user/dylanbaker24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Clawdbot LanceDB memory, disable noisy auto-capture, wipe and reseed memory, and configure recurring memory maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes wipe instructions that can delete all Clawdbot LanceDB vector memory. <br>
Mitigation: Back up or export memory first, confirm the exact path, and keep a rollback plan before running wipe instructions. <br>
Risk: The skill includes recurring cron guidance that can reset memory unattended. <br>
Mitigation: Enable scheduled maintenance only after review and only when recurring memory resets are acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dylanbaker24/memory-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes memory audit, wipe, reseed, auto-capture configuration, and cron maintenance guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
