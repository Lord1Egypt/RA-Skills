## Description: <br>
ConvoYield gives bots a local conversation analytics layer that detects sentiment opportunities, micro-conversions, engagement momentum, yield forecasts, and recommended response strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and bot builders use this skill to analyze user messages, estimate conversation value, and select sales or engagement plays for conversational agents without relying on external APIs for the core analytics path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes cloud telemetry, billing, and persistent analytics features beyond the local conversation analytics core. <br>
Mitigation: Review data flows, storage locations, network exposure, and payment behavior before enabling cloud or interactive modes. <br>
Risk: The release includes wallet, mining, marketplace, and persistent ledger components. <br>
Mitigation: Avoid coin-related modes unless those capabilities are explicitly needed and have been reviewed as high-impact financial-style behavior. <br>
Risk: Security evidence marks the package suspicious because the shipped ecosystem is broader than a local analytics helper. <br>
Mitigation: Install and run only in contexts where the broader ConvoYield feature set is intended, and scan the package before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jcools1977/opencrawl) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Code] <br>
**Output Format:** [Python objects and text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core conversation analysis is local and heuristic; optional cloud, telemetry, billing, wallet, mining, marketplace, and ledger features require separate review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
