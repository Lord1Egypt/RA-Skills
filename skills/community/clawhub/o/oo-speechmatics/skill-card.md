## Description:

Use the OOMOL-connected Speechmatics service to inspect capabilities, retrieve transcription jobs and transcripts, list deployments, and submit transcription jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to submit media URLs for Speechmatics batch transcription and retrieve job status, transcripts, deployment details, and service capabilities through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup permits downloaded code execution, and the CLI may synchronize additional agent skills.

Mitigation: Review setup before enabling the skill, install a verified CLI release yourself, and decide whether to allow skill synchronization; the oo CLI command reference documents OO_SKILLS_SYNC_DISABLED=1.

Risk: Submitting a transcription creates a Speechmatics job.

Mitigation: Confirm the exact payload and effect with the user before running the submit_transcription write action.

## Reference(s):

- [Speechmatics API authentication and supported endpoints](https://docs.speechmatics.com/get-started/authentication#supported-endpoints)
- [Speechmatics](https://www.speechmatics.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON, plain text, or SRT transcript data, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript format depends on the requested output; action inputs are supplied as JSON.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
