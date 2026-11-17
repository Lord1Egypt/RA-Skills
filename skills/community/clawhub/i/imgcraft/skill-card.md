## Description:

Fetch your public IP address and display connection info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check the public IP address seen by an external service when debugging VPN, proxy, network, or API rate-limiting behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill sends a request to httpbin.org, revealing the user's public IP address and ordinary request metadata to that external service.

Mitigation: Install and run only when that disclosure is acceptable for the user's network, VPN, or proxy debugging task.

## Reference(s):

- [httpbin GET endpoint](https://httpbin.org/get)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown guidance with an inline shell command; runtime output is a plain-text public IP address.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contacts httpbin.org and prints the origin IP reported by that service.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
