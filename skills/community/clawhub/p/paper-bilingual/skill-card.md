## Description:

Paper Bilingual converts PDF papers from a URL or local file into bilingual Markdown, preserving extracted text, figures, and paragraph-by-paragraph Chinese translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caottt](https://clawhub.ai/user/caottt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to convert English PDF papers into Chinese-English Markdown for close reading, translation comparison, and figure-preserving study notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads arbitrary user-provided PDF URLs through a shell command without clear URL safety checks.

Mitigation: Only process trusted public PDF URLs, avoid private or internal URLs, and run the workflow in an isolated environment.

Risk: PDF text is sent to the session LLM for translation.

Mitigation: Do not use the skill for confidential papers unless sending their text to the session LLM is acceptable.

Risk: The security verdict is suspicious and recommends review before shared or sensitive use.

Mitigation: Review the skill before installing or using it on shared systems and pin dependencies such as PyMuPDF and Pillow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caottt/skills/paper-bilingual)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Bilingual Markdown files with extracted figure image assets and supporting code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a per-paper output folder containing index.md and extracted image or figure directories.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
