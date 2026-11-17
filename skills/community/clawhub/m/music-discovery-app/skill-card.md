## Description:

A free music discovery application that integrates multiple unauthenticated music APIs for music search, lyrics, internet radio, and concert information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this release to run a full-stack music discovery app that searches music, displays lyrics, plays internet radio, and looks up concert information through free third-party music APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs many dependencies from an under-disclosed third-party npm mirror.

Mitigation: Install only in a disposable or development environment, review dependency sources, regenerate the npm lockfile from a trusted registry, and update vulnerable pinned packages before deployment.

Risk: The local backend startup binds the development server to 0.0.0.0, which can expose it beyond the local machine.

Mitigation: Change local backend startup to bind to 127.0.0.1 unless LAN access is intentionally required and protected.

Risk: Music searches, lyrics requests, radio searches, and event lookups are shared with third-party music APIs.

Mitigation: Avoid sensitive search terms, disclose the external API use to users, and review the third-party API terms and privacy expectations before production use.

## Reference(s):

- [iTunes Search API Documentation](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/)
- [Lyrics.ovh API Documentation](https://lyricsovh.docs.apiary.io/)
- [MusicBrainz](https://musicbrainz.org/)
- [Radio Browser API](https://api.radio-browser.info/)
- [Bandsintown](https://www.bandsintown.com/)
- [Quickstart Guide](docs/QUICKSTART.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with source code files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a FastAPI backend, Next.js frontend, dependency manifests, startup script, and deployment notes; no API keys are required, but user search terms are sent to third-party music APIs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
