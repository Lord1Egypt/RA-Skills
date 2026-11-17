## Description:

Generates FTdesign-compliant HTML preview pages for list, form, and detail interfaces from a user's page description.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[nero1510](https://clawhub.ai/user/nero1510)

### License/Terms of Use:


## Use Case:

Developers and designers use this skill to turn admin-interface requirements into FTdesign-style prototype HTML previews for list, form, and detail pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can write outside the intended workspace when output paths are not constrained.

Mitigation: Run it only on trusted configuration files, review output_filename before execution, and constrain generated files to a dedicated output directory.

Risk: Generated preview HTML can embed unsafe values from configuration input.

Mitigation: Avoid previewing HTML generated from untrusted input and HTML-escape rendered strings before using previews.

Risk: Unvalidated icon class names can affect generated markup.

Mitigation: Validate icon class names against the expected Remix Icon classes before generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nero1510/skills/guidelines)
- [FTdesign design system reference](references/design-system.md)
- [FTdesign components API reference](references/components-api.md)
- [FTdesign examples reference](references/examples.md)
- [Remix Icon stylesheet](https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css)
- [Google Fonts Inter stylesheet](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [HTML files, JSON configuration examples, Markdown guidance, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is intended for browser preview and prototyping.]

## Skill Version(s):

1.0.0 (source: server release metadata, README version history, and artifact version notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
