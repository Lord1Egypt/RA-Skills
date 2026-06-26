## Description: <br>
Designs custom agent-memory benchmarks for a user's use case by eliciting requirements, generating scenario configs, running memory-bench across five memory strategies, and interpreting results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design and run case-specific memory benchmarks that compare retrieval strategies before choosing an agent memory approach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create local scenario, weights, and result files in the current workspace. <br>
Mitigation: Run it from a workspace where generated files are acceptable and check for existing filenames before approving the run. <br>
Risk: The skill invokes a separate memory-bench CLI and may trigger a sentence-transformers model download. <br>
Mitigation: Use it only with a trusted memory-bench installation and review the generated YAML before approving the benchmark command and model download. <br>


## Reference(s): <br>
- [Taxonomy](references/taxonomy.md) <br>
- [Adapter Profiles](references/adapter-profiles.md) <br>
- [Use Case Patterns](references/use-case-patterns.md) <br>
- [Elicitation Flow](references/elicitation-flow.md) <br>
- [Game AI Walkthrough](examples/game-ai-walkthrough.md) <br>
- [NPC Cognition Walkthrough](examples/npc-cognition-walkthrough.md) <br>
- [Coding Agent Walkthrough](examples/coding-agent-walkthrough.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates scenario and weights YAML files, runs memory-bench, and summarizes results.md/results.json for the chosen use case.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
