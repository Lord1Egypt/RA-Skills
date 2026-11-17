## Description:

Provides memory storage and search interfaces with lifecycle hooks that can download a CNB-hosted private enhancement package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xkzs2007](https://clawhub.ai/user/xkzs2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add memory storage, full-text search, and optional vector-search enhancements to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation hooks download an unverified private add-on from CNB.

Mitigation: Review before installing and use --no-hooks unless the publisher and CNB repository are explicitly trusted.

Risk: The downloaded private component may include native extensions and API access.

Mitigation: Treat the private component as separate executable code and prefer a release that pins and verifies the downloaded package.

Risk: Startup behavior checks the private package state over Git.

Mitigation: Allow network access only to the expected CNB endpoint and review lifecycle hook behavior before enabling hooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xkzs2007/skills/llm-memory-publish)
- [Publisher profile](https://clawhub.ai/user/xkzs2007)
- [CNB private package endpoint](https://cnb.cool)
- [CNB private package repository](https://cnb.cool/llm-memory-integrat/llm)
- [Architecture notes](artifact/docs/ARCHITECTURE.md)
- [Hooks documentation](artifact/hooks/README.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-like Python API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite memory files and a private package directory when lifecycle hooks are enabled.]

## Skill Version(s):

8.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
