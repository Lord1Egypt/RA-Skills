## Description: <br>
Trade gTrade perpetuals via CAI using market lookup, preflight checks, trade placement, order status, and hosted enrollment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to guide an agent through CAI enrollment, gTrade market discovery, preflight validation, live trade placement, order status checks, and close flows on supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to place or close live leveraged crypto-perpetual trades. <br>
Mitigation: Require explicit user confirmation for every live trade or close action and enforce predefined notional and leverage limits. <br>
Risk: A CAI API key with platform or full scope can grant meaningful trading authority. <br>
Mitigation: Store CAI_API_KEY only in the agent secret store, use the narrowest available scope, and avoid exposing the secret in prompts or logs. <br>
Risk: Hosted CAI enrollment can enable automated trading for the user. <br>
Mitigation: Have the user complete enrollment directly and never confirm enrollment on the user's behalf. <br>


## Reference(s): <br>
- [CAI Skill Reference](https://cai.com/skill.md) <br>
- [CAI Tools Manifest](https://cai.com/specs/cai-tools.manifest.json) <br>
- [CAI Developers](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and API/action parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY with platform or full scope; live trade and close actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.17 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
