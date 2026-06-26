## Description: <br>
基于 GMGN 官方 API 的 Meme 币扫链工具。自动扫描热门代币，进行 AI 评分与风险分析，并推送格式化通知。完全使用 GMGN API，数据准确可靠。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanguang254](https://clawhub.ai/user/hanguang254) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to scan SOL and BSC meme tokens, score early trading signals, identify common token risks, and receive formatted token summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses broad local Chrome DevTools access through port 9222. <br>
Mitigation: Run it only with a dedicated Chrome profile, no sensitive logins, and keep port 9222 closed except while scanning. <br>
Risk: The release includes mismatched or under-disclosed behavior, including a legacy Ave.ai script and exposed key. <br>
Mitigation: Review or remove the legacy Ave.ai script and exposed key before installation or execution. <br>
Risk: Hourly cron execution adds persistence and repeated browser-control behavior. <br>
Mitigation: Enable scheduled scanning only after accepting the persistence and browser-control risks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanguang254/meme-scanner) <br>
- [GMGN](https://gmgn.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON array of formatted Markdown notification strings, with setup guidance and shell commands in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans token data through a local Chrome DevTools session and writes a local scanned-token cache to suppress duplicate notifications.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
