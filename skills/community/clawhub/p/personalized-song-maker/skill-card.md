## Description:

Turn a person's story and occasion into original lyrics and a newly generated song. This personalized song maker and custom song generator workflow collects the recipient, relationship, occasion, memories, and must-include details, drafts the title, lyrics, section structure, genre, and mood for approval, then generates one finished original song, and reviews story accuracy, name pronunciation, hook, lyric rendering, and vocal result. Use it for custom birthday songs, wedding songs, anniversary songs, proposal songs, family tribute songs, and company or team anthems, with one approved lyric draft and one song generation per run and honest post-result review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to turn a real story, occasion, and required details into an approved lyric draft and an original song, such as a birthday, wedding, anniversary, tribute, or team song.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports broad shared credential permissions.

Mitigation: Authorize only the intended account, protect the shared Beatra credential files, and never copy the device token into prompts, logs, or command arguments.

Risk: The security assessment reports recurring installation-linked analytics.

Mitigation: Review the package's installation registration and telemetry disclosures before connecting the skill.

Risk: The security assessment reports uninstall behavior that could affect shared credentials if inventory data is malformed.

Mitigation: Check the installed-skill inventory and confirm other Beatra skills no longer need the shared credentials before uninstalling.

Risk: The workflow sends story details to a remote song-generation service, and personal or private details may be sensitive.

Mitigation: Collect only details needed for the song and omit private information the user does not want included or shared.

## Reference(s):

- [Beatra Personalized Song Maker](https://beatra.ai/skills/personalized-song-maker)
- [ClawHub Personalized Song Maker release](https://clawhub.ai/beatra-ai/skills/personalized-song-maker)
- [Story-to-song workflow](references/workflow.md)
- [Music editing and audio processing](references/music-editing-and-audio.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Audio files]

**Output Format:** [Markdown lyrics and production guidance, plus generated audio artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One approved lyric draft and one song generation per run; optional paid audio finishing and deliverables.]

## Skill Version(s):

0.2.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
