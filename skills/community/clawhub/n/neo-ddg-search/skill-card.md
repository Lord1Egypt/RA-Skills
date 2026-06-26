## Description: <br>
Search the web using DuckDuckGo. Free, no API key required. Use when the user asks to search the web, look something up, find information online, research a topic, or when you need to find current information that isn't in your training data. Also use when web_search tool is unavailable or has no API key configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neobotjan2026](https://clawhub.ai/user/neobotjan2026) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to run DuckDuckGo web searches when current online information is needed and no built-in web search tool is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to an external DuckDuckGo-backed service. <br>
Mitigation: Avoid placing secrets, credentials, private identifiers, or confidential internal content in search queries. <br>
Risk: The skill depends on the Python ddgs package and its examples mention system-level package installation. <br>
Mitigation: Install the dependency in a virtual environment instead of modifying the system Python packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neobotjan2026/neo-ddg-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search results with titles, URLs, and snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result count defaults to 5; searches are sent to an external DuckDuckGo-backed service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
