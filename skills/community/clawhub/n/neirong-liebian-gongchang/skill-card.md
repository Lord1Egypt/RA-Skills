## Description: <br>
小红书热点追踪、爆文生成、知识卡片和公众号发布的全链路自动化技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and public-account editors use this skill to collect trending topics, analyze content angles, generate long-form article drafts and knowledge cards, and archive results to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend data, generated article text, and card links may be sent to the configured Feishu workspace. <br>
Mitigation: Use draft mode for review, restrict the Feishu bot to the intended folder, and confirm the archive destination before scheduled runs. <br>
Risk: The workflow depends on other skills and platform permissions for trend collection, card rendering, article generation, and Feishu publishing. <br>
Mitigation: Verify dependent skill permissions and configurations before enabling automated or scheduled runs. <br>
Risk: Generated content can be inaccurate, insufficiently original, or unsuitable for platform rules. <br>
Mitigation: Review and edit outputs before publication, and follow the target platform's content and copyright requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/neirong-liebian-gongchang) <br>
- [Artifact README](artifact/README.md) <br>
- [Workflow configuration](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown article drafts, structured analysis text, generated card links, Feishu document links, and workflow configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or link Feishu documents when draft mode is disabled; draft mode returns generated content without publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
