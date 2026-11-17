## Description:

Helps users discover roles, assess job fit, prepare honest application materials, and rehearse interviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dong845](https://clawhub.ai/user/dong845)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use the skill to find and assess openings, create evidence-based CVs and application documents, and practise interviews. It supports market-specific materials while keeping claims grounded in the user's real experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad browser access as a review-needed concern.

Mitigation: Limit browsing to the requested job sources, keep discovery read-only, and let the user handle login or verification steps.

Risk: The security review flags recurring scheduling and inbox handling for review.

Mitigation: Set up a recurring digest only when requested, confirm its schedule and mailbox scope, and stop it when no longer needed.

Risk: The security review flags external data-sharing behavior as a review-needed concern.

Mitigation: Review destinations before sharing CV or profile details, and get the user's direction before submitting or sending information.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dong845/skills/job-hunt)
- [Project repository (listed in the plugin manifest)](https://github.com/addsumtech/job-hunt)
- [Discovery workflow](modes/discover.md)
- [Application workflow](modes/apply.md)
- [Weekly job digest guidance](references/weekly-digest.md)
- [Source policy](references/source-policy.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Word documents, PDF documents]

**Output Format:** [Text guidance and client reports; application documents in Markdown, Word, and PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-specific formats and conventions; applications are not submitted by the skill.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
