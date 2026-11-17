## Description:

Build and run a high-signal information radar for C-end founders and operators across YouTube, X/Twitter, Reddit, WeChat Official Accounts, and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogerrrr18](https://clawhub.ai/user/rogerrrr18)

### License/Terms of Use:


## Use Case:

Founders and operators use this skill to turn RSS/OPML feeds and selected social watchlists into concise, action-oriented intelligence digests. It filters recent items by startup, AI, growth, and finance keywords, ranks them for relevance and actionability, and reports the top signals with transparent filtering counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted OPML or feed lists can cause the digest builder to fetch unsafe URLs, including local files or private-network services.

Mitigation: Use only trusted feed sources, reject file:// and internal/private-network URLs, and add URL validation or a domain allowlist before running the skill on third-party inputs.

## Reference(s):

- [Scoring & Ops Playbook](references/scoring-and-ops.md)
- [ClawHub Skill Page](https://clawhub.ai/rogerrrr18/skills/multisource-intel-radar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with source links, ranking labels, filter counts, and suggested next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest is intended to stay under 10 items and includes top 3 must-read signals, watchlist items, dropped-noise summary, filter transparency, and one next experiment.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
