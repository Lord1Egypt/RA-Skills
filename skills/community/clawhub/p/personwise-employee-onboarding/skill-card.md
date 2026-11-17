## Description:

Creates a grounded interactive digital-human new-hire onboarding course from the user's supplied handbook, onboarding plan, and internal documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

People teams and course creators use this skill to turn handbooks, onboarding plans, and internal documentation into an interactive private course for new hires. It supports grounded voice-question answers and optional assessments while routing individual HR, legal, compensation, or benefits questions to appropriate contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive HR or onboarding materials may be uploaded to PersonWise for course creation.

Mitigation: Use only user-selected materials needed for the course and keep the default private access unless broader access is explicitly requested.

Risk: The workflow may install or update the PersonWise CLI.

Mitigation: Require explicit approval before installation or update and use the verified PersonWise CLI flow bundled with the release.

Risk: Generated onboarding content could overstate unsupported policy, HR, legal, compensation, or benefits details.

Mitigation: Ground the course only in supplied materials, avoid unsupported claims, and route individual matters to the appropriate internal contact.

Risk: OAuth or upload workflows could expose credentials or private file contents if handled carelessly.

Mitigation: Use browser OAuth, do not request or handle secrets, and do not expose upload grants, signed URLs, or private source contents.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/personwiseai/skills/personwise-employee-onboarding)
- [PersonWise publisher profile](https://clawhub.ai/user/personwiseai)
- [PersonWise service](https://personwise.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON inputs and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create bounded JSON blueprint or patch files and invoke PersonWise CLI commands with user-approved installation, OAuth, and upload flows.]

## Skill Version(s):

2.1.9 (source: server release metadata and skill invocation attribution)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
