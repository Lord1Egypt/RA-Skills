## Description: <br>
Reference the workspace policy playbook, answer "What are the rules for tone, data, and collaboration?" by searching the curated policy doc or listing its sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, developers, and workspace maintainers use this skill to list policy topics, retrieve a matching policy section, or search policy text before drafting announcements or answering policy questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user-supplied --policy-file path can cause the CLI to print matching content from any readable file selected by the user. <br>
Mitigation: Use --policy-file only with intended policy documents and avoid paths that may contain secrets, credentials, or unrelated private information. <br>


## Reference(s): <br>
- [Workspace policies](references/policies.md) <br>
- [Policy Lawyer on ClawHub](https://clawhub.ai/CrimsonDevil333333/policy-lawyer) <br>
- [CrimsonDevil333333 publisher profile](https://clawhub.ai/user/CrimsonDevil333333) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with policy headings, sections, or matching snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read an alternate user-supplied policy document path when --policy-file is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
