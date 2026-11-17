## Description:

Translates text or file content with the `trans` command, supporting automatic Chinese-English detection and translation into multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcnull](https://clawhub.ai/user/abcnull)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to translate typed text, whole files, selected file ranges, or specific lines between Chinese and English by default and into other supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated text and selected file contents may be sent to Bing through translate-shell, which can disclose confidential data.

Mitigation: Do not use the skill for secrets, credentials, private source code, legal or medical records, or other confidential files unless that disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abcnull/skills/mac-trans)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and translated text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send translated text or selected file content to Bing through translate-shell; avoid confidential input unless that disclosure is acceptable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
