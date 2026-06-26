## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, account checks, and reading, injecting, or running secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up 1Password CLI, authenticate an account, verify access, and use op commands for secret reads, injection, and command execution. It is intended for environments where the agent is allowed to interact with a user's 1Password CLI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples and op commands can print secrets to the terminal or logs. <br>
Mitigation: Avoid commands that print secret values, keep command output out of chat and logs, and prefer op run or op inject with masking where possible. <br>
Risk: Examples can write secrets to ordinary project files such as key files or generated configuration. <br>
Mitigation: Write secrets to disk only when required, use restrictive permissions, keep generated secret files out of git, and delete them immediately after use. <br>
Risk: Giving an agent access to an authenticated 1Password CLI session can expose credentials beyond the immediate task. <br>
Mitigation: Use the skill only in trusted sessions, verify the active account with op whoami before reads, scope commands with --account or OP_ACCOUNT when multiple accounts exist, and close the tmux session when finished. <br>


## Reference(s): <br>
- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/) <br>
- [Local get-started summary](references/get-started.md) <br>
- [Local CLI examples](references/cli-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-1password) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI (op). Normal app-integration flows also require a 1Password subscription, desktop app access, and an unlocked app session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
