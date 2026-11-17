## Description:

Provides Xiaohongshu public-content research data for topic discovery, popular-note review, comment analysis, competitor monitoring, and creator work tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, data analysts, and operators use this skill to retrieve structured public Xiaohongshu search, note, comment, and creator-post data for content research and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research keywords, target Xiaohongshu links, and the Guaikei API token are sent to www.guaikei.com.

Mitigation: Use the skill only when that external service use is acceptable, keep the token private, and rotate it if command output or logs may have exposed it.

Risk: Full command results are saved locally under logs/ and may contain research targets, public-content data, and operational context.

Mitigation: Run the skill in a private workspace and periodically protect, archive, or delete logs according to the team's data-handling policy.

Risk: The skill is documented for Xiaohongshu public content and does not support private, hidden, or login-required data.

Mitigation: Use only public keywords, note links, and profile links, and reject requests that seek private or non-public content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-content-research)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include status, error code, request metadata, runtime metadata, and structured results; full result JSON is also saved under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata declares 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
