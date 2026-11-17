## Description:

Music composition assistant that accepts natural language input, guides a multi-turn conversation to define genre, mood, theme, tempo, and other musical elements, generates structured prompts for Suno or Udio, and saves output to a user-specified path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gentleyo](https://clawhub.ai/user/gentleyo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn a brief music idea into a structured Suno or Udio prompt, choose style variants, and receive guidance for manual or automated generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated generation can rely on unofficial Suno or Udio wrappers that use account session credentials.

Mitigation: Prefer the manual Suno or Udio web workflow unless the wrapper has been reviewed and isolated.

Risk: The automated path performs network downloads and writes generated track files to disk.

Mitigation: Run automation in a sandbox with restricted network access and a dedicated output directory where overwrites are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gentleyo/skills/music-generate)
- [Suno](https://suno.com)
- [Udio](https://www.udio.com)
- [suno-api community wrapper](https://github.com/gcui-art/suno-api)
- [udio-api community wrapper](https://github.com/udioapi/udio-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration guidance]

**Output Format:** [Markdown with prompt text, setup guidance, and inline Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create MP3 files in a user-specified output directory when an API workflow is configured.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
