## Description: <br>
TomTom helps agents search and read TomTom location data through OOMOL's oo CLI connector instead of calling the TomTom API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent perform TomTom location search workflows such as autocomplete, fuzzy search, nearby POI search, geocoding, and reverse geocoding through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected TomTom credential to run connector actions. <br>
Mitigation: Grant or refresh TomTom access only for the intended account and task, and rely on OOMOL's server-side credential injection rather than exposing raw tokens to the agent. <br>
Risk: Incorrect action payloads can produce failed or misleading location search results. <br>
Mitigation: Inspect each action's live connector schema before sending data and keep the listed TomTom actions limited to read-only search and geocoding workflows. <br>


## Reference(s): <br>
- [ClawHub TomTom Skill](https://clawhub.ai/oomol/oo-tomtom) <br>
- [TomTom Developer](https://developer.tomtom.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; TomTom responses are returned as JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
