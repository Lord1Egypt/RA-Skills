## Description: <br>
Expose OGP via a public HTTPS endpoint, usually a stable Cloudflare hostname or named tunnel, and help verify or fix gateway reachability and gatewayUrl alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dp-pcs](https://clawhub.ai/user/dp-pcs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to expose an OGP daemon through a stable Cloudflare hostname, a temporary cloudflared/ngrok tunnel, or another public HTTPS endpoint. It also guides them through checking that the public discovery endpoint, local daemon discovery card, and framework gatewayUrl agree before federation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an OGP daemon reachable from the public internet. <br>
Mitigation: Use it only for intentional public exposure, prefer HTTPS endpoints, and verify that the selected framework and local port are correct before federating. <br>
Risk: A stale or mismatched gatewayUrl can advertise the wrong public endpoint or framework identity. <br>
Mitigation: Compare the local discovery card, public discovery card, and framework gatewayUrl after any tunnel or routing change. <br>
Risk: Provider credentials or permanent tunnel services can create lasting exposure if configured casually. <br>
Mitigation: Keep Cloudflare and ngrok credentials private, review install commands before running them, and enable launchd or systemd persistence only for deliberate permanent deployments. <br>


## Reference(s): <br>
- [ClawHub Skill: Ogp Expose](https://clawhub.ai/dp-pcs/ogp-expose) <br>
- [OGP documentation](https://github.com/dp-pcs/ogp) <br>
- [Cloudflare tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>
- [ngrok download](https://ngrok.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, XML, and INI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public endpoint checks, tunnel setup steps, and service persistence examples.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
