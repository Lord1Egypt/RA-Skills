## Description: <br>
Harmonic.ai helps agents search, enrich, and read Harmonic.ai company and person data through a connected OOMOL account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Harmonic.ai company and person enrichment, profile lookup, employee listing, and enrichment status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company websites, LinkedIn URLs, email addresses, and similar identifiers may be sent to OOMOL and Harmonic.ai for enrichment or lookup. <br>
Mitigation: Submit only identifiers the user intends to use for that Harmonic.ai action and avoid unnecessary sensitive data. <br>
Risk: The skill depends on an authenticated OOMOL account with a connected Harmonic.ai credential. <br>
Mitigation: Use first-time setup steps only after an authentication or connection error, and confirm account readiness before retrying. <br>


## Reference(s): <br>
- [Harmonic.ai homepage](https://harmonic.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-harmonic-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include Harmonic.ai data plus connector execution metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
