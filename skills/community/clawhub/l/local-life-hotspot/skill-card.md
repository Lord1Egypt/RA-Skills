## Description: <br>
Searches same-day trending topics, drafts one in-depth Xiaohongshu post, generates a simple title image, and can publish it automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[githubsoftware2015](https://clawhub.ai/user/githubsoftware2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social media operators use this skill to find current topic candidates, draft structured Xiaohongshu copy, generate a simple cover image, and optionally publish after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated Xiaohongshu content externally, so unreviewed drafts may reach an unintended account or audience. <br>
Mitigation: Keep auto-publish disabled until the generated title, body, image, destination account, and timing have been reviewed. <br>
Risk: The security evidence reports unsafe shell command construction in the publish path using generated or web-sourced text. <br>
Mitigation: Prefer a fixed version that avoids shell-based command construction and clearly declares the permissions it needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/githubsoftware2015/local-life-hotspot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands] <br>
**Output Format:** [Markdown draft with generated image file paths and console status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can call external search services and optionally publish to Xiaohongshu when auto-publish is enabled.] <br>

## Skill Version(s): <br>
6.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
