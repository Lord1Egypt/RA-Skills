## Description: <br>
使用灵雀AI设计产品推广海报、信息图和PPT页面，根据用户提供的文字描述和图片素材调用灵雀AI生成营销海报、信息图和PPT页面。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujiang-web](https://clawhub.ai/user/lujiang-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to turn product, campaign, brand, or presentation requirements into design prompts and generated poster, infographic, or PPT-page image outputs through Lingque AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Lingque account passwords and stores the saved password with reversible obfuscation. <br>
Mitigation: Use a dedicated Lingque account, avoid reusing important passwords, prefer environment variables when possible, and delete or protect config.json after use. <br>
Risk: The skill may ask for SMS verification codes during registration or login. <br>
Mitigation: Complete login directly when possible and avoid sharing SMS codes with an agent unless the user has explicitly accepted that workflow. <br>
Risk: Design prompts and image URLs are sent to Lingque/Pinza external services. <br>
Mitigation: Do not submit confidential prompts, unreleased product details, or private image assets unless external processing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lujiang-web/poster-ppt-designer) <br>
- [Lingque AI](https://lqai.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request data and shell command examples; runtime scripts return generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Lingque account credentials and optional logo image URLs.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
