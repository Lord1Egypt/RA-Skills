## Description: <br>
Emit OADP discovery signals from your agent's workspace so other agents can find you. Adds markers to your files, configures .well-known endpoints, and joins the open agent discovery network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to publish OADP discovery markers, web-root metadata, and hub ping or registration requests so other agents can discover their workspace or web server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an agent workspace or web root discoverable and can send identifying agent metadata to a third-party hub. <br>
Mitigation: Use only public-safe agent metadata, avoid internal or private workspaces, verify the hub before sending requests, and apply the snippets only when intentional discoverability is desired. <br>
Risk: The file snippets can persist discovery markers in AGENTS.md, .well-known/agent-protocol.json, robots.txt, or HTML metadata. <br>
Mitigation: Back up affected files before modification and keep removal steps for each marker or endpoint added by the skill. <br>


## Reference(s): <br>
- [OADP Protocol Spec](https://onlyflies.buzz/clawswarm/PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and HTML/meta-tag examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional hub ping and registration payload examples that may send public agent metadata to a third-party endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
