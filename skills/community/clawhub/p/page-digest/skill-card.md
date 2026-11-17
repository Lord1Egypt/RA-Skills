## Description:

Fetch a web page and produce a structured markdown digest: title, key points, entities, action items, and a one-paragraph TL;DR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill when they have a public URL and need a concise briefing, extracted key points, named entities, or action items from the page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summaries of web pages can be incomplete, misleading, or affected by prompt-injection-like page content.

Mitigation: Review the generated digest before acting on it, especially for high-impact decisions.

Risk: Using the skill on private or login-only pages could expose sensitive content to an agent workflow.

Mitigation: Use the skill only with publicly accessible pages unless the deployment has approved controls for private content.

Risk: Long pages can be truncated, which may omit relevant context.

Mitigation: Treat truncation warnings as a signal to inspect the source page or fetch a narrower section.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/page-digest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest includes a title, TL;DR, key points, entities, and action items; public page content may be truncated at 20000 characters.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
