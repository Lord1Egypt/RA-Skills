## Description:

CastingWords (castingwords.com). Use this skill for ANY CastingWords request — reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can use the skill through an OOMOL-connected account to check a CastingWords prepay balance, retrieve transcripts, check transcription status, and submit media URLs for transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may silently install other agent skills.

Mitigation: Review and preinstall a verified CLI release, and set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations. Confirm the transcription URL, expected charges, and submission before approving a job.

## Reference(s):

- [CastingWords](https://castingwords.com)
- [CastingWords API documentation](https://castingwords.com/docs/developer/SimpleAPI.html)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, HTML, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands; action results may be JSON, plain text, or HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected action; transcript retrieval can return plain text or HTML.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
