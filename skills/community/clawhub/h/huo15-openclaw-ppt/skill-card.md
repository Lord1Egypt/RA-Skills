## Description:

Generates and edits presentation decks from prompts, URLs, documents, mind maps, PDFs, and existing PPTX files using design-token style packs, semantic slide templates, auditing tools, and export utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presentation creators, and business users can use this skill to create, transform, critique, and export presentation decks from natural-language prompts and source materials. It is suited for local deck generation workflows that need PPTX, web, image, video, notes, and review outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User documents, extracted content, or URL content may be sent to the configured LLM provider.

Mitigation: Use only documents and URLs approved for the configured provider, and verify PPT_LLM_BASE_URL and ~/.openclaw/models.json before running.

Risk: URL import can process untrusted or internal URLs.

Mitigation: Avoid untrusted or internal URLs and restrict imports to approved public sources.

Risk: Some import or build paths may write unexpected files without clear enough user control.

Mitigation: Review output paths before execution and prefer the normal create-pptx.py path over create_pptx_combined.py until the hard-coded output behavior is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-ppt)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command examples; generated artifacts may include JSON deck specs, PPTX files, HTML pages, images, MP4 video, and Markdown review reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured LLM or image-provider credentials and local source documents.]

## Skill Version(s):

5.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
