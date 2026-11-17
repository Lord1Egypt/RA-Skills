## Description:

Miaoji Compliance Copy helps agents scan Amazon listing copy for risky claims, suggest safer replacements, and draft Rufus-oriented listing variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace sellers and ecommerce copywriters use this skill to review product titles and bullet descriptions, identify risky wording, and generate compliant, search-aware rewrite options before manually publishing listing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon policy and Rufus scoring guidance is advisory and may not prove current platform compliance.

Mitigation: Verify important listing changes against current Amazon policy before publishing.

Risk: Generated rewrites may preserve or introduce unsupported product, comparative, medical, or certification claims.

Mitigation: Have the seller review each suggested change and keep required substantiation for regulated or comparative claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/miaoji-compliance-copy)
- [Publisher profile](https://clawhub.ai/user/wangm-a3)
- [Banned words reference](artifact/references/banned-words.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports and listing rewrite drafts, with optional JSON from the bundled checker script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes compliance issue summaries, replacement suggestions, Rufus keyword coverage, three rewrite variants, and search term suggestions.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
