## Description:

Retrieves recent public Xiaohongshu notes by keyword and supports note detail, comment, and creator post lookups for trend and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content creators, and analysts use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for topic monitoring, competitive research, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu research targets and URLs are sent to the Guaikei API.

Mitigation: Use a limited-scope API token, avoid submitting sensitive research targets, and confirm that the API use is acceptable for the workspace.

Risk: Full command results are saved locally by default.

Mitigation: Avoid shared workspaces for sensitive research and clear the generated logs directory when results should not be retained.

Risk: The security review notes that some data-collection capabilities may be under-described.

Mitigation: Review the skill's public-data scope before installation and use it only for public Xiaohongshu content that the user is authorized to analyze.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-hot-content)
- [Guaikei API service](https://www.guaikei.com)
- [Parameter and invocation guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON CLI output with status, request metadata, and results, plus local JSON logs when commands complete.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, Xiaohongshu note URL, creator profile URL, sort/type/time, and limit options.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
