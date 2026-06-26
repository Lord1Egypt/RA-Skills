## Description: <br>
Mupeng Evolve provides agent self-evolution, file-based memory, revenue tracking, communication gating, and identity calibration guidance with no external runtime dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to structure an autonomous agent's memory, behavior updates, communication policies, business task tracking, and calibration routines. It is intended as operational guidance for agents that can edit local files and maintain logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad authority to change agent behavior and working memory. <br>
Mitigation: Restrict writable paths and require human approval for changes to tools, skills, heartbeat files, identity files, and permanent memory. <br>
Risk: Business-facing automation may affect invoices, proposals, public posts, or third-party messages. <br>
Mitigation: Require human approval before sending external communications, publishing public posts, issuing invoices, or submitting proposals. <br>
Risk: Self-evolution and calibration changes can become hard to audit over time. <br>
Mitigation: Regularly review generated logs and scan proposed behavior changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupeng-evolve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API keys, databases, or package dependencies are declared; behavior depends on the installing agent applying the guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
