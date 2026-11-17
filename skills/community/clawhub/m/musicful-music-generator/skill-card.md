## Description:

Generate AI music or lyrics from natural language, with intent detection for vocal songs, instrumental background music, lyrics-only requests, and task status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boner-bbb](https://clawhub.ai/user/boner-bbb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to request vocal songs, instrumental background music, lyrics-only output, and task status updates from a natural language command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A modified or misconfigured MUSICFUL_BASE_URL can send the Musicful API key and prompts to an arbitrary server.

Mitigation: Review the .env file before use, keep MUSICFUL_BASE_URL set to https://api.musicful.ai, and rotate the Musicful API key if the endpoint was unexpectedly changed.

Risk: Prompts or lyrics submitted to the Musicful service may contain sensitive, regulated, or proprietary material.

Mitigation: Do not submit secrets, private lyrics, regulated data, or proprietary material unless the user accepts Musicful's data handling terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boner-bbb/skills/musicful-music-generator)
- [Musicful API key setup](https://www.musicful.ai/api/authentication/interface-key/)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text and JSON status payloads with lyrics, task IDs, preview URLs, and final audio URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MUSICFUL_API_KEY; MUSICFUL_BASE_URL is optional and defaults to the official Musicful API host.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
