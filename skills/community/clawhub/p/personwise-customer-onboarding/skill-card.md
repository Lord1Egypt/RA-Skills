## Description:

Give every new customer an askable digital-human onboarding course.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

External customer-success, implementation, and training teams use this skill to turn confirmed onboarding materials into an interactive digital-human course for new customers. The course is grounded in supplied materials and supports learner voice questions, optional assessments, and private or requested broader access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CLI installation or updates may run native PersonWise executable code and sensitive update commands.

Mitigation: Proceed only when the user and host approve installation or update, and run only the bundled PersonWise bootstrap or the exact official PersonWise update command.

Risk: Browser OAuth and course-credit use can authorize account actions in the selected PersonWise account.

Mitigation: Authenticate only through PersonWise browser OAuth, pin the returned account alias, create only the requested number of courses, and never purchase credits automatically.

Risk: Selected onboarding materials may be uploaded to PersonWise services.

Mitigation: Upload only files named, attached, or explicitly selected by the user; disclose and obtain approval before uploading any agent-discovered local file.

Risk: Generated course content could overstate customer commitments or include unsupported onboarding promises.

Mitigation: Ground timelines, support channels, scope, and commitments only in confirmed materials, and route contract- or plan-specific questions back to the user's team.

Risk: An omitted access target could make the course broader than intended.

Mitigation: Set distribution_target to private unless the user explicitly asks for link access, publication, or topic submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-customer-onboarding)
- [PersonWise Publisher Profile](https://clawhub.ai/user/personwiseai)
- [PersonWise OAuth Protected Resource Metadata](https://personwise.ai/.well-known/oauth-protected-resource/api/agent)
- [PersonWise CLI Release Origin](https://releases.personwise.ai/cli/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration, Markdown]

**Output Format:** [Markdown guidance with PersonWise CLI shell commands, JSON blueprints or patches, and concise final status evidence.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local CLI installation or update approval, browser OAuth, existing course-credit use, and uploads of user-selected onboarding materials.]

## Skill Version(s):

2.1.9 (source: ClawHub release evidence and SKILL.md attribution)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
