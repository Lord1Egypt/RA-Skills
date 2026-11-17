## Description:

Collects structured JSON data from public Douyin search results, creator posts, video comments, and real-time hot lists for content research, competitor analysis, public-feedback review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Douyin public-data lookups for short-video topic research, competitor monitoring, comment analysis, and hot-list tracking. It maps natural-language Douyin research requests to Node.js CLI commands that return JSON and save local result logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin keywords, account or video URLs, and GUAIKEI_API_TOKEN are sent to the guaikei.com API.

Mitigation: Install and run only after confirming that this data transfer is acceptable for the user's task and environment.

Risk: The security summary says the skill can trigger too broadly for some short-video research requests.

Mitigation: Use the skill only for explicit Douyin public-data collection tasks and confirm ambiguous competitor, trend, or content-research requests before execution.

Risk: The security guidance flags token exposure in request URLs and automatic local result saving.

Mitigation: Review token handling before deployment, avoid sharing logs or command traces, and manage saved JSON results as potentially sensitive local files.

Risk: The security guidance notes runtime promotional or contact output and unclear download-address fields.

Mitigation: Review runtime messages and returned fields before exposing results in reports or automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-omni-public-data)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Skill README](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [guaikei token and help site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout is JSON and result logs are saved as JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; commands should run from the skill root.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
