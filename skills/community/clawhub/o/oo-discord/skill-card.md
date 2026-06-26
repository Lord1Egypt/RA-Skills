## Description: <br>
Discord lets an agent read and manage Discord data through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Discord account, guild, invite, connection, entitlement, and public key data, and to perform approved Discord account-related updates through the OOMOL connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a connected Discord account and may perform write or destructive actions. <br>
Mitigation: Confirm the exact payload and effect before write actions, and get explicit user approval before destructive actions. <br>
Risk: Connector access depends on OOMOL-managed credentials and first-time oo CLI setup. <br>
Mitigation: Install only if you trust OOMOL as the connector provider, and run installer, authentication, or connection steps only when a command fails for that setup reason. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-discord) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Discord Homepage](https://discord.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch the live connector schema before building payloads; user confirmation is required for write actions and explicit approval is required for destructive actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version and frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
