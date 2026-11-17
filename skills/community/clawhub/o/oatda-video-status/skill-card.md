## Description:

Check the status of an asynchronous video generation task from OATDA, retrieve the video URL after completion, or poll a video task by task ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check OATDA video generation task status, handle pending or failed states, and return completed video URLs and costs when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an OATDA API key to query task status.

Mitigation: Install only when OATDA is trusted with the API key and task IDs, and avoid printing the full key in agent responses or logs.

Risk: The skill may read ~/.oatda/credentials.json when OATDA_API_KEY is not set.

Mitigation: Set OATDA_API_KEY directly when the credential file should not be read.

Risk: Returned video URLs and task IDs may expose generated media or account activity.

Mitigation: Share task IDs and returned URLs only with intended recipients, and download completed videos promptly when URLs may be temporary.

## Reference(s):

- [OATDA](https://oatda.com)
- [ClawHub skill page](https://clawhub.ai/devcsde/skills/oatda-video-status)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and summarized API response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include video status, video URL, direct video URL, provider, model, completion time, cost, and error guidance when returned by the OATDA API.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
