## Description:

CyberPPT (Multi-Platform) transforms DOCX, PDF, TXT, and XLSX source materials into evidence-based, editable, consulting-style PowerPoint presentations with staged quality gates and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and agent users use this skill to convert source documents into high-density consulting-style presentation decks. The workflow emphasizes traceable evidence analysis, storyline planning, visual blueprinting, editable PPTX reconstruction, and render-based QA before final delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that install and update instructions trust mutable, unverified downloads and active agent skill directories.

Mitigation: Enable the package only after review; prefer an immutable release or reviewed commit, verify hashes or signatures, and avoid installing directly from main or using git pull as an automatic update path.

Risk: The release evidence flags dependency installation and a plaintext HTTP Poppler download path as security concerns.

Mitigation: Install dependencies in an isolated virtual environment and use trusted package-manager or HTTPS sources for external system dependencies.

Risk: The artifact workflow can generate presentation content from user-provided source material, so poor source evidence or skipped QA can produce misleading decks.

Mitigation: Require the documented evidence chain, user confirmation gates, editable-layer checks, render comparisons, and visual QA before treating generated decks as deliverables.

## Reference(s):

- [CyberPPT ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-cyberppt-mod)
- [Platform Compatibility Guide](PLATFORM_COMPATIBILITY.en.md)
- [Platform Feature Comparison](PLATFORM_FEATURES.md)
- [Source Analysis Reference](references/source-analysis.md)
- [Storyline Reference](references/storyline.md)
- [Visual System Reference](references/visual-system.md)
- [PPT Production Reference](references/ppt-production.md)
- [Quality Assurance Reference](references/quality-assurance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown planning outputs, JSON QA and manifest artifacts, shell commands, configuration files, PPTX files, and rendered preview images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final delivery is expected to include editable PPTX content, preview renders, visual comparisons, and QA evidence when the full workflow is followed.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
