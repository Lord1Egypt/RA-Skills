## Description: <br>
Use this skill for NeverBounce (neverbounce.com) requests, including reading, creating, and updating data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to verify single email addresses, manage NeverBounce bulk verification jobs, download results, and check account status through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk verification jobs may upload or process email lists and consume NeverBounce or OOMOL account credits. <br>
Mitigation: Review job payloads, remote file sources, filters, and expected credit impact before approving write actions. <br>
Risk: The skill requires a connected NeverBounce account with sensitive credentials managed through OOMOL. <br>
Mitigation: Use the OOMOL CLI connection flow and do not request or handle raw NeverBounce tokens; troubleshoot authentication only after a command reports an auth or connection failure. <br>


## Reference(s): <br>
- [NeverBounce homepage](https://neverbounce.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [NeverBounce skill on ClawHub](https://clawhub.ai/oomol/oo-neverbounce) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return NeverBounce JSON responses or CSV job-result downloads through the oo connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
