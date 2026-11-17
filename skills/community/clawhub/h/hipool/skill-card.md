## Description:

HipoolMemorySystem provides a lightweight embedded C memory engine for AI agents with key-value storage, tag and time-based search, sharding, WAL recovery, and snapshot support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hualang-c](https://clawhub.ai/user/hualang-c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to build and operate a local embedded memory store for agents in resource-constrained environments. It supports compact key-value memory, tag and time retrieval, named shards, write-ahead-log recovery, and snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security evidence flags unsafe filesystem handling in the shipped C persistence code.

Mitigation: Review or patch filesystem handling before installation, run as an unprivileged user in a private workspace, and use a trusted data directory.

Risk: Shard names and benchmark or test cleanup behavior may be unsafe on shared hosts.

Mitigation: Restrict shard names to simple alphanumeric, underscore, or dash values, and avoid running benchmark or test scripts on shared hosts until shell cleanup is made safer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hualang-c/skills/hipool)
- [README](artifact/README.md)
- [English skill documentation](artifact/hipool-skill-en.md)
- [Skill definition](artifact/SKILL.md)
- [Benchmark results](artifact/benchmark_results.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with C build commands, CLI examples, configuration notes, and source-code-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local build and usage guidance for a C memory engine; no external service integration is required.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
