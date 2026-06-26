## Description: <br>
Master Agent Workflow Global helps OpenClaw users run a global, migratable master-agent workflow for parallel task dispatch, configuration migration, templates, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shujianming](https://clawhub.ai/user/shujianming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to route work through a configurable master and worker agent workflow, tune concurrency and timeouts, and move reusable configurations and templates across installations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can make persistent shell and OpenClaw configuration changes. <br>
Mitigation: Review the installer before use, back up existing OpenClaw and shell configuration files, and accept the persistent changes only in trusted environments. <br>
Risk: Configuration imports and template handling may write files using weak path controls. <br>
Mitigation: Import only trusted migration files and templates, avoid crafted config or template names, and inspect generated paths before applying changes. <br>
Risk: Backups, logs, reports, and migration exports can contain sensitive workflow or environment information. <br>
Mitigation: Store generated artifacts in access-controlled locations and review or redact them before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shujianming/master-agent-workflow-global) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/references/examples.md) <br>
- [Migration guide](artifact/migration-guide.md) <br>
- [OpenClaw hook integration guide](artifact/hooks/openclaw/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw configuration, templates, backups, logs, and migration exports when its installer, hook, or migration commands are executed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
