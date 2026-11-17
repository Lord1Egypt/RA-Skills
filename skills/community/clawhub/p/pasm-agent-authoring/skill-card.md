## Description:

The base kit for building agents on the PASM cognitive engine, including a BaseAgent SDK, agent framework, and skill-packaging library for offline, standard-library-only agent development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build PASM-based agents with memory, mood, action selection, feedback shaping, persistent state, scenario checks, and release-ready skill packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill introduces a third-party Python developer package into the user's environment.

Mitigation: Install and test it in a virtual environment before using it with private repositories or important agent state.

Risk: Generated or authored agents may save persistent state under ~/.pasm-agents.

Mitigation: Review what state is stored before using the agents with sensitive personas, conversations, or repositories.

Risk: The primary usage documentation is Chinese, which may cause implementation mistakes for readers who do not read Chinese fluently.

Mitigation: Have a qualified reader review setup and packaging steps, especially before release or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-agent-authoring)
- [Publisher profile](https://clawhub.ai/user/arronjack)
- [PASM skills homepage](https://github.com/arronJack/pasm-skills)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, TOML, shell command, and file-layout examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-authoring guidance and examples; created agents may persist JSON state under ~/.pasm-agents.]

## Skill Version(s):

0.5.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
