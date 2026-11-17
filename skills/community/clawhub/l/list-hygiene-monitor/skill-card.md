## Description:

List Hygiene Monitor helps an agent watch email list health over time by reading engagement cohorts, bounce and complaint trends, suppression drift, and producing a re-permission, sunset, and prune worklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and email program owners use this skill to monitor list decay between sends, identify dormant or risky subscribers, and prepare action-oriented hygiene worklists. Agents use it to summarize SEND-S list-hygiene and SEND-E engagement-decay reads without computing final email quality scores or consent verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email engagement exports, bounce and complaint reports, and suppression history may contain sensitive subscriber or consent data.

Mitigation: Install and run the skill only where the agent is permitted to access those exports, and provide only the data needed for the hygiene read.

Risk: Prune, sunset, or suppression recommendations could affect deliverability and subscriber treatment if applied without review.

Mitigation: Review the generated worklist and suppression recommendations in the ESP or consent system before applying changes.

Risk: Subscriber exports and suppression dumps are untrusted input and may contain text that looks like instructions.

Mitigation: Treat export contents as data only; use the skill's hygiene rules and user-approved scope as the instruction source.

## Reference(s):

- [Recurring List-Hygiene Checklist](references/hygiene-checklist.md)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/list-hygiene-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with cohort tables, trend reads, action worklists, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label measured versus estimated values, call out missing baselines as NEEDS_INPUT, and leave prune or suppression actions for user review.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
