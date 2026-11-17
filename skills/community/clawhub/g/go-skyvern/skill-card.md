## Description:

Unofficial Go client for the Skyvern API, generated with oapi-codegen from the published OpenAPI document. Package skyvern (github.com/psyb0t/go-skyvern) provides typed REST methods for tasks, agents, runs, browser sessions and profiles, credentials, scripts, schedules, tags, artifacts and audit exports. Use when Go code needs Skyvern browser automation or already imports go-skyvern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this client to call the Skyvern API from their applications, including starting and inspecting automation runs and working with agents, browser sessions, profiles, credentials, scripts, schedules, and artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed if they are hardcoded, committed, or logged.

Mitigation: Read SKYVERN_API_KEY from the environment and avoid logging authenticated requests.

Risk: Requests can contain browser instructions, URLs, credential references, and other sensitive data.

Mitigation: Send only the data needed for the requested task and use the intended Skyvern deployment.

Risk: Starting automation can interact with external websites and consume credits; changes can affect Skyvern resources.

Mitigation: Run, cancel, delete, or change only resources owned by the task and only when the user requested the action.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Project page](https://github.com/psyb0t/go-skyvern)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-skyvern)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.8.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
