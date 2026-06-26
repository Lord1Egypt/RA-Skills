## Description: <br>
Use this skill to inspect ngrok endpoints, reserved domains, tunnel sessions, and online tunnels through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve ngrok account data such as active endpoints, reserved domains, online tunnel sessions, and online tunnels without calling the ngrok API directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected ngrok account and can query account data. <br>
Mitigation: Install and use it only when the user is comfortable allowing the oo CLI to query the connected ngrok account. <br>
Risk: Setup, billing, write, or destructive actions could have account-level effects if introduced or requested. <br>
Mitigation: Confirm those actions and their expected effects with the user before running them. <br>
Risk: Using the skill for general ngrok discussion may unnecessarily involve account-connected tooling. <br>
Mitigation: Use the skill only for ngrok tasks that require account data or connector actions. <br>


## Reference(s): <br>
- [ClawHub ngrok Skill](https://clawhub.ai/oomol/oo-ngrok) <br>
- [ngrok Homepage](https://ngrok.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return read-oriented ngrok account data when connector actions are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
