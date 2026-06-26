## Description: <br>
Monitors and fetches Hacker News stories through the official API, including top, new, best, Ask, Show, Jobs, user profiles, and keyword searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve public Hacker News stories, item details, user profiles, and keyword search results from the Hacker News API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public network requests to Hacker News when invoked. <br>
Mitigation: Install it only when public Hacker News API access is acceptable for the agent environment. <br>
Risk: Broad trigger phrases such as "latest" or "jobs" can activate the skill unexpectedly. <br>
Mitigation: Narrow trigger phrases in the agent setup so generic user requests do not unintentionally route to this skill. <br>
Risk: Dependency drift could change runtime behavior. <br>
Mitigation: Install from the included package-lock.json when possible. <br>


## Reference(s): <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/) <br>
- [HN Reader ClawHub Release](https://clawhub.ai/runawaydevil/hn-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style text with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Hacker News API data and formats story, user, item, and search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
