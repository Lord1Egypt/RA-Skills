## Description: <br>
Feathery lets an agent operate an OOMOL-connected Feathery account to read account, form, user, session, submission, and hidden-field data and to perform approved writes or deletes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting teams that use Feathery can inspect form and account data and, with confirmation, manage users, hidden fields, and submissions through an OOMOL-connected Feathery account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Feathery users, hidden fields, and submissions. <br>
Mitigation: Confirm the exact payload and intended effect before write actions, and require explicit approval before destructive actions. <br>
Risk: The skill depends on the oo CLI and an OOMOL-connected Feathery account, including a remote installer for first-time setup. <br>
Mitigation: Install and authenticate oo only when needed, and run the installer only when the user trusts OOMOL and needs the connector. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-feathery) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Feathery homepage](https://www.feathery.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Feathery account, form, user, session, hidden field, or submission data from connected OOMOL actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
