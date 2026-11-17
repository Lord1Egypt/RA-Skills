## Description:

Companion spirit system for OpenClaw agents that deterministically generates and displays a unique spirit profile from a user identity seed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahaaiclub](https://clawhub.ai/user/ahaaiclub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to add a local companion feature that can show a bilingual spirit card, generate personality details, track simple profile state, and respond briefly in character when invoked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a platform ID, username, or name as a deterministic seed and save a local companion profile in the skill directory.

Mitigation: Use a stable non-sensitive identifier when possible, avoid secrets or private data as seeds, and review the saved companion profile before sharing the skill directory.

Risk: Passive companion appearances may interrupt serious work contexts.

Mitigation: Prefer explicit commands such as spirit show, spirit stats, spirit talk, or spirit rename, and keep passive appearances limited or disabled when interruptions matter.

## Reference(s):

- [OpenClaw Spirits Complete Species Guide](artifact/openclaw-spirits/references/species-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/ahaaiclub/skills/openclaw-spirits)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands, ASCII cards, and JSON companion data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a local companion profile in the skill directory.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
