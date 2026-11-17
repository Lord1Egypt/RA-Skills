## Description:

Fetches Xiaohongshu public notes, note details, comments, and creator posts through Guaikei CLI commands for trend tracking and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, operators, and analysts use this skill to search Xiaohongshu public content, inspect note engagement, retrieve comments, monitor creator posts, and support trend or competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, note URLs, profile URLs, and retrieval tasks are sent to guaikei.com.

Mitigation: Use only public-data tasks that the user is authorized to process and avoid submitting sensitive internal research terms or private URLs.

Risk: GUAIKEI_API_TOKEN is required for API access.

Mitigation: Keep the token in the environment, do not paste it into prompts or logs, and rotate it if exposure is suspected.

Risk: Command results and xsec_token-bearing URLs are saved automatically under a local logs directory.

Mitigation: Review, redact, or delete local logs after use according to the workspace data-retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-pick-hot)
- [Guaikei service website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful command output includes status, request metadata, skill metadata, and retrieved results; command runs also write JSON logs locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
