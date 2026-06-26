## Description: <br>
Build and run a high-signal information radar for C-end founders and operators across YouTube, X/Twitter, Reddit, WeChat Official Accounts, and Xiaohongshu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rogerrrr18](https://clawhub.ai/user/Rogerrrr18) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External founders, operators, and agent users use this skill to collect OPML/RSS and watchlist sources, filter them by business-relevant keywords, and produce short action-oriented daily digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external feed, RSSHub, WeChat, and Xiaohongshu sources. <br>
Mitigation: Review OPML and feeds.txt entries before running and remove private, internal, or unfamiliar URLs. <br>
Risk: The artifact includes a personal default OPML path. <br>
Mitigation: Provide an explicit OPML path for each run instead of relying on the default path. <br>
Risk: Browser searches for WeChat or Xiaohongshu may expose account or browsing context. <br>
Mitigation: Use accountless or public browsing where practical when manually scanning those sources. <br>


## Reference(s): <br>
- [Scoring & Ops Playbook](references/scoring-and-ops.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with source links, scoring summaries, filter transparency, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest is capped to fewer than 10 selected items and includes top signals, watchlist items, dropped-noise summary, filter counts, and a next experiment.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
