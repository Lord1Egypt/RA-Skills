## Description: <br>
Uses an OOMOL-connected Contentstack account through the oo CLI to read, create, and update Contentstack content and schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agents use this skill to inspect Contentstack content types and entries, then create or update entries through an OOMOL-connected account when the user approves write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update real Contentstack entries through a connected account. <br>
Mitigation: Before approving a write action, verify the stack, content type, entry target, payload, and expected publishing workflow. <br>
Risk: A command may run against the wrong or expired OOMOL-connected Contentstack account. <br>
Mitigation: Confirm the intended connection and resolve authentication or scope errors before retrying state-changing actions. <br>
Risk: Connector schemas may differ from assumptions in a generated payload. <br>
Mitigation: Run the connector schema command for the selected action before constructing or executing a payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-contentstack-content-management) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Contentstack homepage](https://www.contentstack.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash, PowerShell, JSON, and text blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches the live connector schema before action payload construction; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
