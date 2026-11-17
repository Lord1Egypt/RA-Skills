## Description:

Helps agents guide users through Sparki workflows that turn long videos into short clips for podcasts, interviews, livestreams, talks, and other long-form content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure and run Sparki video-editing commands that extract short, shareable clips from long-form video content. It is suited for podcast, interview, livestream, talk, and long-content repurposing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos and prompts are sent to Sparki for cloud processing.

Mitigation: Ask for clear user consent before upload and avoid sending sensitive media unless the user accepts Sparki processing.

Risk: A custom --base-url can redirect API-key and media workflows to an untrusted endpoint.

Mitigation: Use the default Sparki endpoint unless the alternate endpoint is fully trusted and expected.

Risk: Persisting an API key in local configuration can expose credentials on shared systems.

Mitigation: Prefer SPARKI_API_KEY for session-scoped use and protect or rotate saved keys when sharing machines.

Risk: Result downloads come from service-provided URLs.

Mitigation: Download only expected task results and validate filenames, paths, and destination directories before opening or redistributing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/long-to-short-zh)
- [Publisher profile](https://clawhub.ai/user/fischerlam)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local video path or Telegram Mini App upload, SPARKI_API_KEY authentication, and Sparki cloud processing.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
