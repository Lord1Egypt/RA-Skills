## Description:

Generates IDR digital-human videos from templates, text, avatars, voices, or audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ihanxu2022](https://clawhub.ai/user/ihanxu2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list available digital humans, voices, and templates, then submit avatar-video generation jobs and retrieve the resulting video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and user content may be sent over plaintext HTTP.

Mitigation: Use only non-sensitive scripts and audio unless the publisher provides an HTTPS endpoint and clear data-handling terms; rotate IDR_USER_TOKEN if it was used over the HTTP endpoint.

Risk: TTS video generation may leave submitted text in local idr_text_*.txt files.

Mitigation: Delete leftover idr_text_*.txt files after generation and avoid submitting sensitive text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ihanxu2022/skills/idr-avatar-video)
- [Authentication](references/authentication.md)
- [Avatars](references/avatars.md)
- [Voices](references/voices.md)
- [Templates](references/templates.md)
- [Video Generation](references/video-generation.md)
- [Neural Avatar](https://www.neural-avatar.com)
- [IDR](https://idr.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-line output with resource listings, task status, and video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, network access to www.neural-avatar.com, and an IDR_USER_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
