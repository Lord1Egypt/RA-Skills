## Description: <br>
Aviationstack (aviationstack.com). Use this skill for ANY Aviationstack request - searching and reading data. Whenever a task involves Aviationstack, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Aviationstack data through an OOMOL-connected account, including aircraft, airlines, airports, cities, countries, taxes, flights, and routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Aviationstack account, so queries may use connected account access or billing credits. <br>
Mitigation: Confirm trust in OOMOL and the oo CLI before use, and monitor billing or credit limits before retrying failed requests. <br>
Risk: The fallback setup path includes installing the oo CLI if it is missing. <br>
Mitigation: Run the installer only when the oo command is actually unavailable and after reviewing the installation source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-aviationstack) <br>
- [Aviationstack Homepage](https://aviationstack.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses read-only connector actions and may return Aviationstack records with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
