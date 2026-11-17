## Description:

Classifies customer micro-moments into Buy Now, Research, Frustration, Advocacy, or Churn Risk with confidence scores, recommended next actions, and routing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support, success, marketing, and sales teams use this skill to classify incoming customer messages, identify intent buckets and confidence, and route follow-up actions in Slack, CRM, and workflow tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer messages may contain sensitive personal, business, or support data.

Mitigation: Redact PII and secrets before processing, confirm authorization for OpenAI and workflow-tool use, and apply organization-specific data handling controls.

Risk: Automatic routing to Slack, CRM, or customer-impacting workflows could create incorrect escalations or outreach from misclassified intent.

Mitigation: Keep CRM, Slack, and customer-facing actions in review mode until thresholds, playbooks, and approval paths are validated.

Risk: Intent classification can be wrong for ambiguous, short, non-English, sarcastic, or domain-specific messages.

Mitigation: Use confidence thresholds, manual review for low-confidence outputs, and feedback logs to tune prompts and routing rules.

Risk: The skill text claims broad GDPR/CCPA compliance without evidence of the user's actual processing controls.

Mitigation: Do not rely on the blanket compliance claim; review OpenAI data handling and implement local privacy, consent, retention, and audit controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/micro-moment-intent-classifier)
- [OpenAI API key setup](https://platform.openai.com/account/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance, Configuration]

**Output Format:** [Markdown guidance with example JSON, CSV, dashboard summaries, shell commands, and routing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include intent scores, primary and secondary intent, confidence, key signals, reasoning, urgency, and recommended next action.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
