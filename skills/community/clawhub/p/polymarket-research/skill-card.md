## Description: <br>
Research any Polymarket topic to get market data, probabilities, volumes, and top holders in one read-only snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, market analysts, and agents use this skill to retrieve read-only Polymarket research snapshots for a topic, including probabilities, 24h volume, resolution dates, top holders, and AI divergence signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SIMMER_API_KEY credential to access Simmer SDK market data. <br>
Mitigation: Store the API key in a protected environment variable, avoid logging it, and rotate it if exposed. <br>
Risk: Market data and holder information can be incomplete, delayed, unavailable, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Treat the output as research context, review results before use, and verify important market data against the source venue. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-research) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/simmer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; supports topic query, minimum volume, maximum results, and top-holder count settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
