## Description: <br>
Admin CLI for Lemon Squeezy stores. View orders, subscriptions, and customers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abakermi](https://clawhub.ai/user/abakermi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Store operators and developers use this skill to run Lemon Squeezy admin CLI commands for viewing orders, subscriptions, customers, and stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Lemon Squeezy API key for command execution. <br>
Mitigation: Use the least-privileged API key available and rotate it if it is exposed. <br>
Risk: Command output may include customer emails, revenue data, order details, and subscription metrics. <br>
Mitigation: Treat command output as sensitive and avoid sharing it in public logs, tickets, or transcripts. <br>
Risk: The skill relies on the `ls-admin` CLI to execute Lemon Squeezy admin commands. <br>
Mitigation: Install and run it only in environments where the CLI source and behavior are trusted. <br>


## Reference(s): <br>
- [Lemon Squeezy API settings](https://app.lemonsqueezy.com/settings/api) <br>
- [ClawHub skill page](https://clawhub.ai/abakermi/lemonsqueezy-admin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LEMONSQUEEZY_API_KEY and may display customer emails, order amounts, subscription metrics, and store data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
