## Description: <br>
Read and edit Markdown notes on your personal computer via SSH tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logancyang](https://clawhub.ai/user/logancyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect, read, create, and append Markdown notes in a personal vault through a preconfigured SSH tunnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or write sensitive personal vault notes through SSH. <br>
Mitigation: Install only when the user trusts the remote vault host, keep the forced-command SSH restriction in place, and confirm user intent before reading or writing notes. <br>
Risk: A web-digest workflow may place content from untrusted external links into the vault. <br>
Mitigation: Browse or summarize external sources into the vault only when the user explicitly requests that workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logancyang/headless-vault-cli) <br>
- [Headless Vault CLI setup instructions](https://github.com/logancyang/headless-vault-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through SSH and return JSON for vault operations.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
