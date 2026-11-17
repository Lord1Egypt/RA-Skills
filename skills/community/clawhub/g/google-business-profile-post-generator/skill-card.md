## Description:

Drafts Google Business Profile update, offer, and event posts for local businesses and builds tracked links for each post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Help US local business owners and multi-location marketing managers prepare Google Business Profile updates, offers, and event posts with tracked calls to action. The skill drafts post copy and a publishing plan but does not publish to the business profile.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Incorrect template columns or a placeholder destination may produce unusable tracked links; generated tracked-links.md may overwrite an existing file.

Mitigation: Verify the column mapping and destination, use a dedicated output folder, and check generated links before relying on them.

Risk: The separately downloaded optional Windows app is unsigned, and its checksum alone does not establish that it is safe.

Mitigation: The bundled workflow does not require the app. Evaluate it separately and do not run it unless you accept the risk.

## Reference(s):

- [Business Profile post rules](references/gbp-post-rules.md)
- [Post-plan template](templates/gbp-post-plan.csv)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/google-business-profile-post-generator)
- [Publisher profile](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown, URLs, Guidance]

**Output Format:** [Structured post plan containing post copy, offer or event fields, a tracked link, publishing notes, and a policy check.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post copy is intended to fit the 1,500-character field. Review the draft and tracked link before use; the business owner publishes the post.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
