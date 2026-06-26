## Description: <br>
Operates Formbricks through an OOMOL-connected account to read, create, update, and delete contacts and contact attribute keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage Formbricks contacts and contact attribute keys through the OOMOL connector from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires account-connected Formbricks access through OOMOL and may expose account data if used in the wrong workspace. <br>
Mitigation: Confirm the active OOMOL/Formbricks connection and workspace context before running actions that access or change data. <br>
Risk: Write and destructive actions can create, update, or delete Formbricks contact records or attribute keys. <br>
Mitigation: Inspect the live connector schema, confirm the exact payload and target with the user, and require explicit approval before destructive actions. <br>


## Reference(s): <br>
- [ClawHub Formbricks Skill](https://clawhub.ai/oomol/oo-formbricks) <br>
- [Formbricks Homepage](https://formbricks.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an authenticated OOMOL account, and a connected Formbricks account.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
