## Description:

Fetches current pollen forecasts for Swedish locations from Pollenrapporten, including severity levels and optional grass pollen alert guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laurobrcwb](https://clawhub.ai/user/laurobrcwb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Swedish pollen forecasts for supported cities and nearby monitoring regions. It can summarize current pollen levels and provide general grass pollen precautions, but it should not be treated as personalized medical advice.

### Deployment Geography for Use:

Global, for Swedish pollen forecast coverage.

## Known Risks and Mitigations:

Risk: Forecast lookups contact api.pollenrapporten.se and depend on that external service.

Mitigation: Review network access before installation and expect output quality to depend on the API's availability and freshness.

Risk: Grass pollen alerts could be mistaken for personalized medical advice.

Mitigation: Present alert text as general allergy guidance only and defer medical decisions to qualified clinicians.

## Reference(s):

- [Pollenrapporten API](https://api.pollenrapporten.se/v1/)
- [Region mappings](references/regions.json)
- [ClawHub skill page](https://clawhub.ai/laurobrcwb/skills/pollen-rapporten)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal output with pollen levels, forecast summaries, and optional grass pollen alert guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls api.pollenrapporten.se at runtime and uses bundled Swedish region mappings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
