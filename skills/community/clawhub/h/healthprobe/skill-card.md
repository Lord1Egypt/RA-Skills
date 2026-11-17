## Description:

Probes a URL to report HTTP status code, response latency in milliseconds, and a healthy/not-healthy verdict with a configurable timeout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Healthprobe to check whether an API or web URL is responsive before making dependent calls. It returns a simple health verdict, status code, latency, and connection error details when a probe fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local URL-probing service can be abused to reach internal network resources from the host running it.

Mitigation: Keep the service limited to localhost, avoid shared or untrusted deployments without authentication and egress controls, and block private, loopback, link-local, and cloud metadata destinations before use.

## Reference(s):

- [Healthprobe ClawHub skill page](https://clawhub.ai/mirni/skills/healthprobe)
- [Publisher profile: mirni](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON response with URL, health verdict, HTTP status code, latency in milliseconds, and optional error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timeout is configurable from 100ms to 30000ms; status_code is -1 when a connection error occurs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
