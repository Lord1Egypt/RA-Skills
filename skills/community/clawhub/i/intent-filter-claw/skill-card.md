## Description:

Identifies purchase intent in public comments, posts, and private messages, then scores and formats high-intent sales leads for follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and marketing teams use this skill to analyze user-provided social comments or message exports, rank likely purchase intent, and prepare lead tables or Feishu dispatch guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process social comments, private messages, or customer data for sales follow-up without strong consent safeguards.

Mitigation: Use only data you are authorized to process, and redact personal details that are not needed for follow-up.

Risk: Lead dispatch to Feishu or sales teams can expose sensitive or unnecessary personal information if recipients are wrong.

Mitigation: Confirm recipients and destination channels before dispatching leads.

Risk: Intent scoring can misclassify comments, sarcasm, complaints, or marketing posts as sales leads.

Mitigation: Review scored leads before outreach and apply the included semantic filters for negation, sarcasm, complaints, and marketing content.

## Reference(s):

- [Intent Keywords](references/intent-keywords.md)
- [Semantic Rules](references/semantic-rules.md)
- [User Value Model](references/user-value-model.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/intent-filter-claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, CSV-style lead fields, concise guidance, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lead scores, intent categories, suggested sales outreach text, and optional Feishu dispatch guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
