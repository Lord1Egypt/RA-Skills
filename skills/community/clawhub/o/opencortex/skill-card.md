## Description: <br>
OpenCortex gives OpenClaw agents a structured workspace memory system with nightly distillation, weekly synthesis, durable memory files, optional vault, optional metrics, and opt-in backup features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jd2005l](https://clawhub.ai/user/jd2005l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and maintain a structured long-term memory architecture for an agent workspace. It is intended for improving memory organization, nightly knowledge distillation, weekly synthesis, and optional local maintenance features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled maintenance jobs can read and write long-term workspace memory without direct interaction. <br>
Mitigation: Review installed cron entries after setup, confirm they are scoped to the intended workspace, and remove or edit jobs that are not needed. <br>
Risk: The skill can capture durable user, project, tool, and optional voice or infrastructure information. <br>
Mitigation: Disable optional voice profiling and infrastructure collection unless required, and review generated memory files before using the skill with sensitive projects. <br>
Risk: Vault and backup features may interact with credentials or secret-scrubbing configuration. <br>
Mitigation: Prefer a system keyring for vault passphrases, avoid file-based passphrase storage unless explicitly accepted, and test git backup scrubbing in a disposable workspace before using a real remote. <br>


## Reference(s): <br>
- [ClawHub OpenCortex Release Page](https://clawhub.ai/jd2005l/opencortex) <br>
- [OpenCortex Architecture Reference](references/architecture.md) <br>
- [Daily Memory Distillation Instructions](references/distillation.md) <br>
- [Weekly Synthesis Instructions](references/weekly-synthesis.md) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [OpenCortex Homepage](https://github.com/JD2005L/opencortex) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace memory files, scheduled maintenance instructions, verification guidance, and optional local helper scripts.] <br>

## Skill Version(s): <br>
3.6.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
