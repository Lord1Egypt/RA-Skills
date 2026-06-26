## Description: <br>
Queries KZCloud CXO map records by location and filters results by function, grade, position camp, distance range, and keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuxiaoxin00](https://clawhub.ai/user/yuxiaoxin00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to authenticate to a KZCloud endpoint, convert user locations through a map skill, and retrieve nearby CXO business-card records in a structured table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The login flow handles account credentials and reusable access tokens. <br>
Mitigation: Use only trusted KZCloud accounts, avoid high-value credentials, and rotate or remove K1_KZClOUD_TOKEN after use. <br>
Risk: The artifact login script disables TLS certificate verification and sends requests to a fixed KZCloud endpoint. <br>
Mitigation: Confirm the endpoint is trusted before use and prefer a version that keeps TLS verification enabled. <br>
Risk: The login script prints the access token and attempts to persist it in the user environment. <br>
Mitigation: Do not share logs containing tokens, clear persisted tokens when no longer needed, and prefer secure prompting and secret storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuxiaoxin00/k1-kzcloud-skill) <br>
- [Gaode Map LBS dependency skill](https://clawhub.ai/lbs-amap/amap-lbs-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured tabular results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires K1_KZClOUD_TOKEN and may call KZCloud and Gaode Map services.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
