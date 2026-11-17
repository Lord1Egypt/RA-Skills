## Description:

Generates and edits HTML-format presentations through PPTUltra for general decks, summary reports, teaching courseware, public speaking, restyling, translation, text polishing, and fact checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyc529](https://clawhub.ai/user/yyc529)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create HTML-format PPT presentations or edit existing HTML PPT content for reports, courseware, speeches, translation, restyling, polishing, and fact checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPT prompts and supplied current-presentation content may be sent to PPTUltra cloud services.

Mitigation: Use the skill only with presentation content that is appropriate to share with PPTUltra, and avoid passing sensitive or unrelated files through --current-ppt.

Risk: Recent prompts, generated links, and optional API key configuration may be retained locally.

Mitigation: Prefer the PPT_API_KEY environment variable over --setup, and periodically delete .history.json and .config.json when local retention is not desired.

Risk: Editing flows can automatically reuse the most recent presentation history when --current-ppt is omitted.

Mitigation: Provide the intended --current-ppt explicitly for editing tasks and review the selected presentation context before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyc529/skills/pptgenerator)
- [PPTUltra](https://pptultra.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output with PPT summary text, share links, page URLs, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call PPTUltra cloud services and may store recent prompts, presentation links, and optional API key configuration locally.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
