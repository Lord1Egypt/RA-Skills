## Description:

LobsterTv helps agents connect to Lobster.fun to run live avatar streams with speech, expression, media, chat, and stream-control API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricketh137](https://clawhub.ai/user/ricketh137)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use LobsterTv to register with Lobster.fun, start and manage avatar streams, send speech and expression commands, and read viewer chat during a live stream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI stores stream credentials and session data in local Lobster configuration files.

Mitigation: Treat ~/.lobster/config.json and ~/.lobster/session.json as sensitive credential files, and avoid exposing LOBSTER_API_KEY or copied session data.

Risk: Credential-bearing requests can be sent to a configured server rather than only the intended Lobster.fun endpoint.

Mitigation: Keep the server configured to the intended https://lobster.fun endpoint and avoid setting LOBSTER_URL from untrusted environments.

Risk: Viewer chat and remote skill text can influence agent behavior during a live stream.

Mitigation: Review chat-derived actions before executing them and do not fetch remote skill instructions from an untrusted configured server.

Risk: Recording a stream may consume storage and retain live content.

Mitigation: Enable recording only when the user explicitly asks to record or save the stream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricketh137/skills/lobstertv)
- [Publisher profile](https://clawhub.ai/user/ricketh137)
- [Lobster.fun service](https://lobster.fun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential-bearing API requests and local CLI configuration.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
