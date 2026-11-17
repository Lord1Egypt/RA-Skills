## Description:

Full access to ioBroker via the iobroker simple-api adapter. Read states, objects, historical data, write to states, execute scripts, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanwebgit](https://clawhub.ai/user/sanwebgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to let an agent inspect, query, and control an ioBroker installation through the simple-api adapter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad administrative control over ioBroker, including state and device mutation.

Mitigation: Use a least-privileged ioBroker account and require explicit human approval for state-changing commands.

Risk: Script execution commands can run JavaScript in ioBroker.

Mitigation: Treat exec and eval commands as dangerous operations and approve them only after reviewing the exact code to be executed.

Risk: The default configuration uses HTTP and may carry Basic Auth credentials without transport encryption.

Mitigation: Prefer HTTPS, avoid storing credentials for plain HTTP endpoints, and restrict network access to trusted hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanwebgit/skills/iobroker-simple-api)
- [ioBroker](https://www.iobroker.net/)
- [ioBroker simple-api adapter](https://github.com/ioBroker/ioBroker.simple-api)
- [ioBroker simple-api documentation](https://www.iobroker.net/#en/adapters/adapterref/iobroker.simple-api/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown command guidance with configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can trigger ioBroker API calls that read state, mutate devices and states, query history, and execute JavaScript when the agent invokes supported commands.]

## Skill Version(s):

1.3.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
