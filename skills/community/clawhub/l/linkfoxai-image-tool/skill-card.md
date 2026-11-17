## Description:

linkfoxai-image-tool helps agents complete Linkfox/Ziniao image upload, scene fission, product replacement, and automatic image matting tasks, using local scripts when available and falling back to the Linkfox OpenAPI service when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziniao-open](https://clawhub.ai/user/ziniao-open)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route supported Linkfox/Ziniao image workflows through an agent, including image uploads, scene fission, product replacement, auto matting, and result-status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store the Ziniao/Open API key in a predictable local plaintext config file.

Mitigation: Use a limited-scope API key when possible, restrict local file access, and rotate the key if it may have been exposed.

Risk: Image data and prompts may be sent to the declared third-party API.

Mitigation: Avoid processing sensitive images or prompts unless the user accepts third-party transfer for this workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziniao-open/skills/linkfoxai-image-tool)
- [Linkfox OpenAPI router](https://sbappstoreapi.ziniao.com/openapi-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown or plain text containing API results, task identifiers, image result URLs, and status/error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require ZNOPEN_API_KEY and may send image data and prompts to the declared third-party API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
