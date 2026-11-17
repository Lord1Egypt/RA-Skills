## Description:

Scans draft social media posts for platform-specific publishing risks and returns PASS/WARN/FAIL rule results with fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content teams use this skill to check draft posts for Reddit, LinkedIn, Twitter/X, and Hacker News before publishing. It helps surface platform-specific warnings, failures, and concrete edits for content quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic platform advice can be inaccurate or become outdated, especially around algorithms, reach multipliers, link placement, and shadowbans.

Mitigation: Review recommendations critically and confirm current platform policies or observed behavior before changing publishing strategy.

Risk: The checker could be misused to evade moderation, spam controls, or platform rules.

Mitigation: Use the output only for legitimate content quality review and do not use it to bypass platform enforcement.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-platform-rules-engine)

## Skill Output:

**Output Type(s):** [text, json, guidance, shell commands]

**Output Format:** [Plain-text CLI report or JSON object with platform, word count, score, verdict, and per-rule results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate clear, warnings, or failures; no external dependencies.]

## Skill Version(s):

1.0.3 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
