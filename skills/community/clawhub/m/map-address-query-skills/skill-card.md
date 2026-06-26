## Description: <br>
Map service address lookup and distance-query workflow for resolving addresses and POIs to coordinates, measuring travel distance and duration, and running route distance matrix queries with Tencent Location Service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottkiss](https://clawhub.ai/user/scottkiss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to set up Tencent Location Service access, geocode natural-language addresses, calculate travel distance and duration between places, and request structured route matrix results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script downloads a third-party qq-map-cli release before map queries can run. <br>
Mitigation: Install only when the scottkiss/qq-map-cli release source is trusted. <br>
Risk: The Tencent Location Service API key can be stored in a persistent config file at ~/.qq_map_cli_config.json. <br>
Mitigation: Use a restricted Tencent key and protect or delete the config file when it is no longer needed. <br>
Risk: Address and route queries are sent to Tencent Location Service. <br>
Mitigation: Avoid sending sensitive addresses or routes unless sharing them with Tencent is acceptable. <br>


## Reference(s): <br>
- [Tencent Location Service Console](https://lbs.qq.com/dev/console/application/mine) <br>
- [qq-map-cli macOS release download](https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-darwin-arm64.zip) <br>
- [qq-map-cli Linux release download](https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-linux-x86_64.zip) <br>
- [qq-map-cli Windows release download](https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-windows-x86_64.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI results may be human-readable text or JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a persistent Tencent API key configuration file and supports geocoder, address-distance, and distance-matrix CLI workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
