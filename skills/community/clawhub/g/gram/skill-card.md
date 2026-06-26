## Description: <br>
Instagram CLI for viewing feeds, posts, profiles, and engagement via cookies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Instagram CLI commands and configuration guidance for viewing feeds, posts, profiles, comments, followers, search results, and account engagement through the gram CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gram CLI uses Instagram session cookies and browser cookie profiles, which can expose account access if mishandled. <br>
Mitigation: Treat sessionid, csrftoken, ds_user_id, and browser cookie profiles like passwords; avoid saving them in shared config files or shell history. <br>
Risk: The CLI can change account state through actions such as like, comment, save, follow, and unfollow. <br>
Mitigation: Require an explicit user request before proposing or running account-changing commands. <br>
Risk: The skill depends on the third-party npm package @cyberdrk/gram handling Instagram session data. <br>
Mitigation: Install and run the package only when the user trusts the package with their Instagram session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arein/gram) <br>
- [gram GitHub repository](https://github.com/arein/gram) <br>
- [npm package @cyberdrk/gram](https://www.npmjs.com/package/@cyberdrk/gram) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output options and browser cookie authentication guidance for the gram CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
