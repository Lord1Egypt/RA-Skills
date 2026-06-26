## Description: <br>
Helps agents manage Multilogin X browser profiles, including launching quick disposable profiles, listing, starting, and stopping saved profiles, and checking launcher status with the xcli CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MultiloginCom](https://clawhub.ai/user/MultiloginCom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to install Multilogin X command-line tools, start the launcher, authenticate, and manage headless or desktop browser profiles for automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Multilogin account credentials and browser profiles. <br>
Mitigation: Use a dedicated low-privilege account, avoid putting passwords in prompts or command lines, and clear or revoke local xcli tokens on shared machines. <br>
Risk: The skill installs and runs external Multilogin binaries. <br>
Mitigation: Install only from trusted Multilogin sources and verify downloaded binaries where possible before allowing an agent to run them. <br>
Risk: Credential passing across delegated node sessions can expose secrets. <br>
Mitigation: Do not send credentials through sessions_spawn messages; provide credentials through a secure local channel on the target machine. <br>
Risk: A running launcher can keep browser automation available after the task is complete. <br>
Mitigation: Stop the launcher when finished and review active profiles before leaving shared or unattended systems. <br>


## Reference(s): <br>
- [ClawHub Multilogin X Skill](https://clawhub.ai/MultiloginCom/multiloginx) <br>
- [Multilogin X CLI Latest Version Endpoint](https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest) <br>
- [Multilogin X Launcher Latest Version Endpoint](https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires xcli and mlx-launcher; commands may depend on local OS, launcher state, credentials, and active Multilogin profile state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
