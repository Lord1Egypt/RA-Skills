## Description:

Deep-read research papers into authoritative, reproducible teaching reports, then turn them into source-grounded multi-image cartoon-comic storyboard workflows with camera/style/logic continuity and final image-PDF assembly guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, educators, and technical readers use this skill to produce detailed paper deep-reading reports, source-grounded teaching explanations, staged comic storyboard prompts, and final storyboard PDF assembly guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundle-building helpers may package more workspace data than intended, including files reached through symlinks.

Mitigation: Run bundle builders only in a dedicated clean workspace, remove symlinks and unrelated files, keep output ZIP files outside the input tree, and inspect archives before uploading or sharing.

Risk: Workspace papers or unrelated documents may contain sensitive material that could be included in generated bundles or visual workflows.

Mitigation: Do not place credentials, private keys, or unrelated sensitive documents in the working directory used with this skill.

Risk: Image and storyboard stages can drift from the original paper if evidence strength is not tracked.

Mitigation: Keep report generation separate from image generation and require storyboard prompts to distinguish paper-explicit facts, report-derived points, reasonable inferences, nearby-work inferences, and missing details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/skills/paper-deepread-comic-studio)
- [Publisher Profile](https://clawhub.ai/user/c-narcissus)
- [README](README.md)
- [Security and Privacy Notes](SECURITY_PRIVACY.md)
- [Detailed Report Contract](schemas/detailed_report_contract.md)
- [Research Generative Overlay](schemas/research_generative_overlay.md)
- [Teaching Explanation Overlay](schemas/teaching_explanation_overlay.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured JSON templates, image-generation prompts, Python helper commands, and PDF assembly guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only deep-read reporting is separated from image-generation turns; storyboard sections are generated as multiple source-grounded 16:9 cards before final PDF assembly.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
