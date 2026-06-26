## Description: <br>
Measures the current internet connection's download and upload speed from the local machine using Cloudflare speed test endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an on-demand download/upload throughput check from the machine running the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The speed test sends download and upload traffic to Cloudflare, which may be unsuitable on metered, restricted, or sensitive networks. <br>
Mitigation: Run it only on networks where the test traffic and Cloudflare visibility are acceptable. <br>
Risk: Measured throughput can vary with current network conditions and routing. <br>
Mitigation: Treat results as a point-in-time estimate and rerun when comparing network changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/elandivar/neomano-internet-speed) <br>
- [Cloudflare speed test download endpoint](https://speed.cloudflare.com/__down) <br>
- [Cloudflare speed test upload endpoint](https://speed.cloudflare.com/__up) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text speed measurements in Mbps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, uses no external Python dependencies, and contacts Cloudflare speed test endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
