## Description:

Summarizes public NetEase Video short-video and topic pages, including video performance, account timelines, leaderboard distributions, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and content operations teams use this skill to summarize public NetEase Video pages, compare account timelines, and report topic or leaderboard performance without downloading content or bypassing platform controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public page analysis can drift into platform-rule violations if used for bulk scraping, downloading, interface reverse engineering, or bypassing controls.

Mitigation: Keep use lightweight and compliant: summarize manually accessed public pages, control request frequency, and avoid downloads, interface calls, reverse engineering, and batch collection.

Risk: Dynamic rendering and human verification may affect what the agent can reliably observe on NetEase Video pages.

Mitigation: Use manual page review when verification is required and clearly retain source links and collection time in summaries.

Risk: The skill is written in Chinese and targets a Chinese-language video platform, which can increase review burden for some users.

Mitigation: Install and use it only when reviewers are comfortable evaluating the Chinese-language instructions and resulting summaries.

## Reference(s):

- [NetEase Video homepage](https://v.163.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/netease)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries with structured data fields and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credential handling, persistence, downloads, interface reverse engineering, or bulk scraping behavior is described by the evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
