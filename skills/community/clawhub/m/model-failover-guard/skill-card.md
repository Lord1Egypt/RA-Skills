## Description: <br>
Automatically monitors OpenClaw model health and switches from a failing primary model to a configured fallback, then attempts failback after stability returns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BovmantH](https://clawhub.ai/user/BovmantH) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to keep OpenClaw service routing available when a primary model becomes unstable. It can run as a one-time check or a loop that tests the current model, changes the default model when thresholds are met, and records state and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guard can intentionally change the OpenClaw default model and restart the gateway while it runs. <br>
Mitigation: Review config.json before use, set excludedProviders for providers that must not be selected, and run once mode first to observe the planned behavior. <br>
Risk: Unexpected failover settings could route work to an undesired fallback model. <br>
Mitigation: Set primaryModel, preferredFallbackProvider, thresholds, and excludedProviders explicitly for the deployment, and back up ~/.openclaw/openclaw.json before enabling loop or service mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BovmantH/model-failover-guard) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/skills/model-failover-guard/SKILL.md) <br>
- [Example configuration](artifact/skills/model-failover-guard/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for configuring and running an OpenClaw model failover guard; the runtime script writes JSON state and text logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
