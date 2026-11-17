## Description:

Provides a local MiniMax quota dashboard for token-plan usage monitoring, 24-hour usage history, and explicitly triggered inference latency probes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MiniMax API users use this skill to launch a local dashboard that checks remaining MiniMax Token Plan quota, tracks recent usage, and runs opt-in latency probes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can read and use the user's MiniMax API key for authenticated MiniMax requests.

Mitigation: Review before installing, run only on a trusted local machine, and avoid shared or network-exposed environments.

Risk: Authenticated quota polling and probes may consume MiniMax account resources or trigger billable actions.

Mitigation: Treat probes as opt-in actions, monitor usage, stop the local service when finished, and do not rely on --no-probe as the only control.

Risk: The dashboard may read and use ~/.mmx/config.json as soon as the page polls quota.

Mitigation: Assume credential access can occur during dashboard polling and use a dedicated or limited MiniMax key where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/minimax-monitor)
- [Publisher profile](https://clawhub.ai/user/wangjipeng977)
- [Metadata source](https://github.com/MiniMax-AI/skills)
- [MiniMax token plan remains API](https://www.minimaxi.com/v1/token_plan/remains)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local dashboard instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard can make authenticated MiniMax requests and write local usage-history samples.]

## Skill Version(s):

1.7.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
