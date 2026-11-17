## Description:

Interact with Komodo Core API using this project. Use when the user wants to list, manage, deploy, or execute operations against Komodo resources (servers, stacks, deployments, builds, repos, procedures, variables, alerts, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[onekill0503](https://clawhub.ai/user/onekill0503)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to inspect, create, update, deploy, run, control, and fetch logs for Komodo-managed resources through the Komodo Core API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform powerful Komodo infrastructure operations, including deploy, run, update, and destroy actions.

Mitigation: Use a narrowly scoped Komodo API key and review proposed operational commands before execution.

Risk: The skill requires Komodo API credentials and may print resource configuration or log output.

Mitigation: Store credentials only in protected environment configuration, avoid passing secrets in JSON arguments, and restrict sharing of terminal output and logs.

Risk: The skill does not enforce HTTPS for the Komodo endpoint.

Mitigation: Set KOMODO_URL to an HTTPS endpoint that the operator controls.

## Reference(s):

- [Komodo project site](https://komo.do)
- [ClawHub skill page](https://clawhub.ai/onekill0503/skills/komodo-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print Komodo resource status, update results, and logs returned by the configured Komodo Core instance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
