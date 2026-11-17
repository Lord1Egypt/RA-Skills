## Description:

Narrative Focus helps agents detect and correct narrative weight misalignment in technical tutorials, deep-dive explainers, interview preparation articles, and framework comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[co-kyo](https://clawhub.ai/user/co-kyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical writers use this skill to label collected technical details by role before writing, or to review draft technical articles for misplaced narrative emphasis and propose focused corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may cause the skill to engage during general article-review prompts.

Mitigation: Use explicit wording when requesting narrative focus review, role labeling, or narrative weight correction.

Risk: Article corrections could introduce incorrect or misleading technical claims if narrative emphasis changes alter factual meaning.

Mitigation: Review proposed edits before applying them and use the skill's authoritative verification step for modified technical claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/co-kyo/skills/narrative-focus)
- [README](artifact/README.md)
- [Pre-processing: Collection & Labeling SOP](artifact/references/pre-processing.md)
- [Post-processing: Detection & Correction SOP](artifact/references/post-processing.md)
- [Proposition Granularity Guide](artifact/references/proposition-granularity-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, role labels, correction guidance, and revised article prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Architectural, Transport, and Configurable labels; detection verdicts; local correction proposals; and authoritative verification statuses for modified technical claims.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
