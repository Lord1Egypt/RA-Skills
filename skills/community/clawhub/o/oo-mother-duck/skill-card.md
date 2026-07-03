## Description: <br>
Enables agents to operate MotherDuck through OOMOL's oo CLI connector for organization user, token, account, and Duckling configuration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer MotherDuck organization users, access tokens, active accounts, and Duckling configuration through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer MotherDuck users, tokens, and configuration, including privileged write and destructive actions. <br>
Mitigation: Require explicit user confirmation for write or destructive operations and verify the target user, token, account, or configuration before execution. <br>
Risk: Using the skill in conversations that contain untrusted instructions could lead to unintended account-administration actions. <br>
Mitigation: Avoid using the skill in conversations with untrusted instructions, and inspect the live connector schema before constructing action payloads. <br>
Risk: Security evidence marks the release as suspicious because of broad account-administration and token-management power. <br>
Mitigation: Install only when the user trusts OOMOL and wants an agent to administer the connected MotherDuck organization. <br>


## Reference(s): <br>
- [MotherDuck homepage](https://motherduck.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands invoke the oo CLI and may return JSON connector responses with meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
