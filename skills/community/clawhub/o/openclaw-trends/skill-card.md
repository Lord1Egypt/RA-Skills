## Description: <br>
Fetch and aggregate OpenClaw-related content from across the internet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndreMashukov](https://clawhub.ai/user/AndreMashukov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and OpenClaw users use this skill to find recent OpenClaw news, tutorials, videos, repositories, and community discussions across public web sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external search and content services, which can expose public search terms and depend on third-party availability. <br>
Mitigation: Run it only for public OpenClaw queries and expect results to vary with external service behavior. <br>
Risk: The artifact includes a hardcoded default YouTube API key. <br>
Mitigation: Set your own YOUTUBE_API_KEY for regular use and rotate or disable any shared key before operational deployment. <br>
Risk: The optional cron example performs unattended daily background checks. <br>
Mitigation: Add the cron entry only when scheduled background searches are intended and review local notification or logging behavior. <br>


## Reference(s): <br>
- [OpenClaw Trends on ClawHub](https://clawhub.ai/AndreMashukov/openclaw-trends) <br>
- [Publisher profile](https://clawhub.ai/user/AndreMashukov) <br>
- [YouTube Data API search endpoint](https://www.googleapis.com/youtube/v3/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON summaries with source, title, description, URL, date, and optional source-specific metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI options include days, output format, notifications, and web-search skipping.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
