## Description: <br>
A universal self-improving agent that learns from ALL skill experiences. Uses multi-memory architecture (semantic + episodic + working) to continuously evolve the codebase. Auto-triggers on skill completion/error with hooks-based self-correction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to collect lessons from agent sessions, turn repeated experiences into reusable guidance, and propose updates to related skills. It supports manual self-improvement prompts and optional hook-based logging around tool use, command results, and session endings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad cross-skill memory collection may retain sensitive project context or user feedback. <br>
Mitigation: Avoid sensitive projects unless this behavior is explicitly desired, periodically inspect or delete stored memory, and limit retained details to reusable lessons. <br>
Risk: Self-improvement proposals may introduce incorrect or misleading guidance into existing skills. <br>
Mitigation: Require manual review for every skill-file or memory write, validate proposed guidance against current repo behavior, and keep traceable evolution or correction markers. <br>
Risk: Optional hooks can capture tool inputs, command outputs, and session events across workflows. <br>
Mitigation: Keep hooks disabled until reviewed, scope them to deliberate use cases, and verify captured data before enabling automated logging. <br>


## Reference(s): <br>
- [Appendix](references/appendix.md) <br>
- [SimpleMem: Efficient Lifelong Memory for LLM Agents](https://arxiv.org/html/2601.02553v1) <br>
- [A Survey on the Memory Mechanism of Large Language Model Agents](https://dl.acm.org/doi/10.1145/3748302) <br>
- [Lifelong Learning of LLM based Agents](https://arxiv.org/html/2501.07278v1) <br>
- [Evo-Memory: DeepMind's Benchmark](https://shothota.medium.com/evo-memory-deepminds-new-benchmark) <br>
- [Let's Build a Self-Improving AI Agent](https://medium.com/@nomannayeem/lets-build-a-self-improving-ai-agent-that-learns-from-your-feedback-722d2ce9c2d9) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON memory records, shell hook commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to skill files and memory records; review proposed writes before applying them.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
