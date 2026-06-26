## Description: <br>
Auto-apply JD.com (京东) price protection on all eligible orders by connecting to Chrome via OpenClaw Browser Relay CDP, navigating to the JD price protection page, clicking all "申请价保" buttons, and reporting refund results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Danielwangyy](https://clawhub.ai/user/Danielwangyy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation agents use this skill to check JD.com orders for eligible price-protection refunds, submit applications through a logged-in Chrome session, and receive JSON results for successful and failed claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a Chrome session logged into JD.com and submits price-protection applications for every eligible order it sees. <br>
Mitigation: Run it only when the user intentionally wants those JD.com account actions, and review the JSON result output after execution. <br>
Risk: Cron scheduling can repeat account actions without prompting. <br>
Mitigation: Keep a clear way to disable the scheduled job and review results periodically, especially when running every few hours. <br>


## Reference(s): <br>
- [JD Price Protection portal](https://pcsitepp-fm.jd.com/) <br>
- [ClawHub skill page](https://clawhub.ai/Danielwangyy/jd-price-protect) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime script outputs JSON containing totals, clicked count, page count, successful refunds, and failed claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
