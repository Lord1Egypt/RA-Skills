## Description:

Use OpenMarlin from OpenClaw to answer questions, run tasks, and manage OpenMarlin account setup and billing flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex4506](https://clawhub.ai/user/alex4506)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to register or connect an OpenMarlin account, submit execution or long-running task requests, and manage billing recovery from inside OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an OpenMarlin API key and can submit tasks, inspect billing data, create top-up sessions, and store local OpenClaw state.

Mitigation: Install only if those permissions are acceptable for the target environment and account.

Risk: A custom or insecure API origin could expose requests or credentials.

Mitigation: Keep OPENMARLIN_SERVER_URL on https://api.openmarlin.ai or another trusted HTTPS API origin, and avoid custom http endpoints except trusted loopback development.

Risk: Printed API keys and sensitive prompt text may be exposed.

Mitigation: Treat any printed API key as exposed and avoid sensitive prompt text until prompt retention and agent-id path validation are fixed.

## Reference(s):

- [OpenMarlin ClawHub skill page](https://clawhub.ai/alex4506/skills/openmarlin)
- [OpenMarlin API origin](https://api.openmarlin.ai)
- [OpenMarlin website](https://openmarlin.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit authenticated OpenMarlin execution, task, registration, and billing requests when activated.]

## Skill Version(s):

0.1.22-main.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
