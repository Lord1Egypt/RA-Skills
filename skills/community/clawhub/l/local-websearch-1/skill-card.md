## Description: <br>
Searches the web through a user-configured SearXNG metasearch engine and returns structured results without requiring search API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eg-yks](https://clawhub.ai/user/eg-yks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run current web searches through a self-hosted SearXNG endpoint and receive JSON search results with source engines, URLs, descriptions, and scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG instance and may be forwarded to upstream search engines. <br>
Mitigation: Use only a trusted SearXNG instance and avoid sending sensitive or confidential queries. <br>
Risk: The skill depends on correct local setup for python3, SEARXNG_URL, and the packaged script path. <br>
Mitigation: Verify the environment variable and installed script location before relying on search results in an agent workflow. <br>


## Reference(s): <br>
- [SearXNG documentation](https://docs.searxng.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON search results from a command-line invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the SEARXNG_URL environment variable; result count is bounded from 1 to 20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
