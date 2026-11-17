## Description:

Hive-Commander provides a 1+5 distributed production swarm with session inheritance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawliet-ai](https://clawhub.ai/user/lawliet-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to split complex requests into five isolated worker tasks, dispatch those tasks through the configured model endpoint, and synthesize worker Markdown outputs into a conflict-audited response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inherits active model API credentials and writes them to a local OpenClaw temp configuration file for parallel worker calls.

Mitigation: Use explicit consent, scoped short-lived tokens, restrictive file permissions, per-run private temp directories, and cleanup of secret-bearing files.

Risk: Worker prompts are sent to the configured base_url with weak endpoint scoping.

Mitigation: Allowlist approved model endpoints and validate the base_url before each run.

Risk: Parallel worker outputs are written to a shared OpenClaw temp directory.

Mitigation: Review worker_*.md outputs before reuse and run multi-agent swarms in a Docker container or dedicated VM when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lawliet-ai/skills/hive-commander)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown synthesis with JSON worker configuration and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed five-worker fan-out; worker outputs are written under ~/.openclaw/swarm_tmp/.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
