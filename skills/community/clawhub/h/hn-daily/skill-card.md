## Description: <br>
Fetches and filters Hacker News top stories for tech news digests, HN updates, and automated Hacker News fetching with keyword filtering and caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Osgood001](https://clawhub.ai/user/Osgood001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical readers, and agents use this skill to fetch public Hacker News top stories, filter them by score and technology keywords, and return a concise digest as text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the public Hacker News API. <br>
Mitigation: Use it only in environments where outbound Hacker News requests are allowed, and configure approved proxy settings when required. <br>
Risk: The skill writes a local cache under the user's home directory. <br>
Mitigation: Review local cache policy before use, and use the documented cache bypass option when fresh results are required. <br>
Risk: The skill may use existing proxy environment variables. <br>
Mitigation: Check HTTP_PROXY, HTTPS_PROXY, and ALL_PROXY values before execution in sensitive environments. <br>


## Reference(s): <br>
- [Hacker News API Reference](references/hn_api.md) <br>
- [Official Hacker News API](https://github.com/HackerNews/API) <br>
- [ClawHub skill page](https://clawhub.ai/Osgood001/hn-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text digest or JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Hacker News data, supports CLI options for limit, minimum score, cache bypass, output format, and proxy environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
