## Description: <br>
Operates Grist through an OOMOL-connected account using the oo CLI to read, create, update, and delete data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Grist workspaces, documents, tables, columns, and records, and to perform confirmed row mutations through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Grist account. <br>
Mitigation: Install only when the skill name, publisher, and requested permissions match expectations; reconnect or authenticate only after an action fails with a relevant auth or connection error. <br>
Risk: Write and destructive actions can change or delete Grist records. <br>
Mitigation: Confirm the exact payload, target records, and intended effect with the user before running write or destructive actions. <br>


## Reference(s): <br>
- [ClawHub Grist skill page](https://clawhub.ai/oomol/oo-grist) <br>
- [Grist homepage](https://www.getgrist.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema lookup before building Grist action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
