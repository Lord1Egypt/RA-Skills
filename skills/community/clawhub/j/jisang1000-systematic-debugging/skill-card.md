## Description:

Debug through a structured root-cause process instead of guesswork. Use when commands fail, tools behave unexpectedly, automations break, integrations only partially work, or the real cause is unclear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisang1000](https://clawhub.ai/user/jisang1000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use this skill to guide agents through a structured root-cause debugging process for failed commands, unexpected tool behavior, broken automations, integration issues, and unclear failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate across many troubleshooting situations and steer the agent toward its debugging workflow even when a narrower response would suffice.

Mitigation: Review the trigger and scope during deployment, and narrow activation criteria if the skill is used in environments with specialized incident or support procedures.

Risk: The artifact includes a non-English example that may be mistaken for normative behavior instead of an illustration.

Mitigation: Treat examples as illustrative and adapt user-facing diagnostic summaries to the deployment language and communication standards.

## Reference(s):

- [Systematic Debugging Skill Page](https://clawhub.ai/jisang1000/skills/jisang1000-systematic-debugging)
- [Publish Notes](artifact/references/publish-notes.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with concise diagnostic steps and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses responses on symptom, confirmed cause, and fix or next blocker.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
