## Description: <br>
Dropbox Sign helps agents read and search Dropbox Sign account, signature request, and template data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Dropbox Sign account details, inspect signature requests, and list accessible templates without handling raw Dropbox Sign API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dropbox Sign account data, signature requests, and templates may contain sensitive business information. <br>
Mitigation: Install and use the skill only when the connected OOMOL account is permitted to access the relevant Dropbox Sign data. <br>
Risk: Future connector actions marked write or destructive could change Dropbox Sign state. <br>
Mitigation: Review the live action schema and require explicit user confirmation before running any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-dropbox-sign) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [Dropbox Sign homepage](https://sign.dropbox.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before running Dropbox Sign read and list actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
