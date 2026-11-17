## Description:

Measures network download speed, upload speed, and latency from the command line using Cloudflare speed test endpoints and public DNS latency targets with no external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT administrators, and support teams use this skill to check internet throughput, diagnose slow connections, measure latency and jitter, and collect command-line or JSON network performance results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends test traffic to Cloudflare endpoints and opens TCP connections to public DNS IPs.

Mitigation: Run it only on networks where that traffic is approved and expected.

Risk: Very large custom --size values can consume significant bandwidth and memory.

Mitigation: Use the default or modest --size values, especially on metered or shared networks.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or structured JSON from command-line execution, with Markdown instructions and bash examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys or accounts required; custom test size controls bandwidth and upload memory use.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
