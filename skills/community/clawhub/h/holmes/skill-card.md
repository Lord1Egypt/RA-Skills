## Description:

Guides an agent through Holmes-style abductive and deductive reasoning with explicit evidence chains, active information gathering, and optional case logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangqi-7](https://clawhub.ai/user/jiangqi-7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent analyze ambiguous problems by enumerating hypotheses, tracing evidence chains, checking assumptions, and producing a structured conclusion or case report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist local case records and reuse lessons from prior cases.

Mitigation: Require explicit confirmation before case logging, and review case records before allowing them to influence future instructions.

Risk: The autoresearch workflow can lead an agent to edit skill files and commit repository changes.

Mitigation: Require confirmation before any SKILL.md edit, lesson update, or Git action, and review diffs before accepting changes.

Risk: The bundled workflow proposes broad Git staging during iterative updates.

Mitigation: Use an explicit allowlist of intended files instead of broad repository staging.

Risk: The skill encourages active web search when information is missing.

Mitigation: Require confirmation before web search and avoid sending sensitive user or workspace data to external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangqi-7/skills/holmes)
- [Autoresearch mechanism](references/autoresearch.md)
- [Case studies](references/case-studies.md)
- [Case closing report](references/case_closing_report.md)
- [Case logger](references/case_logger.md)
- [Reasoning checklist](references/checklist.md)
- [Decision rules](references/decision_rule.md)
- [Holmes learnings](references/holmes-learnings.md)
- [Holmes lessons](references/holmes-lessons.md)
- [Mental models](references/mental-models.md)
- [Conversation patterns](references/research/01-conversations/01-conversations.md)
- [Expression DNA](references/research/02-expression-dna/02-expression-dna.md)
- [Decision heuristics](references/research/03-decisions/03-decisions.md)
- [Thinking system](references/research/04-thinking-system/04-thinking-system.md)
- [Deductive method workflow](references/research/05-deductive-method/05-deductive-method.md)
- [Logic rules library](references/research/06-case-studies/06-case-studies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured reasoning sections and occasional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence labels, evidence chains, model or formula names, and boundary statements.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter is 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
