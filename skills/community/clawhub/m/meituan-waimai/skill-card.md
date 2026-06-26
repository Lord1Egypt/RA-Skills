## Description: <br>
美团外卖 helps users authenticate with a Meituan account, claim eligible Meituan coupon benefits, and query coupon claim history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to complete Meituan SMS login, claim available coupon benefits, and review prior coupon claim records through an agent-guided workflow. <br>

### Deployment Geography for Use: <br>
Global, subject to Meituan account and service availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Meituan login tokens, masked phone data, coupon history, and a persistent device identifier stored on the user's device. <br>
Mitigation: Install only if the publisher is trusted, use isolated XIAOMEI_AUTH_FILE and XIAOMEI_COUPON_HISTORY_FILE paths when needed, and use logout or clear-device-token when finished. <br>
Risk: Broad coupon-related prompts may activate the skill and lead to account or coupon actions the user did not intend. <br>
Mitigation: Confirm the user's intent before starting login, coupon claiming, or history lookup flows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/meituan-openplatform/meituan-waimai) <br>
- [Publisher Profile](https://clawhub.ai/user/meituan-openplatform) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Python script calls for login, coupon claiming, logout, device-token clearing, and coupon history lookup.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
