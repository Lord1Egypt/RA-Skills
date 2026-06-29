## Description: <br>
追踪 OPC/AI/独立开发者相关赛事活动，从信息源抓取并提取结构化信息，可在用户启用上传后提交到 OPC 公共赛事池。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to track OPC, AI, hackathon, startup, and independent-developer events, extract structured event details, maintain local event records, and optionally submit public event information to the OPC event pool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an OPC API key locally for authenticated queries and optional uploads. <br>
Mitigation: Keep the key in scripts/user_config.json only, do not commit local configuration or generated data files, and rotate the key if it is exposed. <br>
Risk: Uploaded event records become visible in the OPC public event pool. <br>
Mitigation: Leave upload_enabled set to false for local-only tracking, and review event title, summary, organizer, dates, and external URL before enabling submission. <br>
Risk: Tracked sources may include private or confidential event information if a user adds unsuitable sources. <br>
Mitigation: Add only public event sources and avoid sources that contain private, confidential, or access-controlled content. <br>


## Reference(s): <br>
- [OPC API Spec](references/api-spec.md) <br>
- [Platform Event Fetching Spec](references/platform-spec.md) <br>
- [Source Management and Parser Guide](references/sources-mgmt.md) <br>
- [Event Record Templates](references/templates.md) <br>
- [OPC Public Event Pool](https://mrkjai.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/guipi888/opc-event-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown summaries, local JSON and Markdown records, shell command examples, configuration JSON, and OPC API payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate local tracking files under scripts/, query summaries, event tables, and optional authenticated submissions to the OPC public event pool.] <br>

## Skill Version(s): <br>
2.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
