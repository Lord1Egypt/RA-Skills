## Description:

Unofficial Go client for the Runway API, generated with oapi-codegen from Runway's OpenAPI document. Package runway (github.com/psyb0t/go-runway) has typed methods on runway.ClientWithResponses for all 49 paths of https://api.dev.runwayml.com, among them text, image and video to video, text to image, upscaling, text to speech, sound effects, voice dubbing, voices, avatars, realtime sessions, recipes, workflows, documents, uploads, task polling and cancelling, and organization credit balance and usage. Requests authenticate with a Bearer API key plus the X-Runway-Version header set to 2024-11-06, both set in one request editor. Use when Go code needs to call Runway's generation API, poll a Runway task, or already imports go-runway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this client to call Runway generation and account APIs from Go applications, submit or inspect tasks, and work with related resources such as uploads, voices, and workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, and other inputs sent through the client leave the local machine for Runway's servers.

Mitigation: Send only content approved for processing by Runway.

Risk: Generation requests spend organization credits, and delete operations can remove tasks or named resources.

Mitigation: Start, cancel, or delete only when requested, and only for resources created or named by the task.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Project repository](https://github.com/psyb0t/go-runway)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-runway)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-runway)

## Skill Output:

**Output Type(s):** [Code, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides typed client usage guidance; callers handle task polling and API response status checks.]

## Skill Version(s):

0.8.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
