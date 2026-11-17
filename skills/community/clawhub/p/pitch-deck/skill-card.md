## Description:

Pitch Deck helps agents create pitch deck outlines, slide structures, fundraising storylines, investor Q&A preparation, demo day materials, and feedback improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and fundraising teams use this skill to draft investor-facing pitch deck structures, market-sizing sections, financial projections, competitor analysis, and preparation material for investor conversations or demo days.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential fundraising or business inputs may be stored locally in plaintext history or data files by the generic helper.

Mitigation: Use a dedicated, access-controlled data directory, avoid entering confidential material unless local retention is acceptable, and review or remove generated local data files after use.

Risk: The helper's removal behavior may give users the impression that stored entries were deleted when they were not fully removed.

Mitigation: Manually inspect the configured data directory and delete retained data or history files when removal of sensitive entries is required.

## Reference(s):

- [Pitch Deck tips](artifact/tips.md)
- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/pitch-deck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with command-oriented pitch deck guidance and tabular calculations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include slide outlines, market-sizing calculations, unit economics, financial projections, competitive analysis prompts, and investor preparation guidance.]

## Skill Version(s):

2.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
