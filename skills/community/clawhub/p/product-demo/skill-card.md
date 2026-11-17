## Description:

Turns two real screenshots of the same user interface in different states into a short Ofox demo video, with dry-run pricing and explicit approval before paid generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and documentation authors use this skill to create short before-and-after UI demo clips from screenshots they already have. It is intended for bounded UI state changes where a real screen recording is not available or not suitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates the real API work to the separate ofox-video-core skill.

Mitigation: Inspect or trust that dependency before use, and prefer a pinned or trusted installer route when the core dependency is missing.

Risk: Screenshots may contain secrets, customer data, faces, or private account details that would be sent to Ofox and appear in the generated video.

Mitigation: Remove or crop sensitive content before generation, and only submit screenshots the user intends to send to Ofox.

Risk: Paid generation can incur cost if run without the user reviewing the quote.

Mitigation: Use the dry-run cost table first and run the paid command only after explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/product-demo)
- [Source homepage](https://github.com/ofoxai/skills/tree/main/skills/product-demo)
- [Ofox app and API keys](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with prompt text, cost-table guidance, and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses dry-run pricing before paid generation and requires OFOX_API_KEY for real Ofox API calls.]

## Skill Version(s):

2.0.0 (source: evidence.json release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
