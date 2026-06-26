## Description: <br>
MiniMax Monitor helps users track MiniMax API package quota, rate probe results, weekly usage, and 24-hour usage history through a local dashboard and optional Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MiniMax API users use this skill to monitor package quota consumption, reset timing, weekly limits, rate probe results, and optional Feishu quota summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local service uses MiniMax credentials and can act as a credential-using proxy. <br>
Mitigation: Install only after reviewing the local service behavior and use the default configuration unless header key passthrough is explicitly needed. <br>
Risk: Rate probes can make billable MiniMax inference requests. <br>
Mitigation: Start the service with probes disabled unless billable performance testing is intentional. <br>
Risk: The browser remember option can retain credentials on shared machines. <br>
Mitigation: Avoid the 24-hour remember option on shared or untrusted computers. <br>
Risk: Optional Feishu notifications can send quota results to the wrong chat if configured incorrectly. <br>
Mitigation: Use the Feishu script only after confirming the target chat and credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/minimax-monitor) <br>
- [README](artifact/README.md) <br>
- [Chinese README](artifact/README_zh.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [MiniMax token plan endpoint](https://www.minimaxi.com/v1/token_plan/remains) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and dashboard usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local Node.js service, open an HTML dashboard, and optionally send quota summaries to Feishu.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
