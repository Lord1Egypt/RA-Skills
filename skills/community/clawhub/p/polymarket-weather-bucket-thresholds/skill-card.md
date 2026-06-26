## Description: <br>
Global temperature bucket threshold strategy via Simmer that buys YES under 15%, sells YES positions at 45%, caps entries near $2, limits scans to 5 trades, and runs every 2 minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OxSnosh](https://clawhub.ai/user/OxSnosh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading-automation users use this skill to run a scheduled Simmer strategy for weather-related prediction markets with fixed entry, exit, spend, and scan limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can trade with Simmer account access and may sell broader account positions than the advertised weather strategy. <br>
Mitigation: Keep dry-run enabled until reviewed, use a least-privilege API key where available, and restrict live execution to positions opened by this strategy or explicitly approved markets. <br>
Risk: The skill runs on a two-minute schedule and can repeatedly evaluate or place trades. <br>
Mitigation: Confirm trade caps, warning handling, and scheduling before enabling managed execution. <br>
Risk: No license identifier is available in the release evidence. <br>
Mitigation: Confirm the license and terms of use before redistribution or commercial deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OxSnosh/polymarket-weather-bucket-thresholds) <br>
- [Publisher profile](https://clawhub.ai/user/OxSnosh) <br>
- [Simmer Markets API endpoint](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line guidance for configuring and running the Simmer trading script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk dependency; dry-run is the default unless live execution is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
