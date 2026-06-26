## Description: <br>
Auto-escalating multi-tier memory search that cascades from in-memory cache through SQLite, grep, and LanceDB vector search to find the best answer with minimal latency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msruruguay](https://clawhub.ai/user/msruruguay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to recall and persist project memory across local storage tiers, with automatic escalation and self-tuning shortcuts for repeated queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local memory search can expose unrelated or sensitive project content from knowledge directories, SQLite databases, grep results, or LanceDB stores. <br>
Mitigation: Install only in approved workspaces, review which local memory paths are accessible, and avoid using it on projects containing sensitive data unless retention rules are clear. <br>
Risk: The store and evolve workflows can persist content, recall statistics, and learned routing state without explicit cleanup controls. <br>
Mitigation: Avoid storing sensitive content, define retention and cleanup rules before use, and review generated knowledge, hooks, and cascade statistics files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msruruguay/midos-memory-cascade) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionary results or CLI text output; write operations may create Markdown, JSON, or JSONL files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches local memory tiers and may persist recall statistics, routing shortcuts, and stored content in project memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
