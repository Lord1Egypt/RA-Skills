## Description: <br>
CLI for reading and managing macOS Contacts, including search, full contact display, create, update, delete, and contact list membership management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bdwelle](https://clawhub.ai/user/bdwelle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill on macOS to look up contact details, create or update contacts, delete contacts, and manage contact list membership through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify sensitive macOS Contacts data. <br>
Mitigation: Grant Contacts access only when acceptable, use narrow searches, and treat returned contact data as private. <br>
Risk: Create, update, delete, and list-membership actions can change real contacts, and delete --force bypasses confirmation. <br>
Mitigation: Confirm exact contact identities before write actions and avoid delete --force unless certain. <br>
Risk: The included live tests can modify the real Contacts store. <br>
Mitigation: Run tests only when prepared for Contacts changes, preferably with disposable fixture contacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bdwelle/mac-contacts) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bdwelle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [YAML contact data, success or error text, and command-oriented guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Contacts permission; read outputs can contain personal contact data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
