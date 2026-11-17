## Description:

Prism Alerts helps agents and operators query Pump.fun bonding and graduated token data from the Strykr PRISM API and run a local polling alert script for newly seen token contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:


## Use Case:

Developers, trading bot operators, and agent builders use this skill to inspect Pump.fun token lists, monitor newly observed contracts, and connect alert output to downstream Telegram, Discord, or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact claims broader alert and integration features than the packaged script implements.

Mitigation: Review the script behavior before relying on claimed volume-spike, Telegram, Discord, or scanning features; implement and test missing integrations separately.

Risk: The watch command stores seen token contracts in a shared temporary file.

Mitigation: Run the script as an unprivileged user and move state to a per-user path with restricted permissions before production use.

Risk: Messaging integration tokens could be exposed if copied into source files or shared command history.

Mitigation: Store Telegram and Discord tokens outside source control, limit token scope where possible, and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nextfrontierbuilds/skills/prism-alerts)
- [Publisher profile](https://clawhub.ai/user/nextfrontierbuilds)
- [Strykr PRISM API base URL](https://strykr-prism.up.railway.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash and JavaScript snippets; shell commands print plain-text token summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The packaged script expects curl and jq, accepts an optional PRISM_URL environment variable, and stores watch state locally.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter says 1.1.1 and skill.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
