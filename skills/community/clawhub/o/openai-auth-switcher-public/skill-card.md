## Description: <br>
OpenAI Auth Switcher Public helps OpenClaw administrators install a localhost web workflow for OpenAI OAuth account takeover, runtime inspection, slot management, dry-run switching, rollback, and release-safe packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amior1024](https://clawhub.ai/user/amior1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw administrators use this skill to manage OpenAI OAuth switching on private trusted machines, including first-run takeover, environment checks, profile slots, dry-run validation, controlled switching, and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth account-switching workflows can expose or persist sensitive auth-management material. <br>
Mitigation: Install only on a private trusted machine, use only accounts you are authorized to manage, and treat generated passwords, install-info.json, callback files, exported auth profiles, backups, and logs as secrets. <br>
Risk: The local web UI could become reachable beyond the intended operator if exposed on a shared host or network. <br>
Mitigation: Keep the web UI bound to localhost, use SSH tunneling for remote access, avoid CI or shared terminals, and stop or uninstall the service when the workflow is complete. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/amior1024/openai-auth-switcher-public) <br>
- [Compatibility](artifact/references/compatibility.md) <br>
- [Install and runbook](artifact/references/install-and-runbook.md) <br>
- [Security model](artifact/references/security-model.md) <br>
- [Web API preview](artifact/references/web-api-preview.md) <br>
- [Runtime discovery](artifact/references/runtime-discovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON status output, and local web UI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local service state, generated web credentials, auth profile copies, backups, logs, and status files on the user's machine.] <br>

## Skill Version(s): <br>
0.3.1-preview (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
