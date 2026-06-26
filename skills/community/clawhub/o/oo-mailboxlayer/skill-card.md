## Description: <br>
Enables agents to validate email addresses with Mailboxlayer through OOMOL's oo CLI and connected-account credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to validate individual email addresses with Mailboxlayer via an OOMOL-connected account, returning deliverability and quality signals without exposing raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validated email addresses are sent through the OOMOL/Mailboxlayer connector. <br>
Mitigation: Use the skill only when the user intends to validate those addresses with a connected Mailboxlayer account. <br>
Risk: The skill depends on an authenticated oo CLI session and connected Mailboxlayer credentials. <br>
Mitigation: Run first-time setup or login commands only when the oo command, authentication, or connection is actually missing. <br>
Risk: Connector payloads can become stale if the live action contract changes. <br>
Mitigation: Inspect the live connector schema before constructing the action payload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-mailboxlayer) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Mailboxlayer Connection Setup](https://console.oomol.com/app-connections?provider=mailboxlayer) <br>
- [Mailboxlayer Icon](https://static.oomol.com/logo/third-party/Mailboxlayer.svg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns an execution id under meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
