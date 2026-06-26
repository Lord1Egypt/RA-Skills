## Description: <br>
Parallel provides high-accuracy web search and research via the Parallel.ai API for agent workflows, returning cited excerpts, structured results, and optional multi-step reasoning modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to perform web research, fact-checking, company and person research, content extraction, structured entity discovery, and monitored web tracking with source links and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a hidden fallback API key in scripts/search.py. <br>
Mitigation: Remove or verify the embedded key before installation and configure a user-owned PARALLEL_API_KEY instead. <br>
Risk: Queries, URLs, objectives, task inputs, monitor events, webhook payloads, and optional authenticated browsing credentials may be sent to external services. <br>
Mitigation: Treat inputs as data shared with third parties, avoid sensitive data unless approved, and set BROWSERUSE_API_KEY only when authenticated browsing is intended. <br>
Risk: Monitor creation can leave persistent account state and webhook integrations. <br>
Mitigation: Create monitors only when there is a plan to review, manage, and delete them when no longer needed. <br>


## Reference(s): <br>
- [Parallel Skill on ClawHub](https://clawhub.ai/mvanhorn/parallel) <br>
- [Parallel.ai](https://parallel.ai) <br>
- [Parallel API Documentation](https://docs.parallel.ai) <br>
- [Parallel Platform](https://platform.parallel.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON results with source URLs, excerpts, citations, task identifiers, status details, and usage information.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARALLEL_API_KEY for normal use; optional BrowserUse authentication can be enabled for authenticated browsing.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
