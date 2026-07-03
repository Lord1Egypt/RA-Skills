## Description: <br>
Local Search runs web searches from the user's machine against public search engines with automatic fallback and returns structured result items for current web information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakurakilove](https://clawhub.ai/user/sakurakilove) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current public web information, verify facts, collect sources, and produce structured search results without a search API key or cloud search service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the user's IP address are sent directly to the selected public search engines. <br>
Mitigation: Avoid sensitive queries unless that exposure is acceptable for the deployment environment. <br>
Risk: The skill uses browser-like headers when requesting public search result pages. <br>
Mitigation: Confirm that use complies with applicable internal policy and the selected search engines' terms before deployment. <br>
Risk: The explicit output option can save search results to a local path. <br>
Mitigation: Use only intended output paths and review saved files for sensitive content before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sakurakilove/skills/local-search) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [Structured search results as text or JSON, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result items include URL, title, snippet, host, rank, date, favicon, source engine, optional raw HTML, and optional relevance score.] <br>

## Skill Version(s): <br>
1.6.2 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
