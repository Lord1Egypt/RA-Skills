## Description: <br>
Guides an agent to learn from user corrections, self-reflection, failures, and better approaches by maintaining local memory and correction files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make an agent capture explicit corrections, recurring preferences, and self-reflection lessons in local memory so future work can adapt to known user expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-derived long-term memory that can influence future agent responses. <br>
Mitigation: Install only when persistent local memory is desired, inspect ~/self-improving/ periodically, and use the documented forget/export flows when memory should change. <br>
Risk: Memory or workspace steering files could accidentally include sensitive data. <br>
Mitigation: Do not store credentials, financial data, medical data, third-party personal data, or sensitive access details; review proposed edits to AGENTS.md, SOUL.md, HEARTBEAT.md, and memory files before accepting them. <br>
Risk: Optional proactive behavior can increase the scope of future agent actions. <br>
Mitigation: Review the separate Proactivity skill before agreeing to install it and require confirmation for changes that affect workspace behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/muguozi1/muguozi1-openclaw-self-improving) <br>
- [Skill Homepage](https://clawic.com/skills/self-improving) <br>
- [Security Boundaries](artifact/boundaries.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Learning Mechanics](artifact/learning.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory and configuration guidance for agent behavior; no external service output is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
