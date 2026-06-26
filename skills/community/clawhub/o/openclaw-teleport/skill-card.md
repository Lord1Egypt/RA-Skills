## Description: <br>
Migrate, back up, inspect, or restore an OpenClaw agent workspace using a single .soul archive, wrapping @kagura-agent/openclaw-teleport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagura-agent](https://clawhub.ai/user/kagura-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to move, back up, inspect, or recover an OpenClaw agent workspace. It is suited for migrations between machines, periodic backup, disaster recovery, and controlled cloning of an agent setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: .soul archives may contain plaintext credentials, API tokens, bot tokens, and app secrets. <br>
Mitigation: Treat .soul files like password exports: encrypt them, transfer them over trusted channels, avoid committing or sharing them, and delete them when no longer needed. <br>
Risk: Unpacking can restore files, credentials, cron jobs, repositories, and services into an OpenClaw workspace. <br>
Mitigation: Inspect archives before unpacking, restore into a controlled workspace first, and review restored credentials, scheduled jobs, repositories, and gateway behavior before relying on them. <br>
Risk: The release wraps an npm package and may process archives from external sources. <br>
Mitigation: Install only if you trust the npm package publisher and the source of any .soul archive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kagura-agent/openclaw-teleport) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or unpack .soul archives and restore workspace state when executed by the user.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
