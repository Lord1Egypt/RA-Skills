## Description: <br>
Transform articles, essays, transcripts, and other long-form writing into polished single-file HTML presentations with editorial pacing and strong visual storytelling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yueeli](https://clawhub.ai/user/yueeli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to convert long-form prose into a reviewed or automatically generated scrollable HTML presentation with staged analysis, slide planning, visual direction, build notes, and final single-file output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided source text and writes project files under a projects folder. <br>
Mitigation: Run it only on source material intended for deck generation and review the created project artifacts before sharing or reusing them. <br>
Risk: Generated HTML presentations may reference external CDN fonts or libraries. <br>
Mitigation: Review the final HTML before sharing and verify that core text and structure remain readable if external resources fail to load. <br>
Risk: Auto mode skips approval pauses for the slide plan and visual direction. <br>
Mitigation: Use review mode when editorial or design checkpoints should be approved before final HTML generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yueeli/prose-to-deck) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Design system](artifact/references/design-system.md) <br>
- [Headline system](artifact/references/headline-system.md) <br>
- [Materials](artifact/references/materials.md) <br>
- [QA checklist](artifact/references/qa-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown stage artifacts and a single self-contained HTML presentation file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a dedicated project folder with progress tracking, analysis, slide plan, visual direction, build notes, and index.html.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
