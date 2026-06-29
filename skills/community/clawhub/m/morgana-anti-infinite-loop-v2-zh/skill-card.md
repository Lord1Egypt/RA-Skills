## Description: <br>
A lightweight Chinese-language Python guard for LLM agents that detects and responds to repeated or looping behavior with predictive checks, healing directives, pause behavior, or abort signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to add loop detection and recovery behavior to LLM agents, including coding agents, RAG chatbots, batch workflows, and multi-agent systems. It helps identify repeated actions, low novelty, intent drift, rapid retry patterns, and known loop signatures before choosing a heal, pause, or abort response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-session loop memory can store samples of agent actions locally in ~/.anti_loop/loops.json. <br>
Mitigation: Avoid passing secrets or sensitive business content as action strings, and periodically inspect or delete the local loop memory file for private workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/morgana-anti-infinite-loop-v2-zh) <br>
- [PyPI project: anti-loop](https://pypi.org/project/anti-loop/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON-like directives, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime guard returns structured intervention results with fields such as intervene, loop_type, directive, and stats.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
