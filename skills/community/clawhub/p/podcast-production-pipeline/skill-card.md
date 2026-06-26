## Description: <br>
End-to-end podcast production automation for topic and guest research, episode outlines, show notes, SEO descriptions, social promotion materials, and Chinese platform publishing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Podcast creators, production teams, and content operators use this skill to prepare interview episodes and generate publication assets after recording. It creates research notes, outlines, show notes, SEO descriptions, social posts, and highlight drafts for international and Chinese podcast platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports exposed credentials in the bundled configuration. <br>
Mitigation: Replace bundled API keys and tokens with securely managed credentials before installation or execution. <br>
Risk: The security review reports automatic workflow metadata delivery through an authenticated Discord gateway path that is not clearly disclosed. <br>
Mitigation: Review and disable or reconfigure Discord posting before running the pre-production workflow. <br>
Risk: Episode topics, guest names, transcripts, and generated publication copy may contain sensitive or unverified content. <br>
Mitigation: Use non-sensitive inputs unless external transmission is acceptable, and treat generated notes, descriptions, and social posts as drafts requiring human review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/podcast-production-pipeline) <br>
- [Use Case Source](https://github.com/AlexAnys/awesome-openclaw-usecases-zh/blob/main/usecases/podcast-production-pipeline.md) <br>
- [Xiaoyuzhou Creator Platform](https://podcaster.xiaoyuzhoufm.com/) <br>
- [Ximalaya Creator Center](https://zhubo.ximalaya.com/) <br>
- [Whisper](https://github.com/openai/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration] <br>
**Output Format:** [Markdown files, text templates, and command-line workflow output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes episode preparation and publication files under the configured podcast storage path.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
