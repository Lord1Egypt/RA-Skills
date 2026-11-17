## Description:

Huashu Design helps agents produce high-fidelity HTML-based prototypes, interactive demos, slide decks, motion design, design variations, and expert design reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swang066](https://clawhub.ai/user/swang066)

### License/Terms of Use:

MIT

## Use Case:

Designers, product teams, and developers use this skill to guide an agent through visual design work such as clickable app prototypes, HTML slide decks, motion demos, infographics, brand-aligned explorations, and structured design critique.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional media and narration scripts may be unsafe when run on untrusted filenames, timeline JSON, or output paths.

Mitigation: Review script inputs before execution and avoid running narration or export workflows on untrusted paths until the reported injection issues are fixed.

Risk: Suggested agent memory asset indexes can expose sensitive personal or project data to future agent work.

Mitigation: Keep sensitive data out of personal asset indexes unless reuse is intentional and approved.

Risk: Animation exports may include Huashu-Design watermarking that is unsuitable for some deliverables.

Mitigation: Verify final exported media for unwanted watermarking before sharing or publishing.

Risk: TTS workflows rely on credentials and configurable endpoints.

Mitigation: Store TTS credentials outside the skill directory where possible and use only trusted TTS endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swang066/skills/huashu-design)
- [README](README.md)
- [Workflow](references/workflow.md)
- [Content Guidelines](references/content-guidelines.md)
- [Design Styles](references/design-styles.md)
- [Slide Decks](references/slide-decks.md)
- [Video Export](references/video-export.md)
- [Voiceover Pipeline](references/voiceover-pipeline.md)
- [Verification](references/verification.md)
- [Critique Guide](references/critique-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML/CSS/JavaScript code, shell commands, and generated design artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HTML, MP4, GIF, PPTX, PDF, PNG, or SVG outputs when the relevant export workflows are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
