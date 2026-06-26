## Description: <br>
Webshare (webshare.io) connector skill for searching and reading Webshare account, proxy configuration, proxy listing, and hourly usage data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run read-only Webshare connector actions through an OOMOL-connected account, including profile lookup, proxy configuration, proxy listings, and hourly usage statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require sensitive Webshare credentials through an OOMOL-connected account. <br>
Mitigation: Install and use it only when the publisher and OOMOL connection flow are trusted, and rely on server-side credential injection rather than handling raw tokens. <br>
Risk: First-time setup includes optional remote installer commands for the oo CLI. <br>
Mitigation: Review the official install guide or verify the installer before running curl or PowerShell installer commands. <br>
Risk: Connector actions depend on live schemas and may fail if authentication, connection scopes, credentials, or billing are not current. <br>
Mitigation: Inspect the live connector schema before each action and use the documented setup or billing recovery steps only after a command fails with the matching error. <br>


## Reference(s): <br>
- [Webshare homepage](https://www.webshare.io/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-webshare) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for invoking oo connector schema and oo connector run; connector responses are JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
