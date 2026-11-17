## Description:

Helps users manage a MyBooks library, reading activity, annotations, book transfers, and administrator-controlled audiobook conversion and voice settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poxenstudio](https://clawhub.ai/user/poxenstudio)

### License/Terms of Use:

MIT-0

## Use Case:

MyBooks users can ask an agent to find and organize books, track reading, import annotations, transfer ebooks, and manage audiobooks when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, book text, voice samples, or TTS keys may be processed by the configured MyBooks server or TTS provider.

Mitigation: Use a trusted server and HTTPS for non-local hosts, keep credentials session-scoped, and review TTS use before sharing sensitive content.

Risk: Uploading an unintended local ebook or voice sample could expose private material.

Mitigation: Upload only files explicitly selected by the user and confirm their destination.

Risk: Library edits, annotation imports, and deletions can change or remove user data.

Mitigation: Preview supported changes and obtain user confirmation before destructive actions.

## Reference(s):

- [MyBooks skill on ClawHub](https://clawhub.ai/poxenstudio/skills/mybooks)
- [MyBooks website](https://www.mybooks.top)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Natural-language responses based on MyBooks API results, with optional commands or configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a requested voice recording as a WAV file.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
