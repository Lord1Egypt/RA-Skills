## Description: <br>
Provides OpenClaw configuration safety rules, recovery guidance, and helper scripts for backups, auth troubleshooting, cooldown resets, and config validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayrizz](https://clawhub.ai/user/jayrizz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw use this skill before changing configuration, troubleshooting authentication failures, taking backups, or recovering from configuration and session issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with OpenClaw auth, .env, and session files and could break or alter the wrong local profile. <br>
Mitigation: Inspect target paths, make a verified private backup, keep backup permissions restrictive, and review repair commands before execution. <br>
Risk: reset_cooldowns.sh contains a hardcoded /Users/admin auth profile path. <br>
Mitigation: Do not run reset_cooldowns.sh until the path is fixed to use the intended $HOME auth file. <br>
Risk: Recovery guidance can change OpenClaw configuration and authentication state. <br>
Mitigation: Use validation and status checks first, restore only from known-good backups, and restart OpenClaw services only after confirming the restored files. <br>


## Reference(s): <br>
- [Recovery Procedures](references/recovery.md) <br>
- [ClawHub release page](https://clawhub.ai/jayrizz/openclaw-sacred-rules) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recovery steps and local helper script commands; some commands may read or modify OpenClaw configuration, authentication, or session state when run by a user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and auto changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
