## Description: <br>
Publishes Toutiao micro-posts with optional images by using a local or headless Chrome browser and Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chellen021](https://clawhub.ai/user/chellen021) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People who manage a Toutiao account can use this skill to publish micro-post text and optional images from a command-line workflow that reuses a local Chrome login session. <br>

### Deployment Geography for Use: <br>
Global, subject to Toutiao account availability and local policy requirements. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly from a logged-in Toutiao account without a final confirmation step. <br>
Mitigation: Run it only when immediate posting is intended, provide explicit post content, and watch the browser during execution. <br>
Risk: Reusing a logged-in Chrome session with remote debugging may expose unrelated browsing context if sensitive tabs or profiles are open. <br>
Mitigation: Use a dedicated Chrome profile, close unrelated sensitive tabs, and enable remote debugging only for the publishing session. <br>
Risk: Running the script without explicit content may post the default bundled message. <br>
Mitigation: Pass reviewed content on the command line or through a file instead of relying on the default content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chellen021/personal-toutiao-pub) <br>
- [Toutiao micro-post publishing page](https://mp.toutiao.com/profile_v4/weitoutiao/publish?from=toutiao_pc) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Command-line guidance and local screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can publish text and optional images, then save success or error screenshots to the user's Desktop.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
