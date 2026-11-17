## Description:

Huo15 Ai Music Composer helps agents turn a user's voice sample, lyrics or theme, and style settings into generated songs with voice cloning, lyric generation, music arrangement, and audio mixing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

External users, creators, educators, content teams, and developers use this skill to generate custom songs from authorized voice recordings, lyrics or themes, and musical style parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive voice recordings, generated voice models, lyrics, and generated media.

Mitigation: Use only authorized voice samples and require explicit retention, deletion, and access-control procedures for uploaded recordings, derived models, lyrics, and generated outputs.

Risk: The server and deployment defaults may expose files, jobs, or stored media if used as-is.

Mitigation: Deploy first in an isolated test environment, bind Redis and MinIO to private interfaces, replace default secrets, and review the server code and deployment templates before any public or production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-ai-music-composer)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/QUICK_START.md)
- [Technical Specification](artifact/docs/technical-spec.md)
- [API Reference](artifact/docs/api-reference.md)
- [Extension Guide](artifact/docs/extension-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, shell, JSON, YAML, and HTTP examples for music generation workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can guide generation of WAV, MP3, MIDI, karaoke files, lyrics, job metadata, and quality reports when connected to the described services.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
