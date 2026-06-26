## Description: <br>
OpenClaw 文档知识库 - 搜索与同步 / OpenClaw Documentation Knowledge Base - Search & Sync <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sushengbuyu](https://clawhub.ai/user/sushengbuyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the bundled OpenClaw documentation index, browse documentation categories, and optionally sync updated OpenClaw docs from the official documentation site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync command fetches remote documentation and can write documentation content outside the intended docs folder according to the security evidence. <br>
Mitigation: Prefer the bundled search index, and run sync only after path validation is fixed or in a constrained workspace where unintended writes can be reviewed. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/sushengbuyu/openclaw-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; search commands return text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes category filters, result limits, search scores, summaries, and matched documentation paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
