## Description: <br>
Knowledge Card Factory automates topic discovery, content research, AI image and card creation, and publishing for social-media knowledge cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, knowledge workers, and teams use this skill to turn topics or trends into researched knowledge cards, captions, draft assets, and optional social posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated research, captions, or card copy may be inaccurate, incomplete, or misleading. <br>
Mitigation: Keep user review enabled and verify the card, caption, tags, and cited source material before publishing. <br>
Risk: Publishing automation can post content to external social platforms with account or brand impact. <br>
Mitigation: Use a sandbox or low-risk account first, keep require_confirmation enabled, and avoid unattended scheduled or multi-channel publishing without review and rollback controls. <br>
Risk: The workflow can scrape or reuse third-party platform content and generated images. <br>
Mitigation: Restrict source platforms to content the user is allowed to reuse and review image provenance, attribution, and platform policy requirements before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/knowledge-card-factory) <br>
- [brave-search dependency](https://clawhub.ai/brave-search) <br>
- [agent-reach dependency](https://clawhub.ai/agent-reach) <br>
- [nano-banana-pro dependency](https://clawhub.ai/nano-banana-pro) <br>
- [xiaohongshu-mcp dependency](https://clawhub.ai/xiaohongshu-mcp) <br>
- [card-renderer optional dependency](https://clawhub.ai/card-renderer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with workflow configuration, generated card assets, captions, tags, and publishing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default workflow keeps auto_publish false and require_confirmation true; failed publishing is saved as a local draft.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
