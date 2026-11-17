## Description:

The OpusClip craft skill turns long videos such as podcasts, webinars, interviews, and streams into publishable short clips through AI candidate finding, honest triage, and a human-reviewed workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and social media operators use this skill to plan OpusClip pipelines for turning long-form recordings into reviewed, scheduled short-form clips. The skill helps agents produce source-selection guidance, credit math, triage criteria, clip QA checklists, and publishing handoff guidance while keeping a human approver in the loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpusClip pricing, tier limits, editor access, and API availability may change or conflict across sources.

Mitigation: Verify current plan details and API access in OpusClip before subscribing, promising automation, or running a production workflow.

Risk: Unreviewed publishing can release caption errors, unfair clips, misleading context, or low-quality reframes.

Mitigation: Keep human approval before every publish and do not grant connected publishing tools permission to auto-post without review.

Risk: The Virality Score can be mistaken for proof of clip quality or expected performance.

Mitigation: Use the score only for triage, compare published clips against real retention data, and let human judgment override score-based decisions.

Risk: Credit usage and processing reliability can surprise users when long or untrimmed source videos are uploaded.

Mitigation: Trim source files before upload, calculate monthly source minutes before choosing a plan, build schedule slack, and download exports promptly.

## Reference(s):

- [The CLIPS framework](references/the-clips-framework.md)
- [The reality of OpusClip in 2026](references/opus-clip-2026-reality.md)
- [Scope, distinctions & connections](references/scope-and-connections.md)
- [Workflows, checklists & worked examples](references/workflows-and-templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with workflow steps, QA checklists, credit calculations, and publishing handoff instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve human review before publishing and should not treat OpusClip scores, tiers, API access, or pricing as final without current in-app verification.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
