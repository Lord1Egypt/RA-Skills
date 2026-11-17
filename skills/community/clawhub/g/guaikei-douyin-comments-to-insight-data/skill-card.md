## Description:

Provides command-line access to public Douyin search, creator post, video comment, and hot-list data for content research, competitor analysis, reputation insight, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content strategists, marketers, and developers use this skill to collect structured public Douyin data for topic selection, competitor monitoring, comment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin research requests and GUAIKEI_API_TOKEN are sent to guaikei.com, with the token treated as potentially exposed because this version sends it in request URLs.

Mitigation: Use a dedicated, least-privileged token, rotate it after testing or shared use, and avoid running the skill in environments where request URLs may be captured in logs or telemetry.

Risk: Scraped public comments and account metadata are automatically saved under the skill's logs directory.

Mitigation: Review and delete generated logs before sharing workspaces, committing files, or moving results outside the approved research context.

Risk: The skill may trigger broadly for short-video research workflows and can show runtime promotional contact information contrary to its own token-handling instructions.

Mitigation: Confirm the user intends to query Douyin before execution and review runtime errors for unexpected contact or promotional content before presenting them to end users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-comments-to-insight-data)
- [Skill README](readme.md)
- [Complete Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Request and Response JSON Schemas](assets/)
- [Guaikei Token and Support Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes JSON logs under the skill's logs directory and emits pure JSON to stdout with logs on stderr.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
