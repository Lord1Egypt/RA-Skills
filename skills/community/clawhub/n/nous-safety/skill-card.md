## Description:

Ontology-driven agent safety layer that evaluates runtime tool-call decisions with semantic analysis, Datalog rules, and knowledge graph evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dario-github](https://clawhub.ai/user/dario-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to add a runtime safety gate that can observe, review, or block potentially harmful tool calls. It is intended for agent workflows that need auditable decision traces and configurable safety rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs mutable remote GitHub code.

Mitigation: Review the installer before running it and prefer installation from a pinned commit or signed release in a virtual environment.

Risk: The installer can delete a caller-selected installation directory during update failure.

Mitigation: Avoid sudo or root installation and do not set NOUS_INSTALL_DIR to a directory containing unrelated data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dario-github/skills/nous-safety)
- [Nous GitHub Homepage](https://github.com/dario-github/nous)
- [Biomorphic Memory Companion Project](https://github.com/dario-github/biomorphic-memory)
- [Agent Self Evolution Companion Project](https://github.com/dario-github/agent-self-evolution)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with bash, Python, YAML, and Datalog snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation guidance, integration examples, configuration notes, and safety-mode guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
