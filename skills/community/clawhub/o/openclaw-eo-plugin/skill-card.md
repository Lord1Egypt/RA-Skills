## Description: <br>
Everything Openclaw (EO) adds a multi-expert collaboration engine for OpenClaw with expert commands, checkpoint verification, proactive memory, and workflow orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[467718584](https://clawhub.ai/user/467718584) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to plan, architect, review, verify, and coordinate software work through a library of specialized experts and OpenClaw commands. It is intended for normal ClawHub release use, with configuration review before deployment in sensitive or multi-agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can automatically edit configured agent instruction files and create persistent self-evolution state. <br>
Mitigation: Review and disable auto-init, rule enforcement, and persistent memory features before use in sensitive environments. <br>
Risk: The plugin can schedule background Dream jobs and send external notifications through Feishu or webhooks. <br>
Mitigation: Audit cron, scheduler, Feishu, and webhook settings before enabling the plugin, and limit credentials to the minimum required scope. <br>
Risk: Server security evidence classified this release as suspicious because impactful automation paths are under-disclosed. <br>
Mitigation: Install only after reviewing the security summary and running local policy checks for the target OpenClaw environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/467718584/openclaw-eo-plugin) <br>
- [Publisher Profile](https://clawhub.ai/user/467718584) <br>
- [README](README.md) <br>
- [OpenClaw Plugin Manifest](openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, command responses, configuration guidance, and code-oriented review or planning output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify persistent OpenClaw agent context, memory, rule, scheduling, and notification configuration depending on enabled plugin features.] <br>

## Skill Version(s): <br>
3.0.4 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
