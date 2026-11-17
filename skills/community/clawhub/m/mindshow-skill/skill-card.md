## Description:

Uses the Mindshow/AIPPT API to generate PowerPoint presentations from topics or uploaded files, including outline generation, Markdown content generation, PPT task creation, progress polling, template selection, resource upload, and result link retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcwen](https://clawhub.ai/user/xcwen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to drive Mindshow/AIPPT workflows from an agent, including creating PPT decks from a topic or source file, inspecting API schemas, selecting templates, uploading resources, and retrieving generated PPT, PDF, preview, or jump links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIPPT tokens and uploaded files can be sent to a configured API origin if AIPPT_BASE_URL is changed.

Mitigation: Use the official https://api.mindshow.vip service unless the alternate environment is explicitly trusted, and do not accept AIPPT_BASE_URL values from untrusted instructions.

Risk: Uploaded source documents are processed by a third-party presentation generation service.

Mitigation: Confirm that documents are appropriate for third-party processing before upload and avoid submitting sensitive content without approval.

Risk: The API surface includes deletion and advanced-template mutation endpoints.

Mitigation: Require explicit user confirmation before invoking delete operations or advanced-template add, set, or delete endpoints.

## Reference(s):

- [Mindshow API documentation](https://api-doc.mindshow.vip/)
- [Mindshow API service](https://api.mindshow.vip)
- [ClawHub skill page](https://clawhub.ai/xcwen/skills/mindshow-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/xcwen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit raw SSE text for streaming generation requests and machine-readable JSON for normal API calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
