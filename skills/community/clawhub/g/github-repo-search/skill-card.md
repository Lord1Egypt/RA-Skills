## Description: <br>
Helps users search and filter public GitHub repositories, then produces a structured recommendation report with comparable candidate projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackhua6](https://clawhub.ai/user/jackhua6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical evaluators use this skill to turn a natural-language open-source project need into GitHub search queries, filtering rules, ranked repository candidates, and decision-ready recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub access may use token-backed permissions for search and repository tasks. <br>
Mitigation: Use a fine-scoped GitHub token, avoid broad organization-wide permissions, and require explicit confirmation before write actions such as creating branches, editing issues or pull requests, changing settings, or triggering CI. <br>
Risk: Repository recommendations can become stale or hard to reproduce because GitHub search results and API quota state change. <br>
Mitigation: Record the search time and quota status, apply documented filters, and re-check repository metadata before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackhua6/github-repo-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown report with query lists, filtering criteria, summary counts, and a Top N comparison table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes repository metadata, recommendation rationale, risk notes, and next-step suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
