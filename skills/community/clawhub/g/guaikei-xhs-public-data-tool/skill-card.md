## Description:

Routes Xiaohongshu keywords, note links, creator profile links, and short links to commands that retrieve public search results, note details, creator posts, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, marketers, and content operators use this skill to collect structured public Xiaohongshu data for content research, competitor monitoring, KOL screening, trend discovery, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use a dedicated, revocable token and confirm that sending these inputs to the third-party API is acceptable for the intended workflow.

Risk: Command results are saved locally under logs/.

Mitigation: Review local logs before sharing workspaces, and avoid processing private or sensitive data through this public-data workflow.

Risk: The skill is intended for public Xiaohongshu data only.

Mitigation: Do not use it for private, hidden, login-only, or otherwise unauthorized data collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-public-data-tool)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may be saved under logs/ and include status, error_code, and result payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
