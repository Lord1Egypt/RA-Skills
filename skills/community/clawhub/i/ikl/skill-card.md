## Description: <br>
Interpersonal Knowledge Layer helps an agent gate disclosure of a user's personal information through per-contact permissions, contact matching, sensitivity categories, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smartinelle](https://clawhub.ai/user/smartinelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use IKL when an assistant receives requests for a user's personal details and needs to decide whether to share, deny, ask the user, or update contact permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve highly sensitive personal information stored in local plaintext files. <br>
Mitigation: Populate knowledge.json minimally, avoid unnecessary bank details or medical history, and protect or remove the local ikl/ files according to the user's environment. <br>
Risk: Default relationship permissions may be broader than a user expects. <br>
Mitigation: Review or zero out the starter permission matrix before use, then add only the categories and levels the user explicitly approves. <br>
Risk: The permission gate should not be treated as technically isolated access control by itself. <br>
Mitigation: Use the skill as policy guidance unless real access controls are added around stored data and tool/file access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smartinelle/ikl) <br>
- [Security design](references/security-design.md) <br>
- [Permissions schema](references/schema-permissions.md) <br>
- [Contacts schema](references/schema-contacts.md) <br>
- [Knowledge schema](references/schema-knowledge.md) <br>
- [Audit log format](references/audit-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with a bash setup command and JSON configuration file schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local ikl/ starter files when setup.sh is run; users populate personal data and permissions manually.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
