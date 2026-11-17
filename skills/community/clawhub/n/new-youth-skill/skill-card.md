## Description:

New Youth.skill is a bilingual reflective coaching skill based on Chen Duxiu's six New Youth standards, helping users assess character, examine claims, expand perspectives, make decisions, plan daily practice, and translate ideas into action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill for reflective coaching in Chinese or English: self-assessing against six character standards, scrutinizing evidence and logic, comparing perspectives, and turning decisions into concrete next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic session-start behavior can apply the skill's persona to unrelated conversations without clear user opt-in.

Mitigation: Review host hook behavior before installation; disable or remove the session-start hook if the skill should only run when explicitly invoked.

Risk: Reflective coaching can sound authoritative when the user's issue needs evidence checking or professional judgment.

Mitigation: Use the skill as decision-support guidance, verify factual claims independently, and keep the final decision with the user.

## Reference(s):

- [New Youth Six Standards](artifact/references/six-standards.md)
- [Application Cases](artifact/references/application-cases.md)
- [Persona Layer](artifact/references/persona-layer.md)
- [Historical Narratives](artifact/references/historical-narratives.md)
- [30 Classic Quotes](artifact/references/30-classic-quotes.md)
- [ClawHub Skill Page](https://clawhub.ai/moroiser/skills/new-youth-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with optional shell command examples and script-generated text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external APIs required; optional Python helper scripts generate daily tasks and self-assessment reports.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
