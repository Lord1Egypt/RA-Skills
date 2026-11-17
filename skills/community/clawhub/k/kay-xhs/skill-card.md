## Description:

Kay Xhs helps agents research Xiaohongshu trends, generate AI images or comics through kay-image, draft post copy, and save image posts to Xiaohongshu drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papayalove](https://clawhub.ai/user/papayalove)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content teams can use this skill to plan Xiaohongshu posts, create visual assets and captions, and prepare draft uploads. Developers and agent operators can use it as a guided workflow that combines browser-based research, kay-image generation, and draft-saving steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate against a logged-in Xiaohongshu creator session and upload selected local images.

Mitigation: Review selected files, generated copy, and browser actions before upload; require explicit approval before publishing and prefer saving drafts for review.

Risk: The skill depends on kay-image and a KIE API key.

Mitigation: Use a narrowly scoped API key, verify or pin the kay-image dependency before use, and avoid placing secrets in shared logs or generated content.

Risk: The security evidence notes third-party data extraction and mandatory persistent memory writes without enough scoping controls.

Mitigation: Collect only permitted content, follow platform rules, and disable or manually approve memory archival unless long-term retention is intended.

## Reference(s):

- [Kay Xhs on ClawHub](https://clawhub.ai/papayalove/skills/kay-xhs)
- [Publisher Profile](https://clawhub.ai/user/papayalove)
- [KIE API](https://kie.ai/)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)
- [Xiaohongshu Case Analysis](artifact/references/cases.md)
- [Image Prompt Templates](artifact/references/prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell, JavaScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image-generation task files, image assets through kay-image, post copy, and browser automation steps that should be reviewed before upload or publication.]

## Skill Version(s):

1.0.3 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
