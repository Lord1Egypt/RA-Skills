## Description: <br>
Imou Open Device Manage lets agents list Imou/Lecheng cloud devices, view device and channel details, query devices by serial number, and rename devices or channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Imou-OpenPlatform](https://clawhub.ai/user/Imou-OpenPlatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to inspect Imou cloud device inventory, check device and channel status, retrieve device details by serial number, and request controlled device or channel renames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Imou developer credentials to access account device inventory and perform device-management actions. <br>
Mitigation: Keep IMOU_APP_SECRET private, install only when this access is intended, and use credentials scoped to the intended Imou account. <br>
Risk: A rename request can change a device or channel name in the Imou cloud account. <br>
Mitigation: Confirm the device serial, channel ID when present, and new name before allowing rename commands. <br>
Risk: Using the wrong regional base URL can send requests to an unintended Imou endpoint or fail against the target account. <br>
Mitigation: Set IMOU_BASE_URL to the official Imou endpoint for the account region before running the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Imou-OpenPlatform/imou-device-manage) <br>
- [Imou Device API Reference](references/imou-device-api.md) <br>
- [Imou Open API Development Specification](https://open.imou.com/document/pages/c20750/) <br>
- [Get Access Token API](https://open.imou.com/document/pages/fef620/) <br>
- [List Devices by Page API](https://open.imou.com/document/pages/683248/) <br>
- [Get Devices by IDs API](https://open.imou.com/document/pages/320fb7/) <br>
- [Modify Device or Channel Name API](https://open.imou.com/document/pages/8ffaa3/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output, optional JSON, and Markdown guidance with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured Imou API credentials and endpoint to list devices, get device details, or rename a device or channel.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
