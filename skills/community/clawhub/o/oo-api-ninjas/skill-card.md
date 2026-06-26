## Description: <br>
API Ninjas (api-ninjas.com). Use this skill for ANY API Ninjas request — searching and reading data. Whenever a task involves API Ninjas, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query API Ninjas location and environment data through an OOMOL-connected account, including geocoding, reverse geocoding, timezone, weather, forecast, and air quality lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires authenticated OOMOL and API Ninjas access and can fail when credentials, scopes, or billing are not ready. <br>
Mitigation: Use an already connected account when available, follow setup only after auth or connection failures, and resolve expired credentials or billing errors before retrying. <br>
Risk: Incorrect request payloads can produce failed or misleading API lookups. <br>
Mitigation: Inspect each action's live schema with the oo CLI before constructing request data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-api-ninjas) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [API Ninjas Homepage](https://api-ninjas.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector responses as JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
