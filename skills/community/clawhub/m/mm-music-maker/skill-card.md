## Description:

Create music with MiniMax music models (e.g., music-2.5). Use when generating songs or instrumental tracks from lyrics and style prompts, or when integrating MiniMax Music Generation API into scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blue-coconut](https://clawhub.ai/user/blue-coconut)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to generate songs, instrumental tracks, or melodic chanting with MiniMax music models, and to integrate MiniMax Music Generation API calls into scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lyrics, prompts, style references, and API authentication requests are sent to MiniMax.

Mitigation: Use the skill only when sharing that content with MiniMax is acceptable under the applicable MiniMax terms, and avoid submitting confidential unreleased material unless those terms permit it.

Risk: The optional URL download path uses a returned URL that is not validated or size-limited by the skill.

Mitigation: Prefer the default hex output path when possible, and treat --output-format url --download as a higher-caution path.

## Reference(s):

- [MiniMax Music API Reference](references/minimax_music_api.md)
- [MiniMax Music Generation API Documentation](https://platform.minimaxi.com/docs/api-reference/music-generation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, Files]

**Output Format:** [Markdown guidance with bash commands and Python script usage; generated output is an audio file path or a temporary download URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MINIMAX_MUSIC_API_KEY for authentication; URL outputs expire after 24 hours.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
