## Description:

笔记手账 generates Chinese-first, notebook-journal style AI image prompts for educational knowledge cards, check-in posters, teaching illustrations, practice pages, and answer-explanation pages across nine visual themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, students, and content creators use this skill to turn a learning topic into structured Chinese AI image prompts for notebook-style educational cards, posters, exercises, and explanations. It is especially oriented to CSP-J/CSP-S/GESP teaching materials and age-appropriate visual study content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad visual-style trigger keywords may activate the skill for requests where the user did not intend notebook-journal educational prompt generation.

Mitigation: Confirm the intended page type, audience, topic, and visual theme before producing the final image prompt.

Risk: Generated educational prompt content may be inaccurate, misleading, or unsuitable when the learning topic is underspecified.

Mitigation: Review learning points, examples, exercises, and any included code before using the resulting prompt for instructional materials.

Risk: Downstream image generation can render Chinese text, formulas, layouts, or C++ code incorrectly even when the prompt is well structured.

Mitigation: Keep prompt text concise, request clear hierarchy and alignment, and manually verify rendered images before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/note-journal)
- [Skill workflow](artifact/SKILL.md)
- [Style system](artifact/styles.md)
- [Prompt templates](artifact/templates.md)
- [Reference guide](artifact/reference.md)
- [Prompt examples](artifact/examples.md)
- [OI code style](artifact/oi-code-style.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown prompt templates and structured prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output; may include C++ code snippets formatted for OI contest-style knowledge cards when requested.]

## Skill Version(s):

3.3.1 (source: server release metadata; artifact frontmatter and changelog show 3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
