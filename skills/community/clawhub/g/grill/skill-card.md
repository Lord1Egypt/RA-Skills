## Description:

Use when a technical writeup, blog post, war story, or "Show HN" is about to go to Hacker News, Lobsters, or any skeptical technical audience, or when the user says "grill this", "make it HN-ready", "harden this post", "is this ready to post", "will this survive the comments". Hardens facts, sourcing, voice, and comment-readiness. Not for identity/infra leak scrubbing (use plate) or repo publication (use publish-readiness).

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use Grill to prepare technical posts for skeptical audiences by checking factual claims and sourcing, tightening the voice, and anticipating likely objections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grill does not perform identity or infrastructure leak scrubbing, so its review alone may leave sensitive details in a draft.

Mitigation: Run the separate plate skill for an identity and infrastructure review before publishing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/escoffier-labs/skills/grill)
- [Publisher profile](https://clawhub.ai/user/escoffier-labs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown with revised prose and editorial feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-specific critique, sourcing notes, and revised text when requested.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
