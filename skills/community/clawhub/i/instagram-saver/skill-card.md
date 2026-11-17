## Description:

When a user provides an Instagram link, this skill helps an agent retrieve high-resolution images and videos from the post through the Cobalt API, including carousel posts and private-account status responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenleung1205](https://clawhub.ai/user/kenleung1205)

### License/Terms of Use:


## Use Case:

External users and agents can use this skill to process Instagram post URLs and request downloadable media links through Cobalt. It is intended for Instagram media retrieval workflows where the user supplies the source URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Instagram links may be sent to the third-party Cobalt service.

Mitigation: Require explicit user confirmation before sending a link and disclose that Cobalt will receive the URL.

Risk: The artifact instructs the agent to construct a shell command using a pasted URL.

Mitigation: Validate that the URL is an Instagram URL and use a structured HTTP client or argument-array invocation instead of interpolating user input into shell text.

## Reference(s):

- [Instagram Saver on ClawHub](https://clawhub.ai/kenleung1205/skills/instagram-saver)
- [Cobalt API endpoint](https://api.cobalt.tools/api/json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send user-provided Instagram links to Cobalt for media lookup.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
