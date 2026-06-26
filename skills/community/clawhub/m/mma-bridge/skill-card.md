## Description: <br>
Uses the mma-bridge command-line tool to interact with Meteor Master AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mordom0404](https://clawhub.ai/user/mordom0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced Meteor Master AI users use this skill to check or start the desktop app, discover local MMA Bridge instances, and send supported API requests for meteor-analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-changing API methods can delete meteor detection groups or change favorites. <br>
Mitigation: Review the mma post method and item IDs before execution, especially for bulk operations, and use lookup methods such as getDataList or getDataDetail to confirm the target records. <br>
Risk: Request payload files can include local paths or record identifiers that affect the wrong media, export, or result set. <br>
Mitigation: Use temporary payload filenames with only the needed JSON fields, verify paths and IDs before running commands, and remove temporary payload files when finished. <br>
Risk: Multiple local Meteor Master AI instances can be running on different ports. <br>
Mitigation: Run mma list first and pass the intended port explicitly when there is more than one active instance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mordom0404/mma-bridge) <br>
- [MMA Bridge API Specification](references/api_spec.md) <br>
- [Current Information API](references/getCurrentInfo.md) <br>
- [Data List API](references/getDataList.md) <br>
- [Data Detail API](references/getDataDetail.md) <br>
- [Delete Group API](references/deleteGroup.md) <br>
- [Collect API](references/collect.md) <br>
- [Uncollect API](references/incollect.md) <br>
- [Analyze Video File API](references/analyzeVideoFile.md) <br>
- [Analyze Image Folder API](references/analyzeImageFolder.md) <br>
- [Analyze Live Stream API](references/analyzeLiveStream.md) <br>
- [Microsoft Store Listing for Meteor Master AI](https://apps.microsoft.com/detail/9pksmkz7c10n) <br>
- [Apple App Store Listing for Meteor Master AI](https://apps.apple.com/cn/app/meteor-master-ai-%E5%BF%AB%E9%80%9F%E6%89%BE%E5%87%BA%E6%B5%81%E6%98%9F/id6458742068?mt=12) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a local Meteor Master AI instance through mma-bridge and may include request payload files.] <br>

## Skill Version(s): <br>
1.2.7 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
