## Description:

Developer Quickstart turns supplied API documentation and SDK guides into a grounded interactive digital-human course for a learner's first successful API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and technical adoption teams use this skill to turn supplied API documentation, SDK guides, and reference material into a first-call course. The course is grounded in the provided sources and designed for an interactive digital-human presenter with learner voice questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update flow can run service-provided shell commands during CLI or skill updates.

Mitigation: Review update prompts carefully and approve only expected PersonWise commands without unexpected executables, shell operators, redirects, unusual paths, or non-PersonWise origins.

Risk: The workflow can upload source materials, consume existing course credits, and change publication access.

Mitigation: Use only user-named or approved materials, rely on explicit course requests for credit use, keep new courses private unless broader access is requested, and publish only when asked.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-developer-quickstart)
- [PersonWise Publisher Profile](https://clawhub.ai/user/personwiseai)
- [PersonWise Service Descriptor](artifact/assets/service-descriptor.signed.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces course blueprints, CLI commands, status summaries, review guidance, and final course delivery details.]

## Skill Version(s):

2.1.9 (source: server release evidence and skill invocation attribution)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
