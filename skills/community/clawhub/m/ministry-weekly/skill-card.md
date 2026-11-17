## Description:

Ministry Weekly helps church staff turn a Sunday briefing into a weekly content package with bulletin copy, scripture context, platform-specific social posts, email, image prompts, sermon-series recap, and optional confirmation-gated Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External church staff and ministry communicators use this skill to produce weekly Sunday communications from a concise sermon brief. It supports bulletin drafts, social posts, email announcements, image-generation prompts, sermon-series continuity, and optional Telegram delivery after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores church profile, sermon series history, and weekly planning history in a local ministry-data.json file.

Mitigation: Use it only where local ministry planning data is acceptable, and keep congregant PII, giving records, attendance lists, and identifiable prayer requests out of the workflow.

Risk: Optional Telegram delivery can publish the assembled package through the user's configured Telegram integration.

Mitigation: Configure Telegram only when desired, review the package first, and require explicit confirmation before each post.

Risk: Generated ministry copy, scripture context, and image prompts may need pastoral, theological, or brand review before publication.

Mitigation: Review all drafts before use, keep scripture context factual and tradition-neutral, and publish social or email content manually unless the confirmed Telegram path is intentionally used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chris/skills/ministry-weekly)
- [Publisher Profile](https://clawhub.ai/user/chris)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown-style structured content package with labeled sections and optional JSON-backed local state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces drafts for user review; optional Telegram posting is confirmation-gated and uses the user's configured integration.]

## Skill Version(s):

1.1.1 (source: frontmatter, README, changelog, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
