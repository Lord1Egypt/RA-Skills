## Description: <br>
Bundles six Kimi/OpenClaw-adapted engineering workflow skills for requirements alignment, codebase-aware planning, handoffs, test-driven development, bug diagnosis, and PRD creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolingrabbit](https://clawhub.ai/user/coolingrabbit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this bundle to add structured coding workflows to Kimi/OpenClaw agents: clarifying requirements, maintaining project context and ADRs, creating handoff notes, developing with tests, diagnosing bugs, and turning aligned discussions into PRDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle contains broad auto-triggered workflow instructions that may activate during normal coding conversations. <br>
Mitigation: Review and narrow trigger phrases before enabling the bundled skills. <br>
Risk: Some workflows can write project files such as CONTEXT.md, ADRs, handoff notes, PRD markdown, tests, or code changes. <br>
Mitigation: Require user confirmation before creating or modifying project documentation, tests, or code. <br>
Risk: The PRD workflow can publish content to an issue tracker through configured GitHub MCP, token, or CLI paths. <br>
Mitigation: Require confirmation before publishing issues and prefer local Markdown fallback until the issue-tracker configuration is reviewed. <br>
Risk: Installing the meta-skill requires copying bundled skills into an agent skills directory. <br>
Mitigation: Back up or inspect the existing .agents/skills directory before copying the bundled skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolingrabbit/skills/mattpocock-skills-kimi) <br>
- [Publisher profile](https://clawhub.ai/user/coolingrabbit) <br>
- [Adaptation notes](docs/ADAPTATION-NOTES.md) <br>
- [Original Matt Pocock skills](https://github.com/mattpocock/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, issue-tracker actions, and workspace file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write CONTEXT.md, ADRs, handoff notes, PRD markdown, tests, code changes, and issue tracker content when enabled by the host agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
