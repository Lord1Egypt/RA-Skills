## Description:

Teaches this agent how to serve content to the OpenPot iOS client: cards, apps, page captures, calendar, voice, chat persistence, and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almnotai](https://clawhub.ai/user/almnotai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to teach an agent how to integrate with OpenPot iOS surfaces, including chat, Pulse cards, calendar, apps, terminal, voice, page captures, chat persistence, and onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through device approval and SSH access setup, which may grant deep access to the agent environment.

Mitigation: Install only when that access is expected, manually verify each device pairing, avoid approving the first pending request by name alone, and review SSH keys after setup.

Risk: Chat, calendar, and page-capture data may be retained by the environment configured for OpenPot.

Mitigation: Review retention expectations before enabling persistence and limit access to stored conversation, schedule, and capture data.

Risk: The bundled Weather and Billable Hours apps are reported by security evidence as having unsafe HTML rendering.

Mitigation: Patch or avoid those bundled apps until their unsafe rendering is fixed.

## Reference(s):

- [OpenPot homepage](https://openpot.app)
- [ClawHub skill page](https://clawhub.ai/almnotai/skills/openpot-awareness)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, HTML, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Pulse card JSON, calendar blocks, setup instructions, self-contained HTML apps, and configuration guidance for OpenPot integrations.]

## Skill Version(s):

6.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
