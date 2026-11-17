## Description:

AI analyzes Instagram reels/posts and generates 8 categories of high-performing comments designed to maximize visibility, drive replies, and build authentic connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wizelements](https://clawhub.ai/user/wizelements)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media managers, agencies, and growth teams use this skill to analyze Instagram reels or posts and generate categorized comment options for engagement campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials or campaign context could be exposed through the optional email-report workflow.

Mitigation: Store SMTP credentials in environment variables or a secret manager, use TLS-enabled SMTP with app-specific credentials where possible, and confirm report recipients before sending.

Risk: Generated Instagram comments may be inappropriate, inaccurate, or perceived as spam if posted without human review.

Mitigation: Review suggested comments for accuracy, tone, platform policy fit, and audience context before posting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wizelements/skills/ig-comment-strategist)
- [Publisher Profile](https://clawhub.ai/user/wizelements)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with optional shell command examples and JSON report references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include categorized comment suggestions, confidence scores, top-N filtering guidance, batch report guidance, and optional email-report handling.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
