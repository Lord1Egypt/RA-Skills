## Description: <br>
INTJ Coach guides INTJ users through growth, career, and strategy conversations, switching between coaching questions and concrete advisory suggestions while recording goals, sessions, and action follow-ups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who identify with INTJ patterns use this skill for growth, career direction, entrepreneurship planning, decision clarity, and accountability. Agents use it to run either a coaching mode that asks focused questions or an advisory mode that gives concrete options, tradeoffs, first steps, and reference cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local coaching notes, session history, and action reminders that may contain personal goals, career details, or sensitive self-reflection. <br>
Mitigation: Tell users where records are stored, decide who can access them, define retention and deletion handling, and avoid deploying shared storage without an access-control review. <br>
Risk: The skill can perform proactive action follow-ups, which may surprise users if reminders are enabled without consent. <br>
Mitigation: Require explicit opt-in for proactive reminders and make it clear how users can pause or delete follow-up tracking. <br>
Risk: Users may raise serious mental-health concerns during coaching conversations. <br>
Mitigation: Keep the artifact-stated boundary that the skill is not a substitute for professional counseling and direct users toward qualified help for severe psychological issues. <br>


## Reference(s): <br>
- [INTJ Coach on ClawHub](https://clawhub.ai/lj22503/intj-coach) <br>
- [Publisher profile: lj22503](https://clawhub.ai/user/lj22503) <br>
- [INTJ insights](artifact/references/intj-insights.md) <br>
- [INTJ Coach question bank](artifact/references/question-bank.md) <br>
- [Advisor mode templates](artifact/references/advisor-templates.md) <br>
- [Coach mode example](artifact/examples/coach-mode.md) <br>
- [Advisor mode example](artifact/examples/advisor-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Conversational text and Markdown records, with optional inline shell commands for profile initialization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown coaching records under ~/.openclaw/workspace/memory/intj-users when used in an environment that permits file writes.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and README version history; SKILL.md frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
