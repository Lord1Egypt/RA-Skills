## Description: <br>
Use when importing articles, organizing notes, or syncing a knowledge base across Obsidian, Feishu, and Tencent IMA with OpenClaw or Codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjke84](https://clawhub.ai/user/cjke84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, knowledge workers, and teams use this skill to turn article links, drafts, and notes into structured Markdown, check duplicates, apply tags and summaries, and write or sync selected content to Obsidian, Feishu, or Tencent IMA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read selected knowledge-base folders and write notes or assets under the configured vault. <br>
Mitigation: Scope OPENCLAW_KB_ROOT to the intended vault and review generated notes before relying on them. <br>
Risk: Selected note content can be uploaded to Feishu or Tencent IMA when those sync destinations are configured. <br>
Mitigation: Provide Feishu access and IMA credentials only for intended sync workflows and verify the destination before upload. <br>
Risk: Custom transport endpoint settings can redirect Feishu sync traffic. <br>
Mitigation: Leave FEISHU_IMPORT_ENDPOINT unset unless the endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cjke84/knowledge-organizer) <br>
- [Project Homepage](https://github.com/cjke84/knowledge-organizer) <br>
- [Feishu Import (OpenClaw Plugin)](references/feishu-import.md) <br>
- [Tencent IMA Import (OpenAPI)](references/ima-import.md) <br>
- [Knowledge Base Tag System](references/tag-system.md) <br>
- [WeChat Article Import](references/wechat-import.md) <br>
- [Xiaohongshu Note Import](references/xiaohongshu-import.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, shell commands, and configuration guidance for knowledge-base import and sync workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write Obsidian-ready Markdown files and prepare Feishu or Tencent IMA sync payloads when configured.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
