## Description:

Mother.skill helps users preserve local memories of their mother, including stories, advice, recipes, sayings, values, voice, and grief-aware memorial context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize personal memories of their mother into a local archive and to receive responses grounded in documented memories, values, recipes, and voice patterns. It is intended for both living and memorial contexts, with explicit grief-aware behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive personal memories about a mother and family members on the local device.

Mitigation: Use it only when local storage of those memories is acceptable, avoid adding details without appropriate family consent, and delete ~/.mother-skill/ to remove the archive.

Risk: Memorial or grief-related prompts may involve emotionally sensitive situations.

Mitigation: Keep responses grounded in documented memories and avoid filling gaps or fabricating details when the archive lacks a relevant memory.

## Reference(s):

- [Memory Preservation Guide](references/preservation-guide.md)
- [Mother Profile Template](templates/MOTHER-PROFILE.md)
- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/skills/mother)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and JSONL-oriented guidance for local memory archive entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local user-provided memory content under ~/.mother-skill/; no external transmission is described in the evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
