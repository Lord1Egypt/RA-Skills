## Description: <br>
小佩宠物设备监控 - 获取喂食器、猫砂盆、饮水机、净化器状态 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners and operators use this skill to check PETKIT smart feeders, litter boxes, water fountains, and air purifiers from an agent session. It reports device status such as food level, daily feeding totals, water level, filter state, and online presence after authenticating with a PETKIT account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships with populated plaintext PETKIT credentials and the script saves credentials locally without protection. <br>
Mitigation: Remove bundled credentials before use, rotate the exposed password if it belongs to a real account, and prefer runtime prompts or OS keychain storage for credentials. <br>
Risk: Using the skill may log the PETKIT mobile app out of the same account. <br>
Mitigation: Use a shared or secondary PETKIT account where possible and warn users before login. <br>
Risk: The skill depends on a reverse-engineered PETKIT API that may change without notice. <br>
Mitigation: Pin and review the petkitaio dependency, test the skill before operational use, and treat failed or missing device readings as stale until verified in the official app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/petkit-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like terminal text with status lines and configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PETKIT account credentials and the petkitaio Python dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
