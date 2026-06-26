## Description: <br>
Fireflies (fireflies.ai). Use this skill for ANY Fireflies request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Fireflies through an OOMOL-connected account for transcript, meeting, bite, channel, user, user group, AI app output, and AskFred workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires brokered access to a user's Fireflies account through OOMOL. <br>
Mitigation: Install only when OOMOL is trusted for this account connection and review the connected Fireflies scopes before use. <br>
Risk: Write actions can change Fireflies state, including AskFred threads, bites, user roles, meeting titles, privacy, and channel assignments. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any action marked write. <br>
Risk: Destructive actions can delete Fireflies transcripts or AskFred threads. <br>
Mitigation: Confirm the target identifier and get explicit approval before running any action marked destructive. <br>
Risk: Raw GraphQL requests depend on backend enforcement that is not visible in the local skill text. <br>
Mitigation: Treat raw GraphQL use cautiously and prefer named connector actions when they cover the task. <br>


## Reference(s): <br>
- [ClawHub Fireflies skill page](https://clawhub.ai/oomol/oo-fireflies) <br>
- [Fireflies homepage](https://www.fireflies.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
