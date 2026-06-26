## Description: <br>
Structured decision support with self-improving local memory that helps users compare options, analyze risk and benefit, and retrospect on past decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xneosoul](https://clawhub.ai/user/0xneosoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to get framework-driven help with multi-option, high-stakes, or time-sensitive decisions while maintaining a local decision-memory profile and retrospective history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses persistent local decision memory, which may contain personal preferences, retrospective notes, or sensitive business context. <br>
Mitigation: Install only when persistent decision memory is desired, review ~/decision-making/ periodically, and avoid storing secrets, medical details, financial specifics, or confidential business information. <br>
Risk: Optional SOUL.md or HEARTBEAT.md snippets can enable proactive cross-session decision follow-up. <br>
Mitigation: Add those snippets only when proactive behavior is wanted, and remove or disable them when follow-up should remain manual. <br>
Risk: Decision guidance can be misleading when key assumptions, constraints, or user preferences are missing. <br>
Mitigation: Use the skill's confidence labels, explicit assumptions, and multi-option tradeoff framing before treating its analysis as decision support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xneosoul/neosoul-decision-agent) <br>
- [Skill homepage](https://clawic.com/skills/decision-making) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with local shell-command snippets and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains optional local state under ~/decision-making/ when installed and used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
