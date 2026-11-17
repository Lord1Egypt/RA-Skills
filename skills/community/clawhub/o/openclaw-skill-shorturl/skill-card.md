## Description:

Provides URL shortening with optional custom short-link domains and custom back halves through the shorturl.bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minecraftxdd](https://clawhub.ai/user/minecraftxdd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn long URLs into short links, choose an allowed short-link domain, and optionally request a custom suffix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs submitted for shortening are sent to shorturl.bot and may expose sensitive paths or query parameters.

Mitigation: Do not shorten URLs containing tokens, passwords, private internal paths, personal data, or sensitive query parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minecraftxdd/skills/openclaw-skill-shorturl)
- [shorturl.bot API endpoint](https://www.shorturl.bot/api/urls/shorturl)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text short URL, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints only the shortened URL by default.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
