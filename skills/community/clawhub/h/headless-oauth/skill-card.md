## Description: <br>
Authorize OAuth CLI tools on a headless server where the agent and user are on separate machines, using pasted redirects, device flow, or manual callback relay patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorivanter](https://clawhub.ai/user/igorivanter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to complete OAuth authorization for command-line tools running on VPS or headless servers. It helps agents explain the remote/local browser split, collect user-provided codes or redirect URLs, and relay callbacks to the expected local endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth codes, redirect URLs, tokens, and keyring passwords can grant account access if exposed. <br>
Mitigation: Treat them as secrets, relay redirect URLs only to the expected localhost callback, and avoid placing credentials in shell history, persistent environment variables, or startup files. <br>
Risk: A manual callback relay can send an authorization response to the wrong local endpoint if the URL is not checked. <br>
Mitigation: Prefer device-flow login when available and verify the localhost host, port, path, code, and state before running relay commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorivanter/headless-oauth) <br>
- [Project homepage](https://github.com/IgorIvanter/headless-oauth) <br>
- [gog CLI documentation](https://github.com/steipete/gogcli) <br>
- [GitHub device login](https://github.com/login/device) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; output may include OAuth URLs, one-time codes, redirect URLs, and localhost callback relay commands.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
