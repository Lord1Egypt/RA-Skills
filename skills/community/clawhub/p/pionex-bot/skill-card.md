## Description: <br>
Supports creating, querying, listing, adjusting, reducing, and cancelling Pionex bot orders for Futures Grid, Spot Grid, and Smart Copy workflows, including bulk listing and signal-provider publishing when credentials and permissions are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pibrandon](https://clawhub.ai/user/pibrandon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to manage Pionex trading bot lifecycles through CLI commands. It is intended for workflows that need bot reads, parameter validation, bot write actions, or signal-provider publishing with explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bot lifecycle and signal-platform write commands can affect trading positions or publish trading signals. <br>
Mitigation: Use a dedicated least-privilege API key, prefer dry-run commands where supported, and require explicit confirmation before any non-dry-run write action. <br>
Risk: Incorrect bot IDs, leverage, ranges, amounts, or signal UUIDs can produce unintended bot changes or signals. <br>
Mitigation: Require explicit user-provided values, run parameter checks before create actions, and surface returned constraints or API errors before retrying. <br>
Risk: The provided security summary flags the signal-publishing write action as high impact and not clearly declared in the top-level description. <br>
Mitigation: Tell users that `bot signal listener` publishes a trading signal as a signal provider and review every generated command before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pionex API credentials, bot permissions, and review before non-dry-run write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
