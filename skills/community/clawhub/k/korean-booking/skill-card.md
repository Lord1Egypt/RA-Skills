## Description:

Korean Booking helps users find Korean and Seoul beauty clinics, review appointment options, open BeautsGO clinic pages, contact online support, and submit appointment requests with user-provided details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to look up Korean beauty and medical-aesthetic clinics, compare booking paths, open clinic detail, price, and support pages, and submit appointment requests after providing contact details.

### Deployment Geography for Use:

Global, with service content focused on Korean and Seoul beauty clinics.

## Known Risks and Mitigations:

Risk: The skill can open unvalidated URLs through shell commands.

Mitigation: Require URL allowlisting and use a shell-free browser-opening path before deployment.

Risk: The skill can submit appointment requests using user contact details.

Mitigation: Require explicit user confirmation immediately before each appointment submission.

Risk: Appointment contact data may be logged in plaintext.

Mitigation: Remove or redact contact-data logs before production use.

Risk: Developer sync scripts can modify the local OpenClaw cache.

Mitigation: Do not run developer sync scripts unless intentionally maintaining a local OpenClaw development environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beautsgo/skills/korean-booking)
- [Skill Definition](SKILL.md)
- [README](README.md)
- [Multi-turn Flow](docs/multi-turn-flow.md)
- [Consult Automation](docs/consult-automation.md)
- [BeautsGO Website](https://beautsgo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with appointment guidance, status messages, and browser-operation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-facing booking summaries and next-step guidance after browser or appointment actions.]

## Skill Version(s):

2.6.8 (source: SKILL.md frontmatter and server release evidence; package.json reports 2.1.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
