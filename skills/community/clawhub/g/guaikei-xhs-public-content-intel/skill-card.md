## Description:

Searches Xiaohongshu public notes, note details, comments, and creator posts, returning structured JSON for content research, engagement analysis, trend monitoring, and keyword comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content creators, analysts, and operators use this skill to research public Xiaohongshu content, compare keyword performance, inspect note details and comments, and monitor creator posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, limits, and GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Use it only in private workspaces, avoid sensitive research targets, and rotate GUAIKEI_API_TOKEN if request data or logs may have been exposed.

Risk: The skill automatically saves full execution results locally.

Mitigation: Monitor and delete the generated logs directory when results are no longer needed.

Risk: Public-content API calls can return empty, unavailable, rate-limited, or error responses.

Mitigation: Check status and error_code before analysis, retry transient failures conservatively, and do not infer conclusions from empty or failed results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-public-content-intel)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON with status, request metadata, and results arrays]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save execution results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
