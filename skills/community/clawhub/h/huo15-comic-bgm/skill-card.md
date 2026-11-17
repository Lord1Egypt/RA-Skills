## Description:

Generates a single Suno v5 background music track from a script's overall mood, matching the requested duration and favoring Chinese traditional instrumentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate one duration-matched background music file for Chinese-style comic or animation projects from script mood data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-derived mood data and the SUNO_API_KEY are sent to api.sunoapi.org.

Mitigation: Use a dedicated API key and run the skill only with script data that is acceptable to transmit to that third-party service.

Risk: The skill downloads audio from a URL returned by the third-party API.

Mitigation: Validate generated download URLs and enforce timeout and file-size limits before accepting downloaded media.

Risk: The package bundles broader media helpers beyond the declared BGM behavior.

Mitigation: Review, disclose, or remove unused Ark image, video, and TTS helpers before deployment.

Risk: Generated files are written into the selected project output directory.

Mitigation: Run the skill in a constrained project directory with only the minimum required filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-bgm)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)
- [Suno API endpoint](https://api.sunoapi.org)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions]

**Output Format:** [MP3 audio file with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a script JSON input, requested duration, output path, and SUNO_API_KEY; falls back to local music assets when available.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
