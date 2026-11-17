## Description:

Uses a local GMNCODE image-analysis script as a fallback when the built-in image tool is unavailable and GMNCODE_API_KEY is configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[io2077](https://clawhub.ai/user/io2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect local images, screenshots, and character or style references when built-in media understanding is unavailable in an environment with GMNCODE_API_KEY configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells the agent to run an unbundled local script.

Mitigation: Inspect and trust the local script before use, and run it only in controlled workspaces.

Risk: Images and prompts may be sent to GMNCODE, and GMNCODE_API_KEY is exposed to the script process.

Mitigation: Avoid sensitive images or prompts unless external processing is approved, and protect or scope GMNCODE_API_KEY appropriately.

Risk: Image identity or source guesses can be uncertain.

Mitigation: Present uncertain results as estimates and do not describe visual style similarity as confirmed source attribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/io2077/skills/local-gmncode-vision)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text, often including a shell command invocation and image-analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output should state uncertainty when identification is unclear and avoid treating style similarity as confirmed provenance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
