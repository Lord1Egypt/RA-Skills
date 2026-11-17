## Description:

Generate single-page HTML posters, flyers, promotional images, marketing materials, and visual designs in Chinese, English, or bilingual formats across multiple visual styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, marketers, and developers use this skill to generate ready-to-open HTML poster files for events, product launches, promotions, announcements, social posts, business materials, education, and holiday greetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local HTML can include browser JavaScript and third-party font or script loads.

Mitigation: Install and use the skill only if those browser-side dependencies are acceptable, and review generated HTML before opening when possible.

Risk: Poster content may be exposed through generated HTML, browser rendering, or exported image files.

Mitigation: Use non-sensitive poster content unless the output location, browser environment, and sharing path are appropriate.

Risk: Generated file output can overwrite existing files if saved with an unsafe name or location.

Mitigation: Choose a safe filename and destination before saving generated HTML or exported images.

## Reference(s):

- [Post Creator Skill Page](https://clawhub.ai/tobewin/skills/post-creator)
- [Poster Style Reference Guide](artifact/references/styles.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [html2canvas Browser Export Dependency](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js)

## Skill Output:

**Output Type(s):** [code, files, guidance]

**Output Format:** [Complete self-contained HTML with inline CSS and browser JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated posters may include Google Fonts and html2canvas CDN references for browser rendering and image export.]

## Skill Version(s):

1.6.3 (source: server release metadata, SKILL.md frontmatter, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
