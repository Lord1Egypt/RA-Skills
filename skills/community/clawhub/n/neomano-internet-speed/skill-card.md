## Description:

Measure current internet connection speed (download + upload) from this machine using a lightweight HTTP-based speed test against Cloudflare speed endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can ask an agent to measure current download and upload throughput from the local machine and report the results in Mbps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the speed test sends and receives network traffic with Cloudflare from the user's machine.

Mitigation: Use the skill only when the user asks for a speed test and is comfortable with Cloudflare endpoint traffic from the current network.

Risk: Large custom download or upload byte values can consume bandwidth on metered or constrained networks.

Mitigation: Keep default byte values unless larger tests are necessary, and avoid large custom values on metered or limited connections.

Risk: Throughput measurements can be misleading because results depend on current network conditions and routing.

Mitigation: Treat reported Mbps values as point-in-time estimates and rerun when conditions or routing may have changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-internet-speed)
- [Cloudflare speed download endpoint](https://speed.cloudflare.com/__down)
- [Cloudflare speed upload endpoint](https://speed.cloudflare.com/__up)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text Mbps measurements with optional Markdown shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports download and upload throughput; results vary with current network conditions and routing.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
