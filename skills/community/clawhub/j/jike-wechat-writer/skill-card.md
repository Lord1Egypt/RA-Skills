## Description:

Jike WeChat Writer guides agents through WeChat public-account article creation, including topic selection, research, style adaptation, Markdown drafting, image planning, and WeChat-ready HTML rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzoob](https://clawhub.ai/user/mzoob)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content teams use this skill to turn ideas, links, or source material into WeChat public-account articles. It supports trend research, style matching, draft iteration, image handling, and optional HTML formatting for WeChat editors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes authenticated calls to the 100.city API and allows the API base URL to be configured.

Mitigation: Install only from a trusted publisher, keep the API key private, and avoid setting 100CITY_BASE_URL to untrusted hosts.

Risk: The skill can fetch external URLs for style extraction and image-related workflows.

Mitigation: Do not provide internal, private, or sensitive URLs; review fetched-source assumptions before using generated content.

Risk: The skill can write article, theme, and persistent memory files.

Mitigation: Review generated files and MEMORY.md updates before publishing, sharing, or reusing them in later work.

Risk: Generated HTML may contain active or unsafe content for downstream publishing surfaces.

Mitigation: Treat rendered HTML as untrusted until reviewed and sanitized for the target WeChat publishing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzoob/skills/jike-wechat-writer)
- [Module A: Topic and Direction](artifact/references/module-a-topic.md)
- [Module B: Memory Adaptation](artifact/references/module-b-memory.md)
- [Module C: Style Matching](artifact/references/module-c-style.md)
- [Module D: Writing and Iteration](artifact/references/module-d-writing.md)
- [Module E: Image Strategy](artifact/references/module-e-image.md)
- [Module F: WeChat Styling](artifact/references/module-f-styling.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown article files, image URLs, configuration guidance, and WeChat-compatible HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a 100CITY_API_KEY for API-backed search, trend, style-analysis, and image-generation features; may update article, theme, and memory files.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
