## Description: <br>
Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make an agent anticipate likely next steps, preserve momentum, recover active task context, and follow through within explicit boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps persistent local operating notes under ~/proactivity/, which may capture sensitive preferences or task context if used carelessly. <br>
Mitigation: Avoid storing secrets or sensitive personal data in proactivity files and review the local notes periodically. <br>
Risk: The skill may propose changes to AGENTS, TOOLS, SOUL, or HEARTBEAT files that affect future agent behavior. <br>
Mitigation: Review the exact proposed lines before approving any workspace integration changes. <br>
Risk: More proactive behavior can cross user expectations if boundaries are unclear. <br>
Mitigation: Define DO, SUGGEST, ASK, and NEVER boundaries before allowing recurring follow-through. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/proactivity) <br>
- [Skill homepage](https://clawic.com/skills/proactivity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local operating notes under ~/proactivity/ when used as documented.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
