## Description:

Turn SOP documents into an askable digital-human procedure course.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to create PersonWise digital-human training courses from user-supplied SOP, procedure, process, or policy documents. It is intended for grounded training content where the source document remains the authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install or update the PersonWise CLI in the user's profile.

Mitigation: Require explicit Host approval for install or update commands and check the command before approving it.

Risk: The workflow uses browser OAuth and an account alias for PersonWise access.

Mitigation: Use browser OAuth only, pin the returned account alias, and do not request or handle passwords, tokens, codes, cookies, or secrets.

Risk: Selected SOP or policy documents may be uploaded to PersonWise to create the course.

Mitigation: Upload only files the user named, attached, or explicitly approved, and do not expose local source contents or upload grants.

Risk: Course creation can spend existing PersonWise course credits.

Mitigation: Create only the requested number of courses, check readiness before each new course, and never purchase credits automatically.

Risk: Courses can expose process or policy content if published or shared by link.

Mitigation: Default new courses to private access unless the user intentionally requests link access, publication, or topic submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-sop-process-training)
- [PersonWise service](https://personwise.ai)
- [PersonWise CLI release origin](https://releases.personwise.ai/cli/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create bounded JSON blueprint files and invoke PersonWise CLI commands; final course output is hosted by PersonWise.]

## Skill Version(s):

2.1.9 (source: server release metadata and skill attribution block)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
