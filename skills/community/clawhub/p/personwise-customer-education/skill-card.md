## Description:

Turn support knowledge into an askable digital-human customer course.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Customer education, support, and enablement teams use this skill to build an interactive digital-human course from their own help center articles, product documentation, or support playbooks around a high-frequency customer question cluster.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the update flow can make the agent run command text supplied by the PersonWise CLI or service after broad approval.

Mitigation: Only approve installs or updates when the shown command is a known PersonWise bootstrap or exact upgrade command from the installed skill directory; avoid approving arbitrary shell text returned by the service or CLI.

Risk: The skill can install or update the PersonWise CLI and then use browser OAuth and course credits to create customer education courses.

Mitigation: Require explicit user approval for install or update commands, use the market-bound CLI/service declared by the release, never handle secrets, and rely on readiness checks before creating courses.

Risk: A course could imply unsupported troubleshooting, certification, competence, or issue resolution if source material is stretched beyond its evidence.

Mitigation: Keep course content grounded in supplied materials, present it as education rather than support diagnosis or an SLA, and escalate unsupported or account-specific questions to the user's support channel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-customer-education)
- [PersonWise Service](https://personwise.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create bounded JSON input files and returns secret-free course, run, source, review, access, and playability evidence.]

## Skill Version(s):

2.1.9 (source: server release metadata and skill attribution block)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
