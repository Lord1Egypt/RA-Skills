## Description: <br>
Diagnose and manage SSH keys, host aliases, and Git remotes for GitHub private repositories in multi-repo environments, especially when deploy keys collide, automation pushes to GitHub, or authentication errors occur. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarinRowe](https://clawhub.ai/user/DarinRowe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose GitHub SSH routing for private repositories and plan fixes for deploy keys, host aliases, Git remotes, and automation configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit output can reveal private repository and SSH configuration details. <br>
Mitigation: Run audits locally, avoid posting raw output, and redact host aliases, usernames, repository URLs, key file names, HostName values, and proxy or jump-host settings before sharing logs. <br>
Risk: Changing the wrong SSH alias, deploy key, remote, or automation source can route private repository access through the wrong identity. <br>
Mitigation: Inspect first with the read-only audit workflow, verify SSH routing before Git operations, update both the live remote and any config or script source, and only push or pull after `git ls-remote origin` succeeds. <br>


## Reference(s): <br>
- [Decision Guide](references/decision-guide.md) <br>
- [Identity Model Boundaries](references/identity-model-boundaries.md) <br>
- [Key Storage by System](references/key-storage-by-system.md) <br>
- [OpenClaw + Automation Notes](references/openclaw-automation.md) <br>
- [Patterns](references/patterns.md) <br>
- [Symptoms](references/symptoms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and SSH configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose read-only local audit commands and configuration changes for SSH aliases, Git remotes, and automation sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
