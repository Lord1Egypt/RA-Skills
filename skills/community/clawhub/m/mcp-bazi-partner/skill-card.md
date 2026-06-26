## Description: <br>
Chinese BaZi (Four Pillars of Destiny) analysis and AI partner matching for users asking about 八字, 命理, 四柱, birth chart analysis, or AI companion matching based on birth date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoezoecookie](https://clawhub.ai/user/zoezoecookie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw or Claude Code users use this MCP skill to analyze a provided birth date, compute BaZi pattern details, match an AI partner persona, and optionally write that persona prompt into OpenClaw's SOUL.md after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change the assistant's future persona by writing to OpenClaw's SOUL.md file. <br>
Mitigation: Use bazi_apply_prompt only after reviewing the exact prompt text and target path, and keep a backup or be ready to remove the marked bazi-partner section from SOUL.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoezoecookie/mcp-bazi-partner) <br>
- [Project homepage](https://github.com/ZoezoeCookie/mcp-bazi-partner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON tool responses and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a marked bazi-partner section to OpenClaw SOUL.md only through the apply prompt tool.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
