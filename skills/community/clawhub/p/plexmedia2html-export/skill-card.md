## Description:

Exports Plex Media Library movies and TV shows as static HTML pages with multilingual output, machine-bound token obfuscation, genre filtering, and detail popups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kesuek](https://clawhub.ai/user/kesuek)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to export Plex movie and TV libraries into static, browser-viewable HTML pages with local cover images and metadata navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Plex token using machine-bound obfuscation rather than strong encryption.

Mitigation: Use a least-privilege Plex token where possible, restrict config file access, and rotate the token if the config file may have been exposed.

Risk: Using the --insecure option disables certificate validation for Plex API requests.

Mitigation: Use HTTPS with valid certificates for normal operation and reserve --insecure for trusted self-signed environments where interception risk is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kesuek/skills/plexmedia2html-export)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Static HTML files, local image files, JSON configuration, and terminal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports paginated movie and series pages, cover images, detail modals, and localized English or German labels.]

## Skill Version(s):

1.3.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
