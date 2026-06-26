## Description: <br>
商品价格监控工具。监控电商商品价格变化，价格低于阈值时发送通知。适合购物党、羊毛党。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage command-line product price watches, set target prices, and check locally stored monitor entries for supported ecommerce URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores monitored product URLs and thresholds in a local file. <br>
Mitigation: Review ~/.price-monitor.json contents and local file permissions before using the skill with sensitive shopping data. <br>
Risk: Price checks and alert behavior are prototype-level and may not reflect real marketplace prices or notifications. <br>
Mitigation: Verify or replace the simulated price and notification code before relying on the skill for purchase decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/price-alert-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text with command-line usage examples and local JSON state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and stores monitored product URLs and thresholds in ~/.price-monitor.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
