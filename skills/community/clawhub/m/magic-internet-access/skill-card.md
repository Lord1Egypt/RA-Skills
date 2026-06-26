## Description: <br>
AI-powered proxy assistant for OpenClaw that helps users fetch, test, filter, and format free public proxy nodes for common proxy clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadowrocketai](https://clawhub.ai/user/shadowrocketai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to receive guided device selection and proxy configuration output for public proxy clients such as Clash, Shadowrocket, and v2rayNG. It is intended for users who explicitly ask for proxy or connectivity assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches free public proxy nodes from untrusted sources, and those nodes may log, block, or tamper with traffic. <br>
Mitigation: Treat returned nodes as untrusted and avoid using them for banking, email, work accounts, or other sensitive activity. <br>
Risk: Local cache files may contain usable proxy credentials or connection strings. <br>
Mitigation: Store generated node cache files only in trusted local workspaces and clear them when no longer needed. <br>


## Reference(s): <br>
- [Magic Internet Access on ClawHub](https://clawhub.ai/shadowrocketai/magic-internet-access) <br>
- [Publisher profile](https://clawhub.ai/user/shadowrocketai) <br>
- [Publisher homepage](https://shadowrocket.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Plain text prompts and proxy configuration strings, with JSON or base64 configuration output depending on the selected client.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs public proxy nodes and client-specific setup guidance; generated nodes should be treated as untrusted.] <br>

## Skill Version(s): <br>
1.8.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
