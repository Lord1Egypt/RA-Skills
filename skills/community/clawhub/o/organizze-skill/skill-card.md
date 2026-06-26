## Description: <br>
Runs Organizze personal finance API operations via Node.js CLI scripts for accounts, categories, transactions, credit cards, and transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leaofelipe](https://clawhub.ai/user/leaofelipe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and manage their Organizze personal finance data from a terminal through CLI wrappers around the Organizze API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, transfer, or delete live Organizze financial records. <br>
Mitigation: Before write or delete actions, list the target records first and require explicit confirmation of exact IDs and payloads. <br>
Risk: The Organizze token grants account access and may expose sensitive personal finance data if mishandled. <br>
Mitigation: Store the token only in approved credential configuration, do not print credential values, and revoke or rotate the token when access is no longer needed. <br>


## Reference(s): <br>
- [Organizze API documentation](https://github.com/organizze/api-doc) <br>
- [ClawHub release page](https://clawhub.ai/leaofelipe/organizze-skill) <br>
- [Organizze app](https://app.organizze.com.br) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and pretty-printed JSON from CLI scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORGANIZZE_TOKEN, ORGANIZZE_EMAIL, ORGANIZZE_USER_AGENT, node, and npm; API operations may read, create, update, transfer, or delete live financial records.] <br>

## Skill Version(s): <br>
1.3.4 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
