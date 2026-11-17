## Description: <br>
模型切换工具(免费版) helps individual developers choose between Claude Haiku, Sonnet, and Opus by task complexity to reduce unnecessary API cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual developers use this skill as a quick model-selection guide for personal projects, sub-agent task routing, and scheduled tasks. It recommends starting with lower-cost models for simple work and escalating only for coding, analysis, architecture, or deeper reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports broad read, write, and exec authority for a skill that is primarily a model-selection guide. <br>
Mitigation: Install and run it only in contexts where those permissions are acceptable, and avoid granting file writes, command execution, or API-key handling unless a specific task requires them. <br>
Risk: The security scan notes broad activation language that may cause the skill to run outside narrow model-selection tasks. <br>
Mitigation: Limit use to explicit model switching, cost optimization, sub-agent routing, or scheduled-task model choice requests. <br>
Risk: Model pricing and availability can change after the skill's examples were published. <br>
Mitigation: Check the current provider pricing and available model names before relying on cost comparisons or configuration examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/model-switching-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands, code] <br>
**Output Format:** [Markdown guidance with examples, decision trees, JSON snippets, JavaScript snippets, and command-oriented configuration advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend model tiers and configuration choices; users should verify current provider pricing and API availability.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
