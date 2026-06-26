## Description: <br>
Converts and publishes Markdown articles with AI-assisted writing, formatting, humanization, and image generation for WeChat, Zhihu, and Toutiao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiangyu2](https://clawhub.ai/user/shixiangyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developers use this skill to convert Markdown into platform-specific drafts for WeChat, Zhihu, and Toutiao. It can also guide AI-assisted drafting, article rewriting, cover-image generation, and publishing-account configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store or use powerful publishing-account credentials. <br>
Mitigation: Use environment variables or a restricted test account, rotate credentials regularly, and avoid granting more platform access than the workflow needs. <br>
Risk: Drafts, prompts, generated images, CSS, or image URLs may be sent to third-party services. <br>
Mitigation: Avoid confidential drafts, review provider choices before use, and do not use untrusted remote CSS or image URLs. <br>
Risk: Platform actions may create drafts or publish content with limited warnings. <br>
Mitigation: Confirm whether each action creates a private draft or a public post, then review the target platform before final publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shixiangyu2/multi-writing-skills-main) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and CLI commands; generated artifacts may include converted HTML, rewritten Markdown, image files, and platform draft content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require platform credentials and external AI provider keys depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
