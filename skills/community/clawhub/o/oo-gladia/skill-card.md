## Description:

Gladia (app.gladia.io). Use this skill for ANY Gladia request — reading, creating, updating, and deleting data. Whenever a task involves Gladia, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Gladia pre-recorded transcription jobs through an OOMOL-connected account, including uploading media, starting transcriptions, and retrieving or deleting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run remote installers whose contents are unverified, without a clear approval step.

Mitigation: Review and install the oo CLI separately before enabling the skill, using a verified release where available.

Risk: Requested audio and transcription data pass through OOMOL and Gladia.

Mitigation: Confirm the media source and data-sharing expectations before uploading media or starting a transcription.

Risk: Automatic skill synchronization can update the installed skill.

Mitigation: Review upstream synchronization behavior and use OO_SKILLS_SYNC_DISABLED if automatic updates are not appropriate.

## Reference(s):

- [Gladia API authentication documentation](https://docs.gladia.io/api-reference/authentication)
- [Gladia](https://app.gladia.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the oo CLI; action payloads are JSON.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
