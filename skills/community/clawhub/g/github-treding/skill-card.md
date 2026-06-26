## Description: <br>
Fetch top trending GitHub repositories today/this-week/this-month and summarize top 15 with stars, language, description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunovu20](https://clawhub.ai/user/brunovu20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to fetch and summarize recently created GitHub repositories ranked by stars. It supports quick repository discovery over default or custom date ranges and result counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts GitHub and can use GH_TOKEN if that environment variable is set. <br>
Mitigation: Run it without GH_TOKEN unless authenticated GitHub API quota is intentionally needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brunovu20/github-treding) <br>
- [GitHub Search repositories API endpoint](https://api.github.com/search/repositories) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text formatted from GitHub API JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; optionally uses GH_TOKEN for higher GitHub API rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
