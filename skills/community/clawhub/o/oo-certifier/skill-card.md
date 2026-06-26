## Description: <br>
Certifier (certifier.io) supports Certifier requests involving reading, creating, and updating data through the OOMOL CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent list, search, create, issue, and send Certifier credentials through an OOMOL-connected Certifier account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Certifier through an OOMOL-connected account and may use sensitive account credentials handled by OOMOL. <br>
Mitigation: Install and use it only when the agent should access that Certifier account through OOMOL, and confirm the connected account before use. <br>
Risk: The create_issue_send_credential action creates, issues, and sends a credential. <br>
Mitigation: Review the exact payload, recipient, group, and custom attributes with the user before approving the write action. <br>
Risk: First-time setup may require installing the OOMOL CLI or connecting a Certifier account. <br>
Mitigation: Run installer or account-connection steps only after an auth or connection failure and only when the user trusts OOMOL and understands the connected account. <br>


## Reference(s): <br>
- [Certifier homepage](https://certifier.io) <br>
- [OOMOL CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-certifier) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to retrieve schemas and run Certifier connector actions; write actions require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
