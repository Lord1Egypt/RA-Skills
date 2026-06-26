## Description: <br>
Predict the likely gender associated with a first name -- with optional country-specific calibration via genderize.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to estimate name-associated gender distributions, optionally calibrated by ISO 3166-1 alpha-2 country code, for personalization, demographic analysis, research, or form pre-filling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted names and optional country codes are sent to the Pipeworx/Genderize remote service. <br>
Mitigation: Use the skill only with data that users are permitted to send to that service, and review consent, privacy, and retention requirements before sensitive or bulk use. <br>
Risk: Gender predictions are statistical guesses and may be incorrect or inappropriate for consequential decisions. <br>
Mitigation: Do not treat outputs as authoritative identity information or use them for eligibility, employment, credit, insurance, or other high-impact decisions. <br>
Risk: The setup uses an unpinned mcp-remote@latest dependency. <br>
Mitigation: Review and pin the dependency version before managed or production deployment. <br>


## Reference(s): <br>
- [Pipeworx Genderize homepage](https://pipeworx.io/packs/genderize) <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-genderize) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [JSON responses and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns statistical gender predictions with probability, count, and optional country-specific calibration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
