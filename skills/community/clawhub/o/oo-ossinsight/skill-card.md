## Description: <br>
OSS Insight helps agents search and read OSS Insight data through the OOMOL `oo` CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query OSS Insight analytics for GitHub repositories, including stars, issues, pull requests, creators, countries, organizations, trends, collections, and collection rankings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs external `oo` CLI commands and depends on live connector schemas. <br>
Mitigation: Inspect the connector schema for the selected action before building a payload, and run only actions whose effects are understood. <br>
Risk: First-time setup may require installing or authenticating the `oo` CLI. <br>
Mitigation: Run setup commands only when the corresponding command-not-found or authentication failure occurs. <br>


## Reference(s): <br>
- [OSS Insight homepage](https://ossinsight.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ossinsight) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
