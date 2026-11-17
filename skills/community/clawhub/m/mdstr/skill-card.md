## Description:

This skill helps agents convert markdown files or text into JSON-safe strings for API calls, LLM prompts, and configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to convert markdown content into JSON-safe strings for REST API payloads, LLM prompt construction, JSON configuration, and CI/CD automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI globally or without a pinned version can increase supply-chain exposure.

Mitigation: Prefer a pinned mdstr version or a project-local dependency managed by a lockfile, and avoid sudo or global installs where practical.

Risk: Markdown converted for API examples may contain secrets or confidential content.

Mitigation: Review markdown inputs for credentials, tokens, and sensitive information before embedding them in API payloads.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON string examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI outputs one JSON-quoted string on stdout, strips trailing newlines by default, writes errors to stderr, and uses deterministic exit codes.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
