## Description: <br>
A developer-focused JFTech device API skill for checking camera status and managing PTZ movement, masking, zoom/focus, presets, and tour plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate JFTech PTZ cameras through the official API, including status checks, directional movement, privacy masking, zoom/focus, presets, and tour management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move a live PTZ camera, enable masking, delete presets, or change tour behavior. <br>
Mitigation: Require explicit confirmation before camera movement, masking, preset deletion, or tour changes. <br>
Risk: The skill requires JF API credentials and device identifiers. <br>
Mitigation: Use dedicated credentials where possible, keep credentials in environment variables, and avoid command-line arguments or configuration files for secrets. <br>
Risk: Requests are sent to the configured JFTech API endpoint. <br>
Mitigation: Verify JF_ENDPOINT before running and use the official international or mainland China endpoint appropriate for the deployment. <br>
Risk: PTZ start actions can continue movement until a stop action is sent or the device reaches its limit. <br>
Mitigation: Send PTZ start and stop commands serially, confirm stop execution, and use short movement intervals for live devices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jftech-open-pro-ptz-control) <br>
- [JFTech Open Platform](https://open.jftech.com/) <br>
- [JFTech API Documentation](https://docs.jftech.com/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JF API credentials, a target device serial number, and network access to the configured JFTech API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
