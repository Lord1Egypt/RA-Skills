## Description: <br>
链接收藏夹，保存和整理有用的网页链接 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users can use this skill to save, list, search, and delete useful web links with short descriptions in a local bookmark file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved URLs and descriptions are written to local storage in the skill directory. <br>
Mitigation: Avoid saving confidential internal URLs or sensitive descriptions unless local storage in the skill directory is acceptable. <br>
Risk: Broad Chinese link and save keywords can route unrelated requests to this skill. <br>
Mitigation: Review activation behavior in the target agent and use explicit bookmark-related prompts when saving or searching links. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huangjingzhi07/link-saver) <br>
- [Publisher profile](https://clawhub.ai/user/huangjingzhi07) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Plain text status messages and local JSON bookmark data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores saved URLs, descriptions, and creation timestamps in links.json in the skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
