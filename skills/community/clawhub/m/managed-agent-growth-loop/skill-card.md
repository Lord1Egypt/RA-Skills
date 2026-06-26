## Description: <br>
Guides agents through managed-customer retrospectives and follow-up loops, turning usage history into state handoffs, proactive watchlists, onboarding gaps, outcome feedback, and quality review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, consultants, and developers use this skill to review managed customer-agent work and convert lessons into handoff files, watchlists, onboarding actions, outcome follow-ups, and quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent tracking files, reminders, or cron-style follow-up recommendations can affect customer operations if created without clear scope. <br>
Mitigation: Name the client or project, define which history or notes may be used, and confirm before creating persistent tracking files, reminders, or scheduled follow-up recommendations. <br>
Risk: External, sensitive, or repeated communications may create unwanted customer-facing actions. <br>
Mitigation: Keep external or sensitive communications as drafts until user approval, and avoid repeated alerts unless the state changes or customer risk increases. <br>
Risk: Retrospective outputs and follow-up guidance may contain incorrect or misleading conclusions. <br>
Mitigation: Review generated guidance before execution and use the skill's quality gate for numbers, source grounding, request alignment, tone, risk, next actions, and owners. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional shell command examples and structured checklist templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent tracking files, reminders, cron-style checks, or approval-gated follow-up drafts.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
