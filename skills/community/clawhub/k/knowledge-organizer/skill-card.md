## Description:

Use when importing articles, organizing notes, or syncing a knowledge base across Obsidian, Feishu, and Tencent IMA with OpenClaw or Codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjke84](https://clawhub.ai/user/cjke84)

### License/Terms of Use:

MIT

## Use Case:

Developers, knowledge workers, and teams use this skill to import articles, drafts, and links into structured knowledge-base notes with duplicate checks, tags, summaries, related-note suggestions, and optional sync to Obsidian, Feishu, or Tencent IMA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad image and sync handling that can affect a user's knowledge base.

Mitigation: Review before installing, start with a test vault and dry-run, and restrict the agent to the intended vault path and trusted image sources.

Risk: Custom Feishu or IMA endpoints could route content to unintended services.

Mitigation: Keep custom endpoints unset unless they are controlled and verify destination credentials and routing before live sync.

Risk: Drafts from untrusted sources may introduce unwanted content into notes or sync targets.

Mitigation: Avoid importing untrusted drafts and review generated summaries, tags, and duplicate decisions before committing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjke84/skills/knowledge-organizer)
- [Project homepage](https://github.com/cjke84/knowledge-organizer)
- [WeChat import workflow](references/wechat-import.md)
- [Xiaohongshu import workflow](references/xiaohongshu-import.md)
- [IMA import workflow](references/ima-import.md)
- [Feishu import workflow](references/feishu-import.md)
- [Tag system](references/tag-system.md)
- [Tencent IMA import_doc API](https://ima.qq.com/openapi/note/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, structured import results, CLI commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Obsidian-ready Markdown files or produce SyncStateRecord-backed Feishu/IMA import results when configured.]

## Skill Version(s):

0.1.2 (source: frontmatter, manifest.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
