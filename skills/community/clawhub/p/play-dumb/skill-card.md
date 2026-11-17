## Description:

Lets an agent intentionally lower how capable it appears by using configurable role-play personas, ten dumbness levels, delayed understanding, partial knowledge, deliberate small mistakes, and clarifying questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dox012](https://clawhub.ai/user/dox012)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to activate a bounded role-play mode where the agent appears less certain, asks simpler questions, or uses one of several playful personas. It is intended for conversational tone control and guided interaction, not for tasks that require factual reliability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to make believable mistakes and appear less capable, which can produce intentionally unreliable answers.

Mitigation: Use it only for explicit role-play or tone-control scenarios, and disable it for factual work, production coding, or decisions where correctness matters.

Risk: Safety overrides exist for medical, legal, financial, personal-safety, frustration, and repeated-query scenarios, but the scanner notes weak controls around when the behavior applies.

Mitigation: Require clear activation controls and verify the mode exits or falls back to normal answering whenever a consequential or frustrated-user scenario is detected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dox012/skills/play-dumb)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dox012)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language agent responses, usually plain text or Markdown, with code blocks or shell commands only when the underlying user request calls for them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may intentionally include uncertainty, simplified reasoning, clarifying questions, or believable mistakes while the mode is active.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
