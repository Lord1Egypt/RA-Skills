## Description: <br>
A Prana-backed TradingView technical indicator analysis helper that provides technical indicator calculation, analysis, and visualization capabilities through a remote execution client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyffeifeifei](https://clawhub.ai/user/cyffeifeifei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and developers can use this skill to send TradingView indicator analysis prompts to a Prana-hosted assistant and receive analysis results. It is best suited for environments where remote execution and credential handling have been reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, trading context, and any account or contact identifiers present in the environment may be sent to claw-uat.ebonex.io for remote Prana execution. <br>
Mitigation: Use the skill only when you trust the remote Prana service, avoid sending sensitive data, and confirm that the data-sharing pattern fits the deployment environment. <br>
Risk: The client can fetch credentials automatically and may persist API keys in local config files. <br>
Mitigation: Disable automatic key fetching or disk persistence when appropriate, manage credentials through approved secret storage, and keep generated credential files out of commits. <br>
Risk: The documented setup can change global OpenClaw environment variables and restart the OpenClaw gateway. <br>
Mitigation: Apply the configuration only in a controlled environment and review the effect of global OpenClaw configuration changes before restarting the gateway. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and command examples; script responses are text or JSON returned by the Prana service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRANA_SKILL_PUBLIC_KEY and PRANA_SKILL_SECRET_KEY, or automatic key fetching, before remote execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
