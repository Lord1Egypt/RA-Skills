## Description:

MyReels API helps agents inspect live MyReels model schemas, submit image, video, speech, or music generation tasks, list authenticated tasks, and poll task status through bundled shell scripts and API references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautyaiclub](https://clawhub.ai/user/beautyaiclub)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect an agent to the MyReels public API for model selection, generation task submission, task history review, status polling, and result URL delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helpers can execute the user's MyReels config file as shell code.

Mitigation: Review the scripts before installation and treat ~/.myreels/config as trusted code until the skill uses safer config parsing.

Risk: An access token may be sent to a configurable API endpoint.

Mitigation: Keep the token limited, use the official HTTPS MyReels API for normal use, and use a separate test token for non-production endpoints.

Risk: Prompts and task data are sent to an external generation service.

Mitigation: Avoid sensitive prompts and regulated data unless the deployment has approved MyReels for that data class.

## Reference(s):

- [MyReels Homepage](https://myreels.ai)
- [MyReels Developer](https://myreels.ai/developer)
- [Live Model Metadata Endpoint](https://api.myreels.ai/api/v1/models/api)
- [ClawHub Skill Page](https://clawhub.ai/beautyaiclub/skills/myreels-api)
- [Live Model Metadata](references/models.md)
- [Code Examples](references/code-examples.md)
- [Error Handling](references/errors.md)

## Skill Output:

**Output Type(s):** [shell commands, json, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can return model metadata, task submission acknowledgements, task lists, polling hints, and result URLs; authenticated operations require a MyReels access token and may require an active subscription.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
