## Description:

PowPow angel-round and Pre-A funding plan skill that runs an interactive investor Q&A, produces an investing-style portrait, and can prepare an optional previewed outreach email for PowPow funding discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External investors and PowPow prospects use this skill to learn about the PowPow project, answer a 13-question investor challenge, receive a non-scored investing-style portrait, and optionally prepare a contact email after preview and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users for investing-style preferences and contact details for investor outreach.

Mitigation: Contact fields are optional, at least one contact channel is required only before sending, and the skill provides a privacy notice before email submission.

Risk: Personalized openings could use prior user memory.

Mitigation: Memory use requires explicit consent, is skipped if declined or unanswered, and is not written into the outreach email.

Risk: The skill can prepare an email to the PowPow founder with the user's style portrait and contact information.

Mitigation: The skill requires a full preview and explicit send confirmation, and it can provide a redacted copy with contact details removed.

Risk: Industry-related answers may use web search and could include current-market uncertainty.

Mitigation: The skill directs the agent to prioritize official PowPow sources and to say when a question is not covered by those materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/durenzidu/skills/powpow-financing-plan-openclaw-en)
- [PowPow homepage](https://www.powpow.online/)
- [PowPow landing page](https://global.powpow.online/landing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown with optional email preview text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive Q&A, investor-style portrait, badge count, and optional redacted email copy.]

## Skill Version(s):

1.2.3 (source: artifact frontmatter and skill.json); ClawHub release version 1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
