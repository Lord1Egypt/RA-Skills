## Description:

Local encrypted execution base for multi-agent, cross-node, privacy-preserving task execution, with storage for secrets and scripts and sealed packages for cross-device delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent runtime operators use MGC Blackbox to store sensitive values and scripts locally, run them through MGC, and delegate sealed scripts or workflows across trusted nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports token access and local service calls as expected behaviors, while scan coverage is partial and some local references could not be resolved.

Mitigation: Protect the MGC token file, review examples before running them, and inspect unresolved references before relying on the security assessment.

Risk: The weather example sends the supplied city to wttr.in.

Mitigation: Avoid using sensitive location details in the city value, or review and change the example before running it.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/zkeviny/skills/mgc-meta-skill)
- [MGC Blackbox Project Homepage](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox Issue Tracker](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Code, API calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP and REST API usage, installation steps, and security guidance.]

## Skill Version(s):

1.5.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
