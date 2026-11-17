## Description:

Mapick recommends OpenClaw skills, searches ClawHub, checks skill safety, manages privacy choices, cleans unused skills, and produces usage/persona summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlleyevan](https://clawhub.ai/user/sunlleyevan)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use Mapick to find missing skills, get personalized recommendations, review safety signals, control network consent, clean unused skills, and inspect outbound privacy activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the skill as suspicious because its recommendation purpose involves broad local, network, install, shell-plan, and session-log authority.

Mitigation: Review before installing, prefer the OpenClaw install path, and grant network access only after understanding the consent prompt and outbound data categories.

Risk: Flows can propose install, uninstall, upgrade, cron, or shell-plan actions that affect local skills or agent behavior.

Mitigation: Require explicit user confirmation, inspect proposed commands before execution, and avoid raw installer commands or unreviewed plan execution.

Risk: Token statistics and privacy-log features may read local OpenClaw session or Mapick log data.

Mitigation: Avoid token statistics unless local session-log reads are acceptable, and use the privacy log to inspect outbound endpoint names and field names without exposing values.

## Reference(s):

- [Mapick ClawHub skill page](https://clawhub.ai/sunlleyevan/skills/mapick)
- [Mapick publisher profile](https://clawhub.ai/user/sunlleyevan)
- [Project link from artifact README](https://github.com/mapick-ai/mapick)
- [Flow reference](artifact/reference/flows.md)
- [Rendering reference](artifact/reference/rendering.md)
- [Lifecycle reference](artifact/reference/lifecycle.md)
- [Error reference](artifact/reference/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with shell command proposals and occasional generated HTML persona report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shell command results are expected as single-line JSON for the agent to parse and paraphrase; persona share reports are generated locally before any user-confirmed upload.]

## Skill Version(s):

1.0.28 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
