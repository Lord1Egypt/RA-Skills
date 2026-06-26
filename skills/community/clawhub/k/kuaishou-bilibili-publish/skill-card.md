## Description: <br>
Automates browser-based video uploads, cover setup, metadata entry, and publishing for Kuaishou, Bilibili, and Douyin creator platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohei2022](https://clawhub.ai/user/xiaohei2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to publish videos from a TXT configuration file to Kuaishou, Bilibili, and Douyin through an authenticated Chrome browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload and publish to live social accounts. <br>
Mitigation: Start with --no-publish and test accounts, then review the content and target account before enabling live publish-all. <br>
Risk: The skill uses stealth-style browser fingerprint changes that may violate platform rules. <br>
Mitigation: Confirm the target platforms' automation rules before use and avoid running debug scripts on sensitive browser sessions. <br>
Risk: Unpinned dependencies can change the runtime behavior over time. <br>
Mitigation: Pin dependencies before operational use and review updates before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohei2022/kuaishou-bilibili-publish) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Test report](artifact/TEST_REPORT.md) <br>
- [Kuaishou Creator Platform](https://cp.kuaishou.com/) <br>
- [Bilibili video upload page](https://member.bilibili.com/platform/upload/video/frame) <br>
- [Douyin creator upload page](https://creator.douyin.com/creator-micro/content/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, TXT configuration examples, and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Chrome session authenticated to the target creator platforms; --no-publish can fill forms without clicking publish.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
