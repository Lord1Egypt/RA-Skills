## Description: <br>
Automatically collects, verifies, evaluates, and records pharmaceutical system bidding opportunities from Chinese procurement sites into WeChat Work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ElliotLaw](https://clawhub.ai/user/ElliotLaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales and business development teams use this skill to monitor pharmaceutical system procurement notices, filter viable projects, record bid details, and generate bidding recommendations. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically post procurement and bidding data to WeChat Work messages and smart tables. <br>
Mitigation: Use a test WeChat Work tenant and table first, restrict token permissions, and confirm the destination and fields before enabling production posting. <br>
Risk: Helper and debug paths can expose WeCom secrets in console output or examples. <br>
Mitigation: Remove or mask secret-printing examples and validation output before use, and avoid storing real secrets in committed configuration files. <br>
Risk: Scheduled execution can repeatedly publish incomplete or incorrect bidding records. <br>
Mitigation: Enable the scheduler only after review, monitor logs and table updates, and require human review for bidding recommendations before business action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ElliotLaw/pharmaceutical-bidding) <br>
- [WeChat Work developer documentation](https://developer.work.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notifications, structured bidding records, configuration JSON, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run immediately and on a daily 8:30 AM Asia/Shanghai schedule when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
