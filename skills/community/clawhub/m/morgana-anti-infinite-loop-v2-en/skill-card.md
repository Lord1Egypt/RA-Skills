## Description: <br>
Lightweight anti-infinite-loop guard for LLM agents that observes agent actions, detects repetitive or stalled behavior, and returns healing, pause, or abort directives for the host agent to apply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add loop detection and recovery behavior to LLM agents, coding agents, RAG systems, data pipelines, and multi-agent workflows. It helps identify repeated actions, low novelty, intent drift, fast retry patterns, and known loop fingerprints before the host agent wastes tokens or stalls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loop fingerprints and small samples of agent actions can be retained on local disk for cross-session detection. <br>
Mitigation: Avoid passing secrets or sensitive customer data in action strings, use a project-specific storage path when appropriate, and periodically review or delete ~/.anti_loop/loops.json. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/morgana-anti-infinite-loop-v2-en) <br>
- [PyPI project page](https://pypi.org/project/anti-loop/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, shell commands, configuration examples, and JSON-like directive objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces host-agent directives such as heal, pause, or abort; it does not directly execute the user's agent workflow.] <br>

## Skill Version(s): <br>
2.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
