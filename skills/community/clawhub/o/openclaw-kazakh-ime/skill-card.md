## Description:

Adds a Kazakh input method for OpenClaw and web text fields, with English, Arabic-script Kazakh, Cyrillic-script Kazakh, shortcut switching, and a virtual keyboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayden76](https://clawhub.ai/user/ayden76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and use a browser-based Kazakh input helper for text fields. It is intended for typing Kazakh in Arabic or Cyrillic script with keyboard mapping, mode switching, and an optional virtual keyboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed browser script runs persistently in the OpenClaw control UI and modifies web text fields.

Mitigation: Review the script before installation and deploy it only on pages where this input-method behavior is intended.

Risk: The script intercepts Ctrl+Shift+K and changes text-field language, input mode, direction, font, and autocomplete attributes.

Mitigation: Check accessibility, shortcut, and locale-sensitive workflows after installation; adjust the language attribute behavior if required.

## Reference(s):

- [OpenClaw Kazakh IME README](references/README.md)
- [ClawHub skill page](https://clawhub.ai/ayden76/skills/openclaw-kazakh-ime)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with installation steps, usage guidance, and inline code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JavaScript and HTML snippets for installing or configuring the input method.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
