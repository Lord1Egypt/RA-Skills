## Description: <br>
Pre-build idea validator that checks competition across GitHub, Hacker News, npm, PyPI, and Product Hunt before writing code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product builders use this skill before implementation to estimate whether an idea already has meaningful competition and to receive competitor summaries, a reality_signal score, and differentiation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may overstate its validation capability compared with the included validator behavior. <br>
Mitigation: Treat outputs as preliminary market-research guidance and require human review before changing product direction. <br>
Risk: The setup asks users to install an unpinned external MCP tool. <br>
Mitigation: Pin and review the MCP package version before use, especially in shared or production agent environments. <br>
Risk: Idea text storage and external data flow are not fully documented. <br>
Mitigation: Avoid confidential business ideas until the publisher documents retention, local storage, and external service behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/idea-reality-validator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sunnyhot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, competitor summaries, scoring, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a reality_signal score, top competitors, and differentiation suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
