## Description:

The nervous system for sovereign AI entities: cross-pillar checks, LLM trust profiles, coherence detection, and signal routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use NSE Orchestrator to set up an agent-wide orchestration layer for identity, payments, calendar, relationships, alignment checks, model trust scoring, and signal routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can shape agent behavior across identity, payments, calendar, relationships, alignment, model scoring, and persistent memory.

Mitigation: Install only when an agent-wide orchestration layer is intended, enable each pillar explicitly, and require confirmation before sensitive actions.

Risk: Optional dependency activation can expand the agent's capabilities in sensitive domains.

Mitigation: Review and pin the dependency set before installing extras or enabling pillar packages.

Risk: Persistent memory and profile-related workflows may record secrets or unverified claims.

Mitigation: Avoid storing secrets or unverified claims, and review memory or public profile writes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/nse-orchestrator)
- [Project homepage](https://github.com/HumanjavaEnterprises/nse-orchestrator.app.OC-python.src)
- [PyPI package](https://pypi.org/project/nse-orchestrator/)
- [NSE project site](https://nse.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require explicit user confirmation before wallet, identity, public profile, calendar, relationship, or persistent-memory actions.]

## Skill Version(s):

0.2.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
