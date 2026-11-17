## Description:

Check MiniMax coding plan usage and credits remaining using a MINIMAX_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check remaining MiniMax coding plan credits and optionally emit threshold-based alert text for automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a user-provided MINIMAX_API_KEY to the MiniMax API endpoint.

Mitigation: Confirm the endpoint is expected before use and protect the API key in local and scheduled execution environments.

Risk: Optional cron usage can pipe output to a user-provided downstream webhook command.

Mitigation: Review the webhook command and environment handling before enabling scheduled alerts.

## Reference(s):

- [MiniMax Coding Plan Remains API endpoint](https://www.minimax.io/v1/api/openplatform/coding_plan/remains)
- [ClawHub skill page](https://clawhub.ai/khaney64/skills/minimax-usage-2)
- [Publisher profile](https://clawhub.ai/user/khaney64)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Discord-formatted Markdown text and shell usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit silently when the optional threshold is configured and remaining usage is above that threshold.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
