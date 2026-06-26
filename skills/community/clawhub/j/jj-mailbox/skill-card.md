## Description: <br>
Jj Mailbox lets AI agents send and receive messages through a jj (Jujutsu) version-controlled file-based mailbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MiaoDX](https://clawhub.ai/user/MiaoDX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up and operate a shared jj-backed mailbox so agents can exchange messages, status, and shared artifacts across local or remote repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox contents can be pushed to a configured git remote during opt-in sync, which can expose secrets or sensitive data placed in the mailbox repo. <br>
Mitigation: Do not store secrets, credentials, or sensitive data in the mailbox repo; use least-privileged git or SSH credentials and sync only to trusted remotes. <br>
Risk: Repository-maintenance commands can create commits, move message files, and run fetch or push operations. <br>
Mitigation: Review high-impact commands before running them and keep sync under explicit user control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MiaoDX/jj-mailbox) <br>
- [Jujutsu installation documentation](https://jj-vcs.dev/docs/install/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON mailbox files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jj-mailbox, jj, git, and python3; optional sync uses the host's configured git or SSH credentials.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
