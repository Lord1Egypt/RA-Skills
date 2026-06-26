## Description: <br>
Starts a temporary remote browser session so a user can complete visual login and persist cookies and localStorage for later Playwright automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelLod](https://clawhub.ai/user/MichaelLod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill on headless servers when a website requires manual visual login before authenticated browsing or automation. It opens a browser through a temporary public URL, then saves session state for later Playwright use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes an authenticated browser session through a public tunnel with broad remote-control capabilities. <br>
Mitigation: Use only in a trusted environment, share the tunnel URL only with the intended user, and close the tunnel immediately after login. <br>
Risk: Saved session files contain authentication cookies and localStorage that can grant account access. <br>
Mitigation: Treat saved session state as sensitive, avoid sensitive accounts when possible, and delete saved session data when it is no longer needed. <br>
Risk: Remote-control endpoints can interact with pages beyond simple login flows. <br>
Mitigation: Prefer a version that binds to localhost, requires a strong access token, and removes general remote-control endpoints before use in higher-trust environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MichaelLod/lock-me-in) <br>
- [cloudflared release download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the script can write Playwright storage state and session metadata files to disk.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
