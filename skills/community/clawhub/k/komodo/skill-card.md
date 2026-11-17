## Description:

Manage Komodo infrastructure - servers, Docker deployments, stacks, builds, and procedures. Use when user asks about server status, container management, deployments, builds, or any Komodo-related infrastructure tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weird-aftertaste](https://clawhub.ai/user/weird-aftertaste)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to inspect Komodo-managed servers, deployments, stacks, builds, procedures, and repositories, and to run authenticated Komodo Core API actions when managing infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform production-impacting Komodo execute and write actions, including deploy, stop, restart, run-procedure, create-stack, and delete-stack.

Mitigation: Use least-privilege Komodo API credentials and review every execute or write command before running it.

Risk: Komodo API credentials may be sent to an untrusted or plaintext endpoint if KOMODO_ADDRESS is misconfigured.

Mitigation: Use only trusted HTTPS Komodo Core endpoints and avoid plaintext HTTP.

Risk: Stack creation may upload compose and environment file contents to Komodo.

Mitigation: Review compose and env files before create-stack and avoid uploading unintended secrets or configuration.

## Reference(s):

- [Komodo API documentation](https://komo.do/docs)
- [ClawHub skill page](https://clawhub.ai/weird-aftertaste/skills/komodo)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal/API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KOMODO_ADDRESS, KOMODO_API_KEY, and KOMODO_API_SECRET for authenticated Komodo Core API operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
