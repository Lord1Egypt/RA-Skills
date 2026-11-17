## Description:

Chinese character conversion between Simplified and Traditional Chinese plus regional variants for Mainland China, Taiwan, Hong Kong, and Japanese Kanji, using OpenCC conversion modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-tw](https://clawhub.ai/user/kai-tw)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, writers, and localization teams use this skill to convert Chinese text between Simplified, Traditional, Taiwan, Hong Kong, and Japanese Kanji variants while preserving regional terminology expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regional terminology or phrase-level conversions may not match the intended audience or context.

Mitigation: Choose the documented conversion mode for the target region and review converted output, especially proper nouns, technical terms, and idioms.

Risk: Dependency changes in OpenCC could alter conversion behavior in managed or sensitive environments.

Mitigation: Use a locked or pinned OpenCC dependency and rerun conversion tests before deployment.

Risk: File conversion can overwrite or create output files when the CLI is used with an output path.

Mitigation: Run the CLI only on files intended for conversion and review output paths before execution.

## Reference(s):

- [OpenCC Conversion Modes - Complete Reference](references/opencc_guide.md)
- [OpenCC GitHub](https://github.com/BYVoid/OpenCC)
- [OpenCC Documentation](https://byvoid.github.io/OpenCC/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Plain text conversions, Markdown guidance, and inline Python or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can read UTF-8 text from arguments, stdin, or input files and can write converted UTF-8 text to stdout or an output file.]

## Skill Version(s):

1.0.0 (source: evidence release and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
