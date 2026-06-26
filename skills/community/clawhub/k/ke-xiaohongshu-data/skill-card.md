## Description: <br>
Collects Xiaohongshu public-data examples for note metrics, creator analysis, search monitoring, and competitive content analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoheizp](https://clawhub.ai/user/xiaoheizp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, brand teams, MCN operators, and creators can use this skill to prepare Xiaohongshu public-data reports for note performance, creator profile review, trend monitoring, and competitor analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests a Xiaohongshu session cookie, which may expose account access if shared with an untrusted release. <br>
Mitigation: Use a low-privilege account where possible, avoid providing a main account cookie, rotate the cookie after use, and install only after verifying the publisher and credential handling. <br>
Risk: The included script appears to produce demo output rather than a fully auditable real scraper. <br>
Mitigation: Treat generated reports as sample or unverified data until the implementation is reviewed against real collection behavior. <br>
Risk: Exported creator profile or contact information may create platform, privacy, or downstream sharing obligations. <br>
Mitigation: Limit exports to necessary public fields and review Xiaohongshu platform rules and applicable privacy requirements before sharing or commercial use. <br>
Risk: Automated collection can create account or platform risk if used with high request volume. <br>
Mitigation: Use conservative limits and delays, avoid high-frequency collection, and stop collection if the platform signals rate limiting or access restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoheizp/ke-xiaohongshu-data) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoheizp) <br>
- [Xiaohongshu website](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Markdown tables, shell command examples, and environment-variable configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires or benefits from XIAOHONGSHU_COOKIE for authenticated collection; included artifact behavior produces demo data and Markdown exports.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
