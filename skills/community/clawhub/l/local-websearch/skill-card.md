## Description: <br>
Searches the web through a configured self-hosted SearXNG metasearch instance and returns structured results without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stperic](https://clawhub.ai/user/stperic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when current web information is needed through a SearXNG instance they control or trust. It is suited for web lookup and research requests where JSON search results are useful to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG server, which may expose private or sensitive terms if the server is not trusted. <br>
Mitigation: Configure SEARXNG_URL to a trusted instance, prefer HTTPS for remote instances, and avoid placing secrets or highly sensitive private data in search queries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stperic/local-websearch) <br>
- [SearXNG documentation](https://docs.searxng.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON search result object printed to stdout, with setup and invocation commands documented in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEARXNG_URL; accepts query text, result count from 1 to 20, and an optional language code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
