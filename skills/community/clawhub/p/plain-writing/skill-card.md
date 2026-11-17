## Description:

Draft, rewrite, edit, or audit prose to reduce AI slop, verbosity, jargon, cliches, unsupported claims, robotic structure, and formatting excess while preserving meaning and voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshuagoode](https://clawhub.ai/user/joshuagoode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to draft, rewrite, edit, or audit technical, workplace, long-form, or creative prose for clearer language while preserving meaning, required facts, and voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linter or comparison output can include excerpts from drafts or source files, especially when broad globs are used.

Mitigation: Run helper scripts only on files intended for agent review, and inspect file paths or globs before execution.

Risk: A rewrite can accidentally alter protected facts, certainty, attribution, requirements, risks, or mitigations.

Mitigation: Use the skill's protected-content ledger, completion test, and final source sweep before returning edited prose.

Risk: The local lint and score tools provide review signals but do not certify factual accuracy, quality, or regulated writing conformance.

Mitigation: Treat tool findings as prompts for manual review, and require qualified human review for regulated or controlled-language work.

## Reference(s):

- [Plain Writing ClawHub page](https://clawhub.ai/joshuagoode/skills/plain-writing)
- [Server-resolved GitHub import](https://github.com/JoshuaGoode/plain-writing/tree/main/plain-writing)
- [AI-shaped writing patterns](references/ai-patterns.md)
- [Writing completion test](references/eval.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Finished prose or Markdown, with optional plain-text or JSON diagnostics from local helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports strict, technical, and natural language modes; technical mode is the default.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
