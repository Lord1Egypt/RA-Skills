## Description:

Builds sales or fundraising pitch narratives from an existing narrative canon as a problem-to-ask slide-beat outline, tying proof beats to claim IDs and flagging unsupported proof as [needs source].

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales, and fundraising teams use this skill to convert an existing narrative canon into a pitch deck outline for investors, sales prospects, or both. It preserves the canon as the source of truth while identifying unsupported proof that needs claims review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request persistent memory writes that are not declared in the distribution manifest capabilities.

Mitigation: Review proposed destinations and payloads before installation or execution; prefer inline proposals or narrowly scoped write permissions.

Risk: Unverified proof or comparative claims could be misleading if used in a pitch without review.

Mitigation: Keep proof beats labeled with approved claim IDs or [needs source] and route unsupported claims for claims review before external use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/pitch-narrative-builder)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown narrative outline with slide-beat mappings and claim-status labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audience-specific ask variants, proof beats tied to claim IDs or [needs source], and a handoff summary.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
