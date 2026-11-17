## Description:

Generate AI videos from text descriptions using Media.io OpenAPI with credit checks, task-result polling, and Vidu Q3 text-to-video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external integrators use this skill to call Media.io text-to-video APIs, submit text prompts for video generation, check available credits, and poll generation tasks for results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, task identifiers, and task data are sent to Media.io APIs.

Mitigation: Avoid placing sensitive information in prompts or generation parameters unless Media.io processing is approved for that data.

Risk: The skill uses a Media.io API key and may consume account credits when generation APIs are invoked.

Mitigation: Keep the API key private, provide it through the environment or explicit runtime configuration, and restrict use to trusted workflows.

Risk: HTTP redirect behavior could affect where authenticated requests are sent if the API service redirects traffic.

Mitigation: Harden the router to disable redirects or explicitly validate redirect targets before using the skill with valuable credits.

## Reference(s):

- [Media.io OpenAPI Documentation](https://platform.media.io/docs/)
- [ClawHub Skill Release Page](https://clawhub.ai/wondershare-boop/skills/mediaio-text-to-video-api)
- [ClawHub Publisher Profile](https://clawhub.ai/user/wondershare-boop)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and cURL examples; Media.io API calls return JSON response payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API_KEY environment variable or explicit api_key argument; generation calls return task_id values that should be polled with the Task Result API.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
