## Description: <br>
PKU Info Spider helps agents work on a Rust CLI for crawling WeChat Official Account articles, including QR login, account search, article fetching, and article-to-Markdown conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when maintaining or debugging the info-spider CLI, especially its WeChat QR login flow, account search, article fetching, and Markdown scraping workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat MP session files can contain sensitive token, fingerprint, or bizuin values. <br>
Mitigation: Treat ~/.config/info-spider/ and related logs as sensitive, avoid sharing session data, and clear sessions with logout when work is complete. <br>
Risk: Scraping WeChat Official Account content may be restricted by platform terms or local rules. <br>
Mitigation: Use scraping features only where allowed, review the applicable terms before collecting content, and keep crawler behavior within permitted limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjsoj/pku-info-spider) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and command examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference info-spider CLI options and local session/configuration paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
