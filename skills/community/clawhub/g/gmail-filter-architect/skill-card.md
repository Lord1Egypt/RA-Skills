## Description:

Designs and checks personalized Gmail filters using a recent sender census, then prepares label, priority, and archive rules for import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kisssam6886](https://clawhub.ai/user/kisssam6886)

### License/Terms of Use:

MIT-0

## Use Case:

Gmail users and their assistants use this skill to organize incoming messages, surface urgent alerts and bills, label forwarded mail, and archive routine marketing or social messages after checking proposed rules against their own mailbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing recent messages requires access to private Gmail data.

Mitigation: Grant mailbox read access only when needed and keep personalized profiles private.

Risk: Incorrect archive rules may hide bills, security alerts, codes, or human replies.

Mitigation: Review every rule against recent mail and check the shared protection exclusions before importing archive filters.

Risk: Applying star or archive rules to existing conversations may alter old mail in bulk.

Mitigation: Do not apply the star/archive batch to existing conversations; retain the old filter backup and verify results after import.

## Reference(s):

- [ClawHub release: gmail-filter-architect](https://clawhub.ai/kisssam6886/skills/gmail-filter-architect)
- [Gmail filter research (Chinese)](references/research-2026-09.zh-CN.md)
- [Gmail search operators](https://support.google.com/mail/answer/7190?hl=en)
- [Create Gmail filters](https://support.google.com/mail/answer/6579?hl=en)

## Skill Output:

**Output Type(s):** [Configuration, Code, Guidance]

**Output Format:** [Gmail filter XML, JSON verification queries, optional gmailctl Jsonnet, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate label-only and star/archive batches; proposed rules require mailbox-specific review before import.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
