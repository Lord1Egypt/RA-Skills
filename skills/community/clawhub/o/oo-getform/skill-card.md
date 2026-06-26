## Description: <br>
Operate Getform (forminit.com) through an OOMOL-connected account for reading, creating, and updating form data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to operate Getform through an OOMOL-connected account, including listing protected Forminit submissions and submitting protected forms. It is intended for schema-first connector use through the oo CLI rather than direct API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance includes remote CLI installer commands that can execute local code. <br>
Mitigation: Prefer the official OOMOL install guide, verify the installer source, and get explicit user approval before running an installer. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Getform account. <br>
Mitigation: Install and use it only when OOMOL-mediated Getform access is acceptable, and rely on the connected account scopes required for the task. <br>
Risk: The submit_form action can write data to a protected Forminit form. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Getform homepage](https://forminit.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce oo CLI connector commands and JSON payload guidance for Getform actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
