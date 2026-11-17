## Description:

Research any topic across Reddit, X/Twitter, and the web from the last 30 days. Synthesizes findings into actionable insights or copy-paste prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanbaker24](https://clawhub.ai/user/dylanbaker24)

### License/Terms of Use:


## Use Case:

Developers, researchers, and other external users use this skill to research recent discussion about fast-moving topics across web, Reddit, and X/Twitter sources and turn the findings into practical insights or reusable prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may be sent to external search services and to X/Twitter when the bird CLI is available.

Mitigation: Use this skill only for topics that are appropriate to share with those services, and invoke it explicitly for recent-research requests.

Risk: X/Twitter searches depend on the locally configured bird session and may expose queries through that account context.

Mitigation: Confirm the local bird configuration is authorized for the intended use, or omit the X/Twitter step when that source is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dylanbaker24/skills/last30days-lite)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with sourced findings, concise recommendations, and optional copy-paste prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs and synthesized patterns from public web, Reddit, and X/Twitter results.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
