## Description: <br>
Run browser operations and untrusted code in a secure PPIO cloud sandbox (Firecracker VM). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piston4711](https://clawhub.ai/user/piston4711) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to browse external sites, run unfamiliar build or test commands, and execute untrusted code inside an isolated PPIO cloud sandbox instead of the local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload arbitrary local files to a third-party cloud sandbox. <br>
Mitigation: Do not upload secrets, credentials, SSH keys, private code, personal configuration, or workspace files unless the transfer is intentional. <br>
Risk: The skill can download sandbox files to local paths and may overwrite existing local files. <br>
Mitigation: Use explicit destination paths, avoid existing files, and inspect downloaded artifacts before relying on them. <br>
Risk: Paused sandboxes can preserve files, browser sessions, and login state while using a billable cloud VM. <br>
Mitigation: Kill sandboxes after completing work, especially after login-based browsing or sensitive execution. <br>


## Reference(s): <br>
- [PPIO Sandbox: Browser Use Integration](references/browser-use.md) <br>
- [PPIO Sandbox Browser Use Documentation](https://ppio.com/docs/sandbox/integrate-browser-use) <br>
- [ClawHub Release Page](https://clawhub.ai/piston4711/ppio-sandbox) <br>
- [Publisher Profile](https://clawhub.ai/user/piston4711) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sandbox commands return JSON status, stdout, stderr, and exit codes where applicable.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
