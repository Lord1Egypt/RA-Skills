## Description:

Manage and explore a personal book library, including metadata, reading activity, external book discovery, and optional text-to-speech features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poxenstudio](https://clawhub.ai/user/poxenstudio)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a MyBooks library can search and update books, track reading, curate lists, and retrieve public book metadata. Administrators can also use the optional TTS tools to create audiobook audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports potentially destructive EPUB repair and overwrite risks.

Mitigation: Review the target book and preserve a backup before repair or replacement actions.

Risk: The security review reports possible local file access beyond the declared permissions.

Mitigation: Provide only the explicit file paths intended for an upload and check the configured destination.

Risk: The security review reports unclear disclosure of some actions and data flows, with incomplete analysis coverage.

Mitigation: Review the skill's actions and network destinations before enabling it; treat the available security analysis as partial.

## Reference(s):

- [MyBooks homepage](https://www.mybooks.top)
- [Book345 public metadata API](https://www.book345.com/api)
- [MyBooks 1.0.8 release page](https://clawhub.ai/poxenstudio/skills/mybooks)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Audio files]

**Output Format:** [Structured JSON results and natural-language guidance; optional WAV audio output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some operations update library data; optional upload and TTS features use user-selected files or save a new WAV file.]

## Skill Version(s):

1.0.8 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
