## Description:

Operate Klangio through an OOMOL-connected account to transcribe audio, recognize chords and beats, separate audio sources, and retrieve job results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected Klangio account can submit audio for transcription, chord or beat recognition, strum recognition, and source separation, then check job status and retrieve generated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs unverified remote code and can introduce broader changes to agent skills.

Mitigation: Install a verified oo release yourself, then review automatic skill installation and synchronization settings before connecting your account.

Risk: Generated files and audio are stored in OOMOL transit storage.

Mitigation: Confirm that this storage location is acceptable before using download actions.

## Reference(s):

- [Klangio](https://klang.io)
- [Klangio API job workflow documentation](https://api-docs.klang.io/docs/getting-started/basic-job-workflow)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands]

**Output Format:** [Markdown guidance, oo CLI commands, JSON job responses, and generated result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Jobs may complete asynchronously; generated files are downloaded to OOMOL transit storage.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
