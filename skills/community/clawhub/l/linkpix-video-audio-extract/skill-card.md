## Description:

Guides agents in extracting MP3 or WAV audio tracks from local videos or video links, using qhkit to resolve platform share links when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and editors use the skill to save a video's existing audio track as MP3 or WAV for editing or reuse. It does not isolate vocals from accompaniment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks for a qhkit API key, which could be exposed in chat or stored in local configuration.

Mitigation: Configure the token locally rather than pasting it into chat; revoke it if exposed or no longer needed.

Risk: Resolving platform share links sends those links to a third-party service.

Mitigation: Use local extraction for local files or direct video links; review privacy implications before submitting share links to qhkit.

Risk: Commercial reuse of extracted background music may infringe copyright.

Mitigation: Check rights and obtain permission before commercial use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-video-audio-extract)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix website](https://www.iqinghu.com)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown instructions and MP3 or WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the local audio file path; may also include a video script when useful.]

## Skill Version(s):

0.1.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
