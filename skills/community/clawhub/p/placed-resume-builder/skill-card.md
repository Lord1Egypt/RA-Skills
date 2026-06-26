## Description: <br>
This skill helps users build, update, template, export, download, and manage resumes through the Placed career platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and career-focused agents use this skill to create, edit, template, and export resumes through Placed. It is suited for resume management workflows that require authenticated API calls and optional PDF, DOCX, JSON, or Markdown exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume content is sent to the Placed service during authenticated API calls. <br>
Mitigation: Use the skill only when the user trusts Placed with the resume data being created, updated, exported, or downloaded. <br>
Risk: The skill can persist a Placed API key in ~/.config/placed/credentials. <br>
Mitigation: Use a revocable API key and protect or delete the local credentials file if persistent access is not desired. <br>
Risk: Resume updates, template changes, and visibility changes may affect user-facing career materials. <br>
Mitigation: Review requested changes and visibility settings before submitting API calls. <br>


## Reference(s): <br>
- [Placed Resume Builder API Reference](references/api-guide.md) <br>
- [Placed Resume Builder on ClawHub](https://clawhub.ai/ajitsingh25/placed-resume-builder) <br>
- [Placed homepage](https://placed.exidian.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return resume data, template details, expiring PDF or DOCX download URLs, JSON exports, or Markdown exports from the Placed API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
