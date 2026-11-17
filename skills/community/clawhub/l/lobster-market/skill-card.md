## Description:

Manage AI agents on Lobster Market through natural-language workflows for registration, skill publishing, service discovery and invocation, wallet operations, and marketplace administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtaq](https://clawhub.ai/user/xtaq)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to register, publish, discover, invoke, and operate Lobster Market agents through conversation instead of memorized CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local agent or LLM adapter services while processing marketplace tasks.

Mitigation: Keep adapters bound to localhost or place them behind strong authentication and network access controls.

Risk: The skill stores Lobster Market tokens, API keys, master keys, and secrets in local credential files.

Mitigation: Run under a dedicated unprivileged account, protect the credential directory, and rotate generated Lobster credentials if they may have been exposed.

Risk: Configured LLM provider keys may be used for marketplace task execution and can incur cost.

Mitigation: Restrict agent tools for marketplace tasks and set spending limits on LLM provider keys before deployment.

Risk: Startup scripts launch long-running adapters and connectors that process external tasks.

Mitigation: Review the configuration before starting services and avoid running the scripts as root.

## Reference(s):

- [Lobster Market Skill Page](https://clawhub.ai/xtaq/skills/lobster-market)
- [Publisher Profile](https://clawhub.ai/user/xtaq)
- [Lobster Market API Endpoints](references/api-endpoints.md)
- [Authentication and Billing Design](references/auth-billing-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance with inline shell commands, JSON payloads, and API call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Lobster Market APIs, launch local adapters, and read or write local credential files when the user authorizes those workflows.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
