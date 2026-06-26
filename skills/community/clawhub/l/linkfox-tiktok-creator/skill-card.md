## Description: <br>
Helps agents use LinkFox-proxied TikTok Shop creator APIs to retrieve creator profiles, shop and showcase products, and manage shoppable video precheck, publishing, and status workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commerce operators, creator-affiliate teams, and agents use this skill to inspect TikTok creator profile and product data, then run controlled shoppable video precheck, publish, and status workflows through LinkFox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and a TikTok creator access token. <br>
Mitigation: Provide credentials only through environment variables or explicit runtime parameters, mask tokens in outputs, and avoid placing secrets in prompts, feedback, or committed files. <br>
Risk: The skill can initiate live TikTok creator workflows, including shoppable video publishing. <br>
Mitigation: Manually confirm every publish and precheck request, verify the target creator account, product, file, title, and region before execution, and review upstream TikTok status responses. <br>
Risk: Persisted response files may contain sensitive creator, product, pricing, or authorization-related data. <br>
Mitigation: Write persisted responses outside repositories, read only the needed fields, and delete response files after use. <br>


## Reference(s): <br>
- [TikTok Creator API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-tiktok-creator) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command invocations for bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist large API responses to local files for later field extraction; those files can contain sensitive creator, product, pricing, or authorization data.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
