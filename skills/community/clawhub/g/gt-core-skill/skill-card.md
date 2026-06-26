## Description: <br>
Use this skill when the user needs to work with Gumtree in a real Chrome browser session, using a local Python CLI and Chrome extension bridge for login, search, listing, favourite, messaging, and post-ad category-flow tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluebluebbb](https://clawhub.ai/user/bluebluebbb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Gumtree through a real Chrome session for login checks, searches, listing review, favourites, messages, and starting post-ad category selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local bridge and Chrome extension can control a logged-in Gumtree browser session. <br>
Mitigation: Install only from a trusted publisher, keep the extension disabled when not in active use, and review each account action before running it. <br>
Risk: The skill can perform real Gumtree account actions, including login, logout, favouriting, messaging, and post-ad category selection. <br>
Mitigation: Treat command output as confirmation of real account activity and avoid running message, favourite, or post-ad flows without explicit user intent. <br>
Risk: Passing passwords through command-line arguments can expose credentials in shell history or process listings. <br>
Mitigation: Avoid unnecessary credential repetition and prefer a fresh, trusted local terminal session when login is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bluebluebbb/gt-core-skill) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local Chrome, uv, and an active browser extension connected to the local bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
