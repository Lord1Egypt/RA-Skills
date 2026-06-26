## Description: <br>
Hermes Evolution enhances OpenClaw with fast PM routing, proactive self-check, auto skill generation, user profiling, layered memory, and continuous learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add task routing, task storage, scheduled checks, user profiling, collaboration support, and self-improving workflow behavior to an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store user and workflow data in local task, rule, correction, schedule, collaboration, profile, and log files. <br>
Mitigation: Use the skill only in a controlled workspace, review retention expectations, and inspect generated local files before sharing or syncing the workspace. <br>
Risk: The skill can create new behavior through auto-skill generation and self-improving rules. <br>
Mitigation: Keep auto-skill generation and self-improving rules disabled until reviewed, then approve generated skills and rules before operational use. <br>
Risk: The Feishu integration can send task data externally when Feishu credentials are configured. <br>
Mitigation: Inspect or disable Feishu notification defaults before setting FEISHU_APP_TOKEN or FEISHU_APP_SECRET, and avoid sending sensitive task data through notifications. <br>
Risk: Periodic checks, scheduler runs, and cron-triggered modules can perform actions without an immediate user prompt. <br>
Mitigation: Review scheduled tasks and cron configuration before enabling them, and start with manual runs in a controlled workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuritu/hermes-evolution) <br>
- [Hermes Evolution README](README.md) <br>
- [Hermes Evolution skill documentation](SKILL.md) <br>
- [Hermes Evolution v1.0 documentation](docs/HERMES-EVOLUTION-v1.0.md) <br>
- [Deployment checklist](docs/HERMES-DEPLOY-CHECKLIST.md) <br>
- [Quick reference](docs/HERMES-QUICK-REF.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JavaScript examples, shell commands, and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local task, rule, correction, schedule, collaboration, log, profile, and generated-skill files when its modules are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
