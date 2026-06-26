## Description: <br>
Query Joe's Corner, a news and content aggregator built for the AI age, when the user wants live content, asks about Joe's Corner, or is building with the Joe's Corner API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joescorner](https://clawhub.ai/user/joescorner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Joe's Corner feeds and retrieve public posts for topic tracking, link discovery, research gathering, dashboards, and digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public content from joescorner.ai, so returned posts may be incomplete, outdated, or unsuitable as the sole basis for important decisions. <br>
Mitigation: Use the returned source links and timestamps to verify important claims against primary sources before acting on them. <br>
Risk: The scripts install and use the Joe's Corner Python client through uv or pip. <br>
Mitigation: Install in a managed environment and pin or review package versions according to local dependency policy. <br>
Risk: The skill makes outbound network requests to Joe's Corner API endpoints. <br>
Mitigation: Invoke it only for explicit Joe's Corner feed or API tasks, or restrict network access where tighter control is required. <br>


## Reference(s): <br>
- [Joe's Corner](https://joescorner.ai) <br>
- [ClawHub skill page](https://clawhub.ai/joescorner/joescorner) <br>
- [Joe's Corner Python client](https://github.com/joescorner/joescorner-python) <br>
- [Joe's Corner OpenAPI spec](https://github.com/joescorner/joescorner-openapi) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON or compact plain text from Joe's Corner API scripts, with concise guidance when selecting feeds or posts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API calls; no authentication required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
