## Description:

Unofficial Go client for the Label Studio API, generated with oapi-codegen. Package labelstudio (github.com/psyb0t/go-label-studio) provides labelstudio.NewClientWithResponses with a typed ...WithResponse method for every endpoint: projects, tasks, annotations, predictions, imports, exports, storage, ML backends, webhooks, users, organizations and workspaces. Auth is an Authorization: Token header added through a request editor, against a self-hosted or cloud server URL. Use when Go code needs to call the Label Studio API, or already imports go-label-studio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go integrations with a self-hosted or cloud Label Studio instance, including project, task, annotation, prediction, and administration workflows. It helps select generated client methods, configure authentication and server URLs, and handle responses safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reported one referenced path missing from the bundle, so some scan evidence is incomplete.

Mitigation: Check whether the missing context matters to your intended use before installing.

Risk: API credentials and annotation or task content are sent to the configured Label Studio server.

Mitigation: Use a verified server URL, use HTTPS for remote servers, and keep API tokens out of source code, commits, logs, and request-header output.

Risk: Create, update, and delete operations can change Label Studio data.

Mitigation: Run data-changing calls only when requested and only for resources within the user's scope.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-label-studio)
- [Project homepage](https://github.com/psyb0t/go-label-studio)

## Skill Output:

**Output Type(s):** [Go code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.11.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
