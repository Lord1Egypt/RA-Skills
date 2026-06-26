## Description: <br>
Save, inspect, activate, and compare Hong Kong IPO scoring parameter versions across weights, thresholds, and cost assumptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to manage stateful Hong Kong IPO scoring parameters, compare candidate versions, and activate the parameter version used by later scoring or recommendation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the package exposes broader financial-data, profile, network, and persistence behavior than the parameter-manager description alone suggests. <br>
Mitigation: Review the runtime before installation, run only explicit commands, and avoid granting the skill open-ended authority over financial workflows. <br>
Risk: The runtime may store financial preferences and review history locally. <br>
Mitigation: Treat ~/.hkipo-next/data/hkipo.db as sensitive local data, protect or remove it when no longer needed, and avoid storing unnecessary personal financial assumptions. <br>
Risk: The runtime may cache market data and make requests to third-party finance sites. <br>
Mitigation: Use it only where those network requests are acceptable, and verify external data before relying on generated IPO decisions or recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hackstoic/hkipo-parameter-manager) <br>
- [hkipo-next runtime README](runtime/hkipo-next/README.md) <br>
- [AiPO API documentation](runtime/hkipo-next/references/aipo-api.md) <br>
- [API Guide](runtime/hkipo-next/references/api-guide.md) <br>
- [HK IPO mechanism guide](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [HK IPO analysis guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [Risk preference guide](runtime/hkipo-next/references/risk-preferences.md) <br>
- [AiPO service](https://aipo.myiqdii.com) <br>
- [AASTOCKS IPO market](https://www.aastocks.com/tc/stocks/market/ipo/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [CLI output in JSON, text, or markdown, with parameter-management commands and structured response objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parameter versions are stored locally by default under ~/.hkipo-next/data/hkipo.db.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, release metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
