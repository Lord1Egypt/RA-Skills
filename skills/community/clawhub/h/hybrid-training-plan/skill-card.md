## Description:

Reads a user's Hybrid Training Plan sessions and records workouts, day status, and exercise maximums in their account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulkennethkent](https://clawhub.ai/user/paulkennethkent)

### License/Terms of Use:

MIT-0

## Use Case:

Hybrid Training Plan account holders use the skill to check scheduled workouts and log completed training, mark days complete or skipped, and review or set exercise maximums. It is not for general fitness advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key grants access to personal training data.

Mitigation: Keep HYBRID_API_KEY out of chat and files the agent reads.

Risk: An alternate API endpoint could receive the account key.

Mitigation: Leave HYBRID_API_URL at its default unless you trust the alternate endpoint.

Risk: Logging sessions or changing day status or exercise maximums updates the live account.

Mitigation: Review proposed logs, completions, skips, and maximum changes before allowing them.

## Reference(s):

- [Hybrid Training Plan skill release](https://clawhub.ai/paulkennethkent/skills/hybrid-training-plan)
- [Hybrid Training Plan API reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown summaries of sessions and account changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weights in kilograms for account updates; reports may use the user's preferred distance unit.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
