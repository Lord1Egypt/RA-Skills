## Description: <br>
Givebutter connector helper for searching and reading campaigns, chapters, contacts, funds, recurring plans, and transactions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when a Givebutter task requires reading campaign, chapter, contact, fund, recurring plan, or transaction data through the oo CLI. The skill guides agents to inspect the live connector schema before constructing action payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Givebutter accounts may expose donor, contact, campaign, recurring plan, and transaction records. <br>
Mitigation: Install and use the skill only if OOMOL is trusted, and keep use to the documented read-only get and list actions unless a future release clearly documents additional operations. <br>
Risk: CLI actions can fail when the oo CLI is missing, the user is not signed in, the Givebutter connection is expired or missing scopes, or OOMOL billing blocks execution. <br>
Mitigation: Use the documented setup, login, connection, or billing recovery step only after the matching command failure occurs. <br>


## Reference(s): <br>
- [Givebutter homepage](https://givebutter.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub Givebutter skill page](https://clawhub.ai/oomol/skills/oo-givebutter) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payload conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector action responses are returned as JSON when the generated oo CLI command uses --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
