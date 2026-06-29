## Description: <br>
Identify the project handle from an intake note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxt-ai](https://clawhub.ai/user/wxt-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and delivery teams use this skill to extract a concise project code from a client brief, delivery note, or project update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extracted project code may be incorrect if the intake note is ambiguous or contains multiple project-like identifiers. <br>
Mitigation: Review the returned project_code before using it in delivery, account, or ledger workflows. <br>
Risk: Users may include unnecessary sensitive details in intake notes. <br>
Mitigation: Provide only the note text needed for identification and avoid credentials, private files, and account secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxt-ai/skills/project-code-notes-identifier) <br>
- [Publisher profile](https://clawhub.ai/user/wxt-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text project_code field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a concise project code from user-provided note text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
