## Description: <br>
Openclaw Smart Cache helps agents add a two-layer local cache and request-learning workflow for repeated OpenClaw queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[king-nan](https://clawhub.ai/user/king-nan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to cache repeated API, database, configuration, scraping, or computation results and to learn frequent query patterns for tool recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cache and request learner can persist query history, cached results, and tool choices on local disk. <br>
Mitigation: Do not cache passwords, API keys, private personal data, or confidential business queries; clear stored cache and learner data when it is no longer needed. <br>
Risk: The package evidence contains documentation only, while the artifact describes external Python files and installation from an external repository. <br>
Mitigation: Verify the external repository and expected files before installing or executing any referenced cache manager, learner, or integration code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/king-nan/openclaw-smart-cache) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local in-memory and SQLite-backed caching patterns plus cache-management commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
