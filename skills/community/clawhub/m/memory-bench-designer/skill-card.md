## Description:

Designs custom agent-memory benchmarks from a user's use case, generates scenario configurations, runs memory-bench across five memory strategies, and interprets the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI engineers use this skill to design, run, and interpret scenario-specific memory retrieval benchmarks before choosing an initial agent-memory strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to run a benchmark shell command using a generated scenario name.

Mitigation: Inspect the exact command before execution, use a simple alphanumeric scenario name, and run from a scratch directory.

Risk: The benchmark can create files and result directories, and existing output paths may be overwritten.

Mitigation: Use fresh output directories and avoid existing paths unless overwriting is intended.

Risk: Embedding-enabled runs may download a sentence-transformers model.

Mitigation: Enable embedding runs only in environments where that dependency, download, and runtime cost are acceptable.

## Reference(s):

- [Memory Bench Designer ClawHub page](https://clawhub.ai/tatsuko-tsukimi/skills/memory-bench-designer)
- [Memory Bench Designer runner](https://github.com/TatsuKo-Tsukimi/memory-bench-designer)
- [Adapter profiles](references/adapter-profiles.md)
- [Elicitation flow](references/elicitation-flow.md)
- [Taxonomy](references/taxonomy.md)
- [Use-case patterns](references/use-case-patterns.md)
- [Coding agent walkthrough](examples/coding-agent-walkthrough.md)
- [Game AI walkthrough](examples/game-ai-walkthrough.md)
- [NPC cognition walkthrough](examples/npc-cognition-walkthrough.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML configuration files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create scenario and weights YAML files plus benchmark result directories containing results.md and results.json.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
