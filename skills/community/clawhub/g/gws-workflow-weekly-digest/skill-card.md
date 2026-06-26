## Description: <br>
Google Workflow: Weekly summary: this week's meetings + unread email count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and productivity-focused agents use this skill to generate a read-only weekly Google Workspace digest that combines this week's meetings with an unread email count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured or untrusted gws command or Google account could expose calendar and email metadata to the wrong environment. <br>
Mitigation: Before installing, confirm the gws command comes from a trusted source, review the shared Google Workspace auth instructions, and use the intended Google account and scopes for a read-only weekly digest. <br>
Risk: The generated weekly digest may contain sensitive meeting or email summary information. <br>
Mitigation: Review the digest before sharing it and restrict output to authorized recipients or systems. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/googleworkspace-bot/gws-workflow-weekly-digest) <br>
- [Shared Google Workspace auth and global flags](../gws-shared/SKILL.md) <br>
- [Google Workspace workflow commands](../gws-workflow/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CLI output options for json, table, yaml, or csv.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and Google Workspace authentication; the documented workflow is read-only.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
