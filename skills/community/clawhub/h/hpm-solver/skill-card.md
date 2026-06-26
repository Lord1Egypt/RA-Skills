## Description: <br>
HPM Solver calculates Harry Potter: Magic Awakened purchase combinations using food and plant price coefficients, equivalent item grouping, filtering, and replacement restoration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xilowei920](https://clawhub.ai/user/xilowei920) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and tool builders use this skill to compute gold or diamond purchase combinations and residual values for Harry Potter: Magic Awakened from local price and quantity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact links to an optional external tar.gz archive whose contents are not established by the reviewed local files. <br>
Mitigation: Use the reviewed files as the basis for deployment; download or run the archive only after separately verifying its contents and trusting the publisher. <br>
Risk: Local price and history fields may store user-entered data. <br>
Mitigation: Do not enter sensitive personal information into local price, quantity, or history fields. <br>
Risk: Solver recommendations depend on local price tables, multipliers, and quantity limits. <br>
Mitigation: Review and update the local HPM price data before relying on purchase-combination results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xilowei920/hpm-solver) <br>
- [Publisher profile](https://clawhub.ai/user/xilowei920) <br>
- [WeChat mini-program archive linked by the artifact](https://astron-claw-media-prod.oss-cn-beijing.aliyuncs.com/astron-claw-media-prod/c76c9c06e5a6429885e66501e8730ef8/hpm-miniprogram-v13.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, code snippets, JSON examples, and local solver outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local price and history data; solver results depend on the provided price coefficients, target currency amounts, and quantity limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
