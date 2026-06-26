## Description: <br>
ipstack (ipstack.com). Use this skill for ANY ipstack request - searching and reading data. Whenever a task involves ipstack, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform read-only ipstack IP geolocation lookups through an OOMOL-connected account, including single-IP, requester-IP, and batch lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IP addresses are sent to the OOMOL/ipstack connector for geolocation. <br>
Mitigation: Use the skill only when sharing those IP addresses with the connected service is intended. <br>
Risk: The skill may require CLI login or connector setup for an OOMOL-connected account. <br>
Mitigation: Only follow install, login, or connection steps when intentionally enabling the ipstack integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ipstack) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [ipstack homepage](https://ipstack.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from connector actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only geolocation lookup results are returned by the OOMOL ipstack connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
