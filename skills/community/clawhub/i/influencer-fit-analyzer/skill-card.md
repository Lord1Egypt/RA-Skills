## Description:

Build an influencer shortlist from a category, budget, and market, or from account links and handles you already have. This influencer analysis and creator matching workflow reads public creator profiles and recent posts on TikTok, Douyin, Xiaohongshu, Instagram, YouTube, and X, or works from bios, follower counts, and posts you paste, then writes an 8-12 person memo with followers, recent play, interaction, content pillars, and a talk-or-not call. Use it for influencer analysis, creator matching, influencer shortlist, and creator research when you need who to approach for a campaign or collab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, brand managers, and creator strategists can use this skill to identify creators for a campaign or collaboration. Provide a category, budget, and market, or existing creator handles, to receive an 8–12 person shortlist memo based on public profile information or user-supplied data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting grants Beatra account permissions beyond creator research, including generation and voice-management access.

Mitigation: Review the full authorization before connecting, and revoke access from the Beatra Console if it is no longer needed.

Risk: Creator lookups are optional paid operations; installation telemetry runs automatically, and selected files may be uploaded externally.

Mitigation: Use pasted creator information when paid lookups are unnecessary, confirm each lookup before it runs, and avoid uploading files unless needed and approved.

Risk: A damaged installation inventory can make uninstall affect other Beatra skills that share the connection.

Mitigation: Use the bundled uninstall decision flow, review its decision and remaining-skills information, and do not manually remove the shared connection.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/influencer-fit-analyzer)
- [Beatra skill documentation](https://beatra.ai/skills/influencer-fit-analyzer)
- [Creator lookup and paid confirmations](references/creator-lookup.md)
- [Shortlist methodology](references/shortlist.md)
- [Authorization and installation](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown shortlist memo]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 8–12 creators, with follower counts, recent play when looked up, interaction, content pillars, and a talk-or-not recommendation.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
