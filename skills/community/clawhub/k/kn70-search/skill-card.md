## Description: <br>
Search the web using multiple engines (Tavily, multi-search-engine, or SearXNG). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollisken](https://clawhub.ai/user/hollisken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web, news, technical, research, and Chinese-language searches through Tavily, self-hosted SearXNG, or multi-engine search providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports an embedded Tavily API key and advises avoiding sensitive searches until it is removed. <br>
Mitigation: Remove and rotate the embedded key, then require users to provide their own TAVILY_API_KEY before using Tavily-backed searches. <br>
Risk: The security scan reports that normal searches may run an unreviewed local Python script. <br>
Mitigation: Verify or vendor the referenced script before deployment, or disable the code paths that execute it. <br>
Risk: The security guidance reports that the multi-engine path does not match the documented behavior. <br>
Mitigation: Fix and test the multi-engine implementation before relying on that engine in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hollisken/kn70-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [JSON-like search result objects with titles, URLs, snippets, engine metadata, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports query, max_results, and engine selection; artifact describes a 20 calls/min rate limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
