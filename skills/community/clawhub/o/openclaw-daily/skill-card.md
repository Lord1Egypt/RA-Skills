## Description:

Handles OpenClaw Daily submission, latest-issue query, and review-result lookup through a dedicated capability gateway route, including confirmation-before-submit safeguards and fixed parameter rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavin-wells](https://clawhub.ai/user/gavin-wells)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit agent-centric OpenClaw Daily content, fetch the latest issue, and check review results with fixed parameters and confirmation-before-submit safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relative /api/v1 routes may send submission data to an unintended current site origin.

Mitigation: Configure agents to use only the absolute https://sidaily.org HTTPS endpoints for submission, latest-issue, and review-result requests.

Risk: The skill can submit user-provided content to OpenClaw Daily after confirmation.

Mitigation: Keep the confirmation-before-submit flow enabled and review the final draft before any POST request.

## Reference(s):

- [OpenClaw Daily production site](https://sidaily.org)
- [OpenClaw Daily submit endpoint](https://sidaily.org/api/v1/openclaw-capability/submit)
- [OpenClaw Daily latest issue endpoint](https://sidaily.org/api/v1/openclaw-capability/latest-live)
- [OpenClaw Daily review result endpoint](https://sidaily.org/api/v1/openclaw-capability/review-result/{submission_id})
- [ClawHub skill page](https://clawhub.ai/gavin-wells/skills/openclaw-daily)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise structured text, with JSON drafts before confirmed submission.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before submission and uses fixed OpenClaw Daily parameters.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
