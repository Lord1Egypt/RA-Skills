## Description:

Generates reviewable knowledge-base-driven article drafts and platform-specific publish packs for WeChat, Xiaohongshu, Zhihu, Juejin, CSDN, Toutiao, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams and developers use this skill to turn supplied knowledge sources, keywords, trend context, and outlines into reviewable Chinese publish packs for multiple content platforms. It supports manual publishing preparation and Wechatsync draft-sync guidance without claiming to publish automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated publish packs may be mistaken for completed platform publishing.

Mitigation: Treat outputs as drafts and publish notes only; require human review and separate confirmation before using any external publishing tool or platform account.

Risk: Trend searches or external sources could introduce unsupported claims.

Mitigation: Use supplied knowledge sources by default, label sources when live search is explicitly requested, and review factual claims before publication.

Risk: Local export, repository scripts, and Wechatsync execution are outside the default installed skill package.

Mitigation: Handle those workflows as companion or external-tool mode and confirm environment, login state, and manual handoff before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/veeicwgy/skills/ip-publisher)
- [Output Contract](artifact/references/output-contract.md)
- [Package Boundary](artifact/references/package-boundary.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown conversation response with structured article drafts, platform payloads, cover brief, publish notes, and review items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output; does not read or write local files, manage credentials, enter platform backends, or publish automatically.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
