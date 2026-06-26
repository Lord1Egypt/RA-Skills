## Description: <br>
Runtime-level grill enforcement plugin. Blocks exec/spawn calls for research/development tasks unless a valid grill token exists. Ensures agents think before they act. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangsuann](https://clawhub.ai/user/tangsuann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Grill Gate to enforce a design-review token check before selected OpenClaw exec or subagent-spawn actions run for research and development tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can block selected agent exec or subagent-spawn actions. <br>
Mitigation: Install it only in environments where that enforcement is desired, and test the configured policies before relying on it. <br>
Risk: Trigger words, exemptions, blocked commands, token directory, and token TTL may be too broad or too narrow for a deployment. <br>
Mitigation: Review and tune those settings before use. <br>
Risk: Tokens should not be assumed to be truly one-use unless the implementation is fixed. <br>
Mitigation: Use a short token TTL and operational review controls until one-use token behavior is verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangsuann/grill-gate) <br>
- [Publisher profile](https://clawhub.ai/user/tangsuann) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [OpenClaw plugin responses with text block reasons and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May block selected exec or sessions_spawn calls until a valid local grill token is present.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
