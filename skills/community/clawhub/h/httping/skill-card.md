## Description:

Lightweight HTTP endpoint health checks with curl. Use when an agent needs to (1) verify one or more URLs are reachable, (2) collect status codes, TLS info, and timing, or (3) loop-check a service during deployment or incident triage without standing up a full monitoring tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check HTTP(S) endpoint reachability, status codes, TLS timing, and response timing during deployment checks or incident triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps an agent make outbound curl requests to user-provided URLs.

Mitigation: Use it only for endpoints the user is authorized to test and ensure network egress is appropriate for the current host.

Risk: Repeated or unbounded probes can tie up an orchestration session or create unwanted traffic.

Mitigation: Use bounded curl timeouts and prefer cron or heartbeat scheduling over tight foreground sleep loops.

Risk: HTTP response bodies may contain unnecessary or sensitive data during health checks.

Mitigation: Discard response bodies during triage and surface only status, timing, TLS, remote IP, and failure facts.

## Reference(s):

- [Scheduling notes for httping](artifact/references/scheduling.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/httping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and key=value probe output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Probe facts include HTTP status, remote IP, timing, TLS verification result, or curl failure details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
