## Description: <br>
Monitor DX clusters for rare station spots, track active DX expeditions, and get daily band activity digests for amateur radio operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amateur radio operators use this skill to check live DX cluster spots, identify rare stations or expeditions, and generate daily band-activity digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor contacts DX cluster servers and may send the configured callsign during login. <br>
Mitigation: Use the skill only when network access to DX clusters and callsign sharing are intended. <br>
Risk: Optional cron entries can run ongoing background monitoring and create local logs or state files. <br>
Mitigation: Enable cron entries deliberately, review the generated logs and state file, and remove them when monitoring is no longer needed. <br>
Risk: The README references a setup script that is not included in the artifact. <br>
Mitigation: Do not run setup scripts from outside the package unless they are inspected separately. <br>


## Reference(s): <br>
- [NG3K Amateur Radio DX Peditions](https://www.ng3k.com/misc/adxo.html) <br>
- [DX-World](https://www.dx-world.net/) <br>
- [425 DX News](http://www.425dxn.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with optional shell commands and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local log and state files when cron-based monitoring is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
