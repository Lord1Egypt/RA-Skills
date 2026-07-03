## Description: <br>
Drive a self-hosted Huly workspace through the huly CLI for issues, projects, cards, documents, calendars, channels, direct messages, actions, time tracking, notifications, and approvals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamcoder18](https://clawhub.ai/user/iamcoder18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to choose safe huly CLI commands, verify workspace context, read or mutate Huly records, and understand side effects before operating a self-hosted Huly workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through broad workspace operations, including destructive CLI actions. <br>
Mitigation: Confirm the active Huly workspace, preview destructive changes, and require explicit approval before deletes or other irreversible mutations. <br>
Risk: Raw huly api or huly ws commands can bypass safer task-specific CLI surfaces. <br>
Mitigation: Use standard huly CLI commands first and allow raw API/RPC escape hatches only when the normal command cannot complete the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iamcoder18/skills/huly) <br>
- [Server-resolved GitHub source](https://github.com/IamCoder18/huly-cli/tree/main/packages/huly-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command patterns for programmatic reads.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
