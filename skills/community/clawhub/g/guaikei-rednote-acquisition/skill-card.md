## Description:

Search Xiaohongshu public notes, retrieve note details and comments, and inspect public creator posts for content research and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content creators, marketers, and analysts use this skill to collect structured public Xiaohongshu note, comment, and creator-post data for trend research, competitor monitoring, KOL screening, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, and GUAIKEI_API_TOKEN-authenticated requests to www.guaikei.com.

Mitigation: Install and run it only when that data sharing is acceptable, and keep GUAIKEI_API_TOKEN out of recorded terminals, transcripts, and shared environments.

Risk: Command results and request details may be written to local JSON log files.

Mitigation: Use protected workspaces for sensitive research and clean or restrict access to generated logs after use.

Risk: The security verdict is suspicious because token-bearing links and API tokens require user review before installation.

Mitigation: Review the security summary and guidance before deployment, and confirm the skill is limited to authorized public-data workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-acquisition)
- [Guaikei service website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include status, error_code, request metadata, skill runtime metadata, and results; successful runs may also write JSON logs locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
