## Description: <br>
Nous Safety provides an ontology-driven agent safety layer that evaluates tool actions with semantic analysis, Datalog reasoning, and knowledge graph evidence before returning ALLOW, BLOCK, or REVIEW decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dario-github](https://clawhub.ai/user/dario-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add a runtime safety decision layer to agents, starting in shadow mode for observation and moving to primary mode after tuning rules. It helps evaluate proposed tool calls with formal rules, semantic analysis, and knowledge graph context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can delete the configured install directory without confirmation if an update fails. <br>
Mitigation: Review the installer first, avoid setting NOUS_INSTALL_DIR to a broad or valuable directory, and back up any existing ~/.nous installation before updates. <br>
Risk: The installer clones and installs from a GitHub repository, so an unpinned install may change over time. <br>
Mitigation: Prefer installing from a pinned trusted commit in a virtual environment before using the skill in an agent workflow. <br>
Risk: Primary blocking mode can affect agent actions before the rules are tuned. <br>
Mitigation: Start in shadow mode, inspect local logs and any data sent to the configured LLM provider, then enable blocking only after reviewing the decisions. <br>


## Reference(s): <br>
- [Nous GitHub Repository](https://github.com/dario-github/nous) <br>
- [Nous Safety ClawHub Page](https://clawhub.ai/dario-github/nous-safety) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, Python, Prolog, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an installer, usage snippets, and mode configuration guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
