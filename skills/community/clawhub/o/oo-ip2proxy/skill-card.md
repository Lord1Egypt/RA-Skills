## Description: <br>
IP2Proxy helps an agent inspect IP2Proxy requests by looking up whether an IPv4 or IPv6 address is a proxy through the OOMOL IP2Proxy connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to check whether an IP address is associated with proxy usage through an OOMOL-connected IP2Proxy account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account and sensitive IP2Proxy credentials to run lookups. <br>
Mitigation: Keep credentials scoped in the connected account, review each oo command before execution, and resolve authentication, scope, or billing errors only when command output requires it. <br>
Risk: Incorrect connector payloads could send unintended lookup inputs or fail against the live IP2Proxy action contract. <br>
Mitigation: Inspect the live action schema before constructing payloads and confirm any future write or destructive actions before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ip2proxy) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [IP2Proxy homepage](https://www.ip2location.com/web-service/ip2proxy) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema checks before running IP2Proxy lookup requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
