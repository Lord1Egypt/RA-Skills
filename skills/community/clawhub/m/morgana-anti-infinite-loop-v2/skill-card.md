## Description: <br>
Lightweight anti-infinite-loop guard for LLM agents that detects repeated, cyclic, low-novelty, and pre-flight loop patterns, then returns healing, pause, or abort directives for agent runtimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add an anti-loop guard to LLM agent loops across Claude, OpenAI, Hermes, LangChain, AutoGen, or custom harnesses. It observes agent actions and intent, detects likely loops, and produces a directive to heal, pause, or abort the run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loop history is saved locally under ~/.anti_loop/loops.json by default and may include samples of agent actions. <br>
Mitigation: Use a controlled storage_path, apply restrictive file permissions, avoid storing sensitive prompts or customer data in observed action text, and delete the history file when retention is not needed. <br>
Risk: Healing directives can alter agent behavior during a task if they are applied without review or policy checks. <br>
Mitigation: Route directives through the host agent's existing safety, logging, and approval controls, especially before using pause or hard_kill modes in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kofna3369/morgana-anti-infinite-loop-v2) <br>
- [Publisher Profile](https://clawhub.ai/user/kofna3369) <br>
- [PyPI Package](https://pypi.org/project/anti-loop/) <br>
- [README-listed Repository](https://github.com/kofna336/anti-loop) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown documentation, Python API return dictionaries, and CLI JSON/status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core package uses Python stdlib by default; optional extras add numpy or torch for advanced paths.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence; artifact frontmatter and pyproject.toml list 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
