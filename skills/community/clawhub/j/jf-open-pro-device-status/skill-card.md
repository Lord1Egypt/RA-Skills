## Description: <br>
Checks whether JF devices are online or offline, with support for single-device and batch status queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query JF Open Platform device connectivity, including single-device checks and batches of up to 500 device tokens. <br>

### Deployment Geography for Use: <br>
China, Asia, Europe, and North America endpoints are documented; reviewers should confirm deployment availability for the target JF Open Platform account. <br>

## Known Risks and Mitigations: <br>
Risk: Signed JF credentials and device tokens can be sent to the endpoint named by JF_ENDPOINT. <br>
Mitigation: Keep JF_ENDPOINT set to an official JF regional host and install the skill only when JF device status checks are needed. <br>
Risk: Command-line arguments and token files can expose app secrets or device tokens. <br>
Mitigation: Prefer protected environment variables for JF credentials, restrict token-file access, and avoid passing secrets directly on the command line. <br>
Risk: Status output can disclose WAN IPs and device identifiers. <br>
Mitigation: Share table or JSON output only where disclosure of device identifiers and WAN IPs is acceptable. <br>


## Reference(s): <br>
- [JF Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-status) <br>
- [Publisher profile](https://clawhub.ai/user/jftech) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text, table, or JSON output with command-line usage and environment variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries require JF credentials and device tokens; responses may include device UUIDs, online/offline status, wake state, and WAN IP.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
