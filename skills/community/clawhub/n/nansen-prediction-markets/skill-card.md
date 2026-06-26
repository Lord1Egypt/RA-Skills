## Description: <br>
Polymarket screeners — discover trending events, top markets by volume, and search for specific markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to browse Polymarket prediction-market activity through Nansen CLI screeners, including trending events, high-volume markets, keyword searches, closed markets, and market categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a NANSEN_API_KEY credential and invokes the nansen CLI. <br>
Mitigation: Review the requested environment variable, CLI installation metadata, and generated commands before installation or execution. <br>
Risk: The security summary notes that the supplied artifact was not available for full verification. <br>
Mitigation: Review the artifact contents and install metadata before deployment; the supplied scan telemetry gives no supported reason to block the release. <br>


## Reference(s): <br>
- [Nansen Prediction Markets on ClawHub](https://clawhub.ai/nansen-devops/nansen-prediction-markets) <br>
- [nansen-devops publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY environment variable.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
