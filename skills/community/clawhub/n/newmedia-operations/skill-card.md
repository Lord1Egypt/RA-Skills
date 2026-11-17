## Description:

Provides an end-to-end workflow for Chinese social media operations, including industry analysis, competitor monitoring, account nurturing, viral content creation, engagement hook design, and optional data collection for Douyin, Xiaohongshu, WeChat Video, Weibo, and related channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swcxy12315](https://clawhub.ai/user/swcxy12315)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, marketers, and developers use this skill to plan and execute social media operations for Chinese content platforms. It helps prepare industry and competitor analysis, account setup guidance, content ideas, engagement prompts, monitoring workflows, and report outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in browser or account control may be delegated to external tools.

Mitigation: Use a dedicated low-privilege browser profile and require explicit approval before every live post, account action, or publishing step.

Risk: Bundled collector outputs may be synthetic sample data presented as platform collection.

Mitigation: Treat collector output as demo data unless real collection provenance is available and verified.

Risk: External OpenCLI and ima-skill downloads are outside the artifact.

Mitigation: Verify download sources and installation contents before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/swcxy12315/skills/newmedia-operations)
- [Industry Analysis Guide](references/INDUSTRY_ANALYSIS.md)
- [Competitor Analysis Guide](references/COMPETITOR_ANALYSIS.md)
- [Account Nurturing Guide](references/ACCOUNT_NURTURING.md)
- [Viral Content Guide](references/VIRAL_CONTENT.md)
- [Engagement Hooks Guide](references/ENGAGEMENT_HOOKS.md)
- [IMA Knowledge Integration Guide](references/IMA_KNOWLEDGE.md)
- [OpenCLI Integration Guide](references/OPENCLI.md)
- [OpenCLI Repository](https://github.com/jackwener/opencli)
- [IMA Agent Interface](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and report templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform-specific operating plans, content calendars, competitor summaries, data collection commands, and locally generated JSON or Markdown reports.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
