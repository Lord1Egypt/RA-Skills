## Description:

Add a Historical Figures Advisory Board to AI agent personalities. 10 pre-configured personas inspired by public-domain historical figures for strategic advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcrowan3](https://clawhub.ai/user/jcrowan3)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to validate PersonaNexus YAML identities and compile board-enabled agent personalities into system prompts, OpenClaw JSON, SOUL/STYLE Markdown, Anthropic XML, and related formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI file-output path can overwrite unexpected files in shared or attacker-writable directories.

Mitigation: Run the skill in a least-privileged virtual environment and write generated files only to trusted, non-shared directories until the temporary-file write helper is fixed.

Risk: Compiled persona prompts can incorporate unreviewed YAML identity content.

Mitigation: Review each YAML identity and bundled template before compiling it into an agent prompt or personality file.

## Reference(s):

- [PersonaNexus Framework](https://github.com/PersonaNexus/personanexus)
- [ClawHub Skill Page](https://clawhub.ai/jcrowan3/skills/personanexus-bod)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell examples; CLI outputs include text, JSON, Markdown, OpenClaw personality JSON, SOUL.md, STYLE.md, and Anthropic XML-oriented prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only processing; CLI file outputs are optional and should be written to trusted directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
