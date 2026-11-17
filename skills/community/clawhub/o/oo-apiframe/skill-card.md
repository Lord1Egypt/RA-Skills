## Description:

Apiframe (apiframe.ai). Use this skill for ANY Apiframe request — reading, creating, and updating data. Whenever a task involves Apiframe, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to work with Apiframe through an OOMOL-connected account: inspect models, submit image, music, and video generation jobs, and check job status or results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions execute a remote CLI installer that has not been independently verified.

Mitigation: Review and install a verified CLI release separately before enabling the skill. Check automatic skill synchronization settings and allow only the connected accounts you intend to use.

Risk: Generation requests can consume credits, and requests pass through OOMOL.

Mitigation: Review the requested generation and available credit terms before submitting jobs.

## Reference(s):

- [Apiframe](https://apiframe.ai/)
- [Apiframe API documentation](https://apiframe.ai/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-apiframe)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON job results and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation requests return job IDs; job results depend on the selected model and job status.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
