## Description: <br>
Plans multi-night stargazing and astrophotography routes by comparing nightly candidates for route continuity, transfer distance, lodging continuity, feasibility, backup routes, far-line options, and route risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clhwbd](https://clawhub.ai/user/clhwbd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan practical multi-night stargazing or astrophotography trips. It is intended for questions about the smoothest holiday route, main versus backup route choices, far-line alternatives, and whether a high-scoring single night is worth a long transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live weather retrieval may disable TLS certificate verification during retries, which can compromise the integrity of weather-dependent route recommendations. <br>
Mitigation: Require normal HTTPS certificate verification for all weather requests and fail clearly when secure retrieval is unavailable. <br>
Risk: Multi-night route plans depend on weather, astronomy, and geographic inputs that can change or be incomplete. <br>
Mitigation: Review the referenced inputs before travel and treat the skill's route output as planning guidance rather than a booking or safety decision. <br>


## Reference(s): <br>
- [Go Stargazing Trip ClawHub page](https://clawhub.ai/clhwbd/go-stargazing-trip) <br>
- [Agent Contract](references/agent-contract.md) <br>
- [Dynamic Sampling Plan](references/dynamic-sampling-plan.md) <br>
- [Current Output Schema](references/output-schema-current.md) <br>
- [Scope Policy](references/scope-policy.md) <br>
- [Scoring Lite](references/scoring-lite.md) <br>
- [Stargazing Scoring System](references/stargazing_scoring_system.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown planning guidance with optional shell commands and structured route details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces main routes, backup routes, far-line options, nightly suggestions, reference information, and route risk notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
