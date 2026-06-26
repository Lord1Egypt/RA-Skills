## Description: <br>
Post to LinkedIn using the official API v2. Uses OAuth tokens so only post when explicitly asked or scheduled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmythril](https://clawhub.ai/user/0xmythril) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with LinkedIn, verify account access, and post or share LinkedIn updates through linkedin-cli when the user explicitly requests it or a scheduled workflow triggers it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or delete LinkedIn posts when valid OAuth credentials are available. <br>
Mitigation: Confirm the exact post, share, or deletion target with the user before running linkedin-cli, and use an account whose LinkedIn posting authority is acceptable for this workflow. <br>
Risk: Security evidence notes a mismatch between posting-only documentation and an exposed delete command. <br>
Mitigation: Treat delete as a destructive action, require explicit confirmation, and clarify or remove the delete capability before relying on the skill as posting-only. <br>
Risk: The skill depends on LinkedIn OAuth credentials and access tokens stored in a local configuration file. <br>
Mitigation: Store credentials with restricted file permissions and review the granted LinkedIn permissions before authenticating. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xmythril/linkedin-cli-2) <br>
- [linkedin-cli Project Homepage](https://github.com/0xmythril/linkedin-cli) <br>
- [LinkedIn Developer Apps](https://www.linkedin.com/developers/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires linkedin-cli and LinkedIn OAuth credentials; posting, sharing, and deletion actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
