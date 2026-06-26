## Description: <br>
Ok Computer Swarm runs concurrent DuckDuckGo searches for multiple user-provided topics and returns a structured report of top results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grahammiranda13](https://clawhub.ai/user/grahammiranda13) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and other ClawHub users use this skill to gather high-level starting-point research across several topics in parallel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided search queries are sent to DuckDuckGo. <br>
Mitigation: Avoid using secrets, credentials, or confidential internal details as search queries. <br>
Risk: The requests dependency is specified as a lower-bound version rather than a locked package hash. <br>
Mitigation: Install in a managed environment and pin or review dependency versions before production deployment. <br>
Risk: DuckDuckGo free API results may be incomplete or insufficient for deep analysis. <br>
Mitigation: Treat results as a starting point and corroborate important claims with additional sources or review tools. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/grahammiranda13/openclaw-ok-computer-skill) <br>
- [Publisher homepage](https://www.grahammiranda.com/) <br>
- [DuckDuckGo API endpoint](https://api.duckduckgo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON search-result report with title and URL fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one or more query values and an optional max-results limit; sends user-provided queries to DuckDuckGo.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
