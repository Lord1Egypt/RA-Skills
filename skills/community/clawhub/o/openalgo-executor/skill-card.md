## Description: <br>
Interacts with the OpenAlgo API for trading operations by placing market or limit orders, retrieving positions, and fetching symbol quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anthonyabraham1379-pixel](https://clawhub.ai/user/anthonyabraham1379-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation operators use this skill to query an OpenAlgo service for positions and quotes or submit market and limit orders through a configured endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real trading orders through OpenAlgo. <br>
Mitigation: Use only endpoints you control and add explicit live-trade confirmation and safe order limits before connecting it to a funded account. <br>
Risk: The script defaults to an undocumented remote endpoint rather than the documented localhost service. <br>
Mitigation: Change or override the default URL and verify the endpoint before sending position, quote, or order requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses and plain-text CLI messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Order placement can affect real trading accounts when connected to a live OpenAlgo endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
