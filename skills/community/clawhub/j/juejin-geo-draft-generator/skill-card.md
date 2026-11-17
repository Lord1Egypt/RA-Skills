## Description:

Assists developers and technical content teams in turning AI-GEO content assets into Juejin-style article drafts, metadata, and publish review materials for manual publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operations teams use this skill to adapt local AI-GEO brand assets into Juejin-ready technical drafts, summaries, title candidates, tags, and a pre-publication checklist. The browser-fill flow is intended to assist draft preparation while leaving review, saving, and final publishing under human control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated articles, titles, tags, or summaries may contain factual errors, unsupported claims, or over-marketing.

Mitigation: Review generated content against the publish checklist and source assets before saving or publishing.

Risk: The optional browser automation uses a visible browser session and may interact with sensitive logged-in account state.

Mitigation: Do not export credentials or browser storage, stop for login or risk-control prompts, and keep final saving and publishing as manual actions.

Risk: The example automation depends on Playwright behavior and may overwrite clipboard contents while filling article text.

Mitigation: Install it in a virtual environment, pin Playwright for operational use, and expect clipboard contents to be replaced during the draft-fill flow.

Risk: Brand inputs and generated drafts may contain sensitive business information.

Mitigation: Treat local input files as sensitive and confirm the selected model and runtime privacy settings before generating drafts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljseeking/skills/juejin-geo-draft-generator)
- [Juejin Creator Draft Page](https://juejin.cn/creator/content/article/draft)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, generated draft text, title and tag lists, checklist content, and optional Playwright-assisted browser actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files under output/juejin and requires human review before any Juejin publication.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog, released 2026-05-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
