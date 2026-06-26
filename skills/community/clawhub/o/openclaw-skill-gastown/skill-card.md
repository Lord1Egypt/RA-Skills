## Description: <br>
Multi-agent coding orchestrator using Gas Town and Claude Code to coordinate parallel coding work with persistent state, work tracking, monitoring, and merge workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saesak](https://clawhub.ai/user/saesak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate non-trivial coding tasks across multiple Claude Code workers, track progress through Gas Town and Beads, and coordinate review and merge activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad authority to change repositories, maintain persistent work state, and coordinate merge behavior. <br>
Mitigation: Use it only in repositories where automated workers and merge-queue activity are acceptable, and keep human review in place before changes are merged. <br>
Risk: Setup instructions install external command-line tools and may download or build dependencies. <br>
Mitigation: Review setup commands before running them, prefer pinned or verified tool versions, and avoid running privileged installation steps blindly. <br>


## Reference(s): <br>
- [Gas Town Architecture](references/architecture.md) <br>
- [Gas Town GitHub](https://github.com/steveyegge/gastown) <br>
- [Beads GitHub](https://github.com/steveyegge/beads) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/saesak/openclaw-skill-gastown) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for coordinating local multi-agent coding workflows; does not produce a standalone binary artifact.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
