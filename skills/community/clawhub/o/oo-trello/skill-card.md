## Description: <br>
Operates Trello through the OOMOL oo CLI for reading, creating, updating, and deleting Trello data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate their Trello boards, lists, cards, labels, members, comments, and checklists through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform write and destructive Trello actions through an authenticated OOMOL connection. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before changing or removing Trello data. <br>
Risk: First-time use may fail if the oo CLI is not installed, the user is not signed in, or Trello is not connected. <br>
Mitigation: Run setup steps only after an auth, connection, or missing-command failure and direct the user to complete the matching OOMOL setup. <br>


## Reference(s): <br>
- [ClawHub Trello skill listing](https://clawhub.ai/oomol/oo-trello) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Trello homepage](https://trello.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for Trello connector actions and confirmation handling; connector responses are JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
