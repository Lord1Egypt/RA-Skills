## Description:

Generates and iterates a shareable OpenCard profile card from local OpenClaw identity, configuration, skills, and session statistics, producing an HTML preview and optional PNG export while treating profile data as read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timothyliew2](https://clawhub.ai/user/timothyliew2)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to assemble a public-facing profile card from local OpenClaw data, refine AI-written card copy, preview HTML, and export a PNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses sensitive local OpenClaw profile, identity, memory, skills, and session metadata excerpts.

Mitigation: Review USER.md, IDENTITY.md, and MEMORY.md before use, and prefer local models or curated excerpts when profiles contain sensitive content.

Risk: Cloud model use can send generated-card context excerpts to the model provider during copy generation.

Mitigation: Use a local model or explicitly chosen excerpts when external model processing is not acceptable.

Risk: Temporary JSON and HTML preview files can contain profile or memory-derived content.

Mitigation: Write temporary outputs outside the packaged skill directory and remove them after rendering or export.

Risk: Browser rendering can request external background image and font resources, exposing client IP and HTTP metadata.

Mitigation: Use trusted background image URLs or local image paths, and use local assets when network metadata exposure is a concern.

## Reference(s):

- [OpenCard Data Flow](references/data-flow.md)
- [Background Template](references/background-template.html)
- [ClawHub Skill Page](https://clawhub.ai/timothyliew2/skills/open-card)
- [Node.js](https://nodejs.org/)
- [Google Chrome](https://www.google.com/chrome/)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [JSON data, HTML preview, PNG image export, and Markdown guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+ for data collection and HTML rendering; PNG export additionally requires Node.js, npm, playwright-core, and local Chrome or Chromium.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
