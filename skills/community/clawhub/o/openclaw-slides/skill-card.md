## Description:

Create stunning, animation-rich HTML presentations from scratch or convert PowerPoint files (.ppt/.pptx) to beautiful web slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and presentation authors use this skill to generate new browser-based slide decks, convert PowerPoint files into web presentations, or enhance existing HTML presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read presentation and image files provided by the user.

Mitigation: Use it only with files intended for deck generation or conversion, and review generated HTML and assets before sharing.

Risk: Optional PowerPoint conversion and image processing rely on unpinned Python packages.

Mitigation: Approve optional pip installs only in environments where installing unpinned dependencies is acceptable.

Risk: Remote-font presets can affect viewer privacy or offline portability.

Mitigation: Bundle fonts locally or choose offline-safe font settings when privacy or offline viewing matters.

Risk: Inline editing stores deck content in browser localStorage.

Mitigation: Enable inline editing only when local browser persistence is acceptable for the presentation content.

## Reference(s):

- [Style Presets Reference](references/STYLE_PRESETS.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [MyClaw Skills](https://myclaw.ai/skills)

## Skill Output:

**Output Type(s):** [code, files, shell commands, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce self-contained HTML slide decks, preview HTML files, processed local assets, and optional in-browser editable presentation state.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
