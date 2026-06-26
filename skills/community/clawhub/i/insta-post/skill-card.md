## Description: <br>
Uploads Instagram posts through browser automation, including image upload, caption entry, optional collaborator tagging, and sharing through an active Instagram session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, social media operators, and agents use this skill to prepare and publish Instagram image posts from local JPG files in a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real posts to the currently logged-in Instagram account. <br>
Mitigation: Before each run, verify the target account, media paths, caption, and collaborators, and do not allow unattended posting. <br>
Risk: Browser automation can act on the wrong tab or stale Instagram UI state. <br>
Mitigation: Confirm the active Instagram tab before publishing and verify the final shared-post confirmation in the browser. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/insta-post) <br>
- [Instagram](https://www.instagram.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled script emits JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Instagram browser session and local image paths; use may publish real posts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
