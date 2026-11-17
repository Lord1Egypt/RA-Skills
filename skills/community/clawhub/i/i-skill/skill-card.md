## Description:

Generates personalized interaction guides by analyzing user conversations so assistants can adapt responses to user preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistant operators use i-skill to create and maintain a concise local personalization profile that lets an agent adapt language, format, and recommendations after manual activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and mutates a persistent local personalization profile and related consent or audit logs.

Mitigation: Use a dedicated private data directory with restricted permissions and avoid storing sensitive identifiers in the profile.

Risk: Consent and sanitization protections are described, but the security evidence says they are incomplete until enforced directly in code.

Mitigation: Review profile updates before use and treat consent and sanitization behavior as requiring human oversight before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neuhanli/skills/i-skill)

## Skill Output:

**Output Type(s):** [markdown, guidance, configuration]

**Output Format:** [Markdown personalization profile with supporting local JSON and log records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile content is intended to remain concise and is updated only after activation or explicit update consent.]

## Skill Version(s):

3.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
