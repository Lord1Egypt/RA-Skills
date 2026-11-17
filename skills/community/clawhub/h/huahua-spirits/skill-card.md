## Description:

Huahua Spirits adds a deterministic companion-spirit system to an OpenClaw agent, giving each user a persistent spirit with species, rarity, personality, bond, bilingual display cards, and light interaction behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiye1997](https://clawhub.ai/user/baiye1997)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to add a lightweight companion character that can be summoned, displayed, interacted with, and occasionally surfaced by an agent for warmth and continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passive interaction hooks can record short excerpts of user messages in local companion history.

Mitigation: Tell users what is stored, avoid routing sensitive messages through passive hooks, and provide a clear way to disable or delete the local companion history.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baiye1997/skills/huahua-spirits)
- [Species Guide](artifact/references/species-guide.md)
- [Product Spec](artifact/SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands; helper scripts may return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English spirit cards; local companion state is stored in the skill assets directory.]

## Skill Version(s):

1.4.7 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
