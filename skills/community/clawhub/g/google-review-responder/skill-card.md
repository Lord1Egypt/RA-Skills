## Description:

Helps agencies and consultants monitor client Google Business Profile reviews, draft tailored replies, and route them for operator approval before posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

Agencies and consultants managing configured client locations use this skill to check for unanswered Google Business Profile reviews, prepare industry-aware replies, and seek operator approval before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived per-client Google OAuth credentials are accessible locally.

Mitigation: Store credentials in a protected secrets location with restricted access; never paste refresh tokens into chat or approval messages.

Risk: The reply command can publish public business responses without a built-in approval-state check.

Mitigation: Restrict who can run the reply command and require explicit operator approval and review of the exact reply before each post.

Risk: Public exposure of the web-based OAuth onboarding server could compromise client credentials.

Mitigation: Do not expose the onboarding server publicly unless client identifier handling, authentication, HTTPS, file permissions and overwrite protections are fixed.

Risk: Public replies for regulated clients may reveal sensitive information or imply compliance assurances.

Mitigation: Have operators review industry-specific drafts, omit patient information from medical replies, and verify compliance with their own policies.

## Reference(s):

- [Review Responder on ClawHub](https://clawhub.ai/chris/skills/google-review-responder)
- [Setup and client onboarding](artifact/SETUP.md)
- [Skill instructions and privacy scope](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Plain-text review summaries, draft replies and approval messages; operational commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies can be published publicly after operator approval; approval is not technically enforced by the reply command.]

## Skill Version(s):

2.1.1 (source: ClawHub release metadata; bundled documentation identifies 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
