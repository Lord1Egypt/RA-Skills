## Description:

Build and format email newsletters from agent-curated content. Sections, formatting, subscriber-friendly HTML output. Works with any email service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect newsletter items, organize them into sections, draft newsletter copy, and export subscriber-ready content for an email service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newsletter items are stored locally in newsletter-items.json, so local data loss or unauthorized local access could affect draft content.

Mitigation: Keep backups of important newsletter drafts and protect the local workspace where the skill stores draft items.

Risk: Generated Markdown may include untrusted titles, notes, or URLs directly in newsletter output.

Mitigation: Review generated Markdown before publishing and prefer the HTML output path when link and text escaping matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/newsletter-kit)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code]

**Output Format:** [HTML, Markdown, or plain text newsletter content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores draft newsletter items locally in newsletter-items.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
