## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and collects public creator posts for trend, competitor, KOL, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content, marketing, social media, and data analysis teams use this skill to search public Xiaohongshu content, inspect note details and comments, monitor public creator posts, and prepare structured source data for trend research, competitor analysis, KOL screening, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search terms, Xiaohongshu URLs, and the Guaikei API token to guaikei.com.

Mitigation: Install and run it only when third-party API use is acceptable; keep the token private, avoid sensitive targets, and rotate the token if it may have appeared in shared logs or workspaces.

Risk: Successful runs automatically write fetched result files under logs/.

Mitigation: Restrict access to the logs directory, clean it when results are no longer needed, and avoid sharing workspaces that contain sensitive analysis outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-notes-and-comments)
- [Guaikei API token service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; successful command runs return structured JSON and may save result files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands accept keyword or Xiaohongshu URL inputs plus optional filters such as type, sort, time, and limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
