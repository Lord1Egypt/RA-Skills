## Description:

Local full-text search for OpenClaw memory recall using MeiliSearch. Self-hosted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enjuguna](https://clawhub.ai/user/enjuguna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to search local memory files, maintain tiered MeiliSearch indexes, and optionally distill recent daily notes into MEMORY.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer asks for broad system authority to install MeiliSearch and manage a system service.

Mitigation: Review the installer before running it and prefer a user-level service or verified package installation path.

Risk: The skill creates persistent background indexing jobs.

Mitigation: Require explicit opt-in for cron jobs and document how to inspect, disable, or remove scheduled tasks.

Risk: Private memory content can be sent to any configured MEILI_HOST.

Mitigation: Validate that MEILI_HOST is a trusted local endpoint before indexing or searching memory content.

Risk: Configuration loading executes the workspace .env file as shell input.

Mitigation: Use non-executing environment parsing and restrict file permissions on configuration containing MEILI_KEY.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enjuguna/skills/meili-memory)
- [Publisher profile](https://clawhub.ai/user/enjuguna)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON search results, Markdown memory updates, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update MeiliSearch indexes and append distilled facts to MEMORY.md when explicitly applied.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
