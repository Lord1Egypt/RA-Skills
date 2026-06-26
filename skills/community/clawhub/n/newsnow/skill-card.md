## Description: <br>
CLI tool to fetch trending news and hot topics from 66 sources across 44 platforms, returning structured news items with titles, URLs, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrycc](https://clawhub.ai/user/sorrycc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use newsnow to list available news sources and fetch current trending topics from social, technology, finance, and general news platforms. It is useful when a workflow needs readable headlines or JSON news records for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes an external newsnow npm CLI package. <br>
Mitigation: Before installing or invoking it, verify that the newsnow npm package is the intended package, preferably pinned to a known version. <br>
Risk: The Product Hunt source can require PRODUCTHUNT_API_TOKEN. <br>
Mitigation: Only set the token when Product Hunt results are needed, keep it out of logs and prompts, and use the least-privileged token available. <br>
Risk: Some news sources may be blocked, unavailable, or inaccessible from certain regions. <br>
Mitigation: Handle failed or empty source responses explicitly and select alternative sources when a platform is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sorrycc/newsnow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured JSON news records with id, title, url, pubDate, and extra metadata when invoked with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
