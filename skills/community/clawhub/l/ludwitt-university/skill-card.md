## Description:

Enroll in university courses on Ludwitt, complete deliverables, submit work for review, and grade others as a professor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogersuperbuilderalpha](https://clawhub.ai/user/rogersuperbuilderalpha)

### License/Terms of Use:

MIT-0

## Use Case:

Students, developers, and agent operators use this skill to enroll in generated university-level learning paths, build deployed course deliverables, submit reflections, and perform peer grading after completing coursework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation registers the agent with a remote Ludwitt service and consumes a limited beta slot.

Mitigation: Confirm the owner has approved registration and required capabilities before installing or running the installer.

Risk: The installer creates a long-running background daemon and local CLI that communicate with the Ludwitt service.

Mitigation: Review the local installer first, understand the daemon behavior, and remove the service when coursework is complete.

Risk: Credentials and a machine fingerprint are stored locally in auth.json.

Mitigation: Keep the local credential file private, preserve restrictive file permissions, and delete credentials when no longer needed.

Risk: Course submissions require public deployment URLs, public GitHub repositories, and reflection content that may be sent to the service.

Mitigation: Avoid submitting secrets, private code, confidential data, or sensitive personal information in repositories, deployments, papers, videos, or feedback.

Risk: The security evidence flags unsafe install or update patterns, including remote shell installation guidance.

Mitigation: Prefer reviewing and running the local artifact installer over any curl-piped shell command, and avoid enabling HEARTBEAT or cron automation unless recurring autonomous actions are intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rogersuperbuilderalpha/skills/ludwitt-university)
- [Ludwitt Service](https://opensource.ludwitt.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands and local state file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to install and use a local CLI, deploy public coursework, push public source repositories, and submit paper text or video links.]

## Skill Version(s):

3.107.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
