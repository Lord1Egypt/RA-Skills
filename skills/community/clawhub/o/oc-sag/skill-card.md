## Description:

ElevenLabs text-to-speech with mac-style say UX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Sag to turn text into spoken audio with ElevenLabs, select voices, and generate local voice replies. It also provides command-line guidance for pronunciation, delivery, and voice selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation is sent to ElevenLabs and may contain private content.

Mitigation: Avoid sending sensitive text unless its external processing is acceptable.

Risk: The security scan was partial because a local path-like reference could not be resolved.

Mitigation: Review the unresolved reference before relying on the scan for that part of the skill.

## Reference(s):

- [Sag homepage](https://sag.sh)
- [Sag on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-sag)

## Skill Output:

**Output Type(s):** [Audio, Shell commands, Guidance]

**Output Format:** [Spoken audio or an audio file, with shell commands and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the sag command-line tool and an ElevenLabs API key; local playback or MP3 file output is supported.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
