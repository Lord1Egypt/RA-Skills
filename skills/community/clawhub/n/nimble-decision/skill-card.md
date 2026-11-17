## Description:

Classifies, routes, and scores text with a local Ollama decision model, returning probabilities or scores rather than generated prose.

This skill is for research and development only.

## Publisher:

[avenlee-github](https://clawhub.ai/user/avenlee-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the skill to route requests, classify intent, apply probability-based gates, score urgency or sentiment, and batch-tag text. Its outputs can support low-cost triage, with uncertain decisions escalated for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logging defects may retain sensitive text and may not honor logging opt-outs during evaluations.

Mitigation: Avoid sensitive inputs until the logging defects are fixed. Keep inferences local; if logging is needed, use NIMBLE_NO_LOG=1 or an empty logFile, and do not rely on --no-log for evaluations.

Risk: A non-local configured endpoint sends input text to a remote host.

Mitigation: Keep the endpoint local or use only a remote server you trust.

Risk: The model weights are documented as CC BY-NC 4.0, which restricts commercial use.

Mitigation: Check the model's license terms before deployment and limit use to cases those terms allow.

## Reference(s):

- [Nimble Decision on ClawHub](https://clawhub.ai/avenlee-github/skills/nimble-decision)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON containing per-question classifications, probabilities, or weighted scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are decision signals; low-confidence or consequential decisions should be reviewed or escalated.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
