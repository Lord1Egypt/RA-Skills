## Description:

Kazakh Convert helps agents convert Kazakh text between Cyrillic and Arabic scripts, including direct text conversion, file-based conversion, and user dictionary management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayden76](https://clawhub.ai/user/ayden76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Kazakh text between Cyrillic and Arabic scripts in chat workflows, local files, and repeatable command-line tasks. It also supports maintaining a local custom dictionary for preferred word-level corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied input, output, and dictionary paths access the local filesystem and output or dictionary operations can overwrite files.

Mitigation: Use explicit, task-scoped paths and avoid pointing --input, --output, or --dict at sensitive or unrelated files.

Risk: Script conversion quality depends on the bundled mapping rules and any user dictionary entries.

Mitigation: Review converted text before publication or downstream use, and add dictionary entries only for verified corrections.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayden76/skills/kazakh-convert)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text or Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read UTF-8 input text from arguments, stdin, or local files and may write converted text or user dictionary updates to local paths supplied by the user.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
