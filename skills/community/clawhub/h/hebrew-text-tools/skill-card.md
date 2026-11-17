## Description:

Hebrew text processing utilities for transliteration, gematria calculation, nikud removal, letter identification, and Hebrew number formatting; pure Python, no dependencies, and works offline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeperl](https://clawhub.ai/user/abeperl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and end users use this skill to process Hebrew text offline, including transliteration, gematria calculation, nikud removal, Hebrew letter naming, RTL reversal, and Hebrew number formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad Hebrew-related prompts.

Mitigation: Confirm the user needs Hebrew text processing before applying transformations or recommending commands.

Risk: Transliteration is Ashkenazi-style and has a known Tav mapping accuracy issue.

Mitigation: Treat transliteration as a utility aid, not an authoritative linguistic result; verify sensitive names, liturgy, or educational material with a qualified source.

Risk: Hebrew number formatting is limited to 1-999 and RTL reversal is basic for mixed text.

Mitigation: Check ranges and mixed-direction output before using results in published or user-facing content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeperl/skills/hebrew-text-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and text or JSON utility output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline pure-Python CLI and Python API; optional JSON output is available from the script.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
