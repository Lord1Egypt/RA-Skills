## Description: <br>
OpenClaw skill for autonomous play in the OVERCLOCK AI Strategic Battle Arena, including battles, card purchases, strategy changes, and game monitoring through API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[senti-1000ma](https://clawhub.ai/user/senti-1000ma) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to operate an OVERCLOCK player account by checking game state, changing strategy, buying card packs, running battles, reviewing leaderboards, and reporting observed behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend account value by purchasing card packs. <br>
Mitigation: Use a dedicated throwaway player ID and require explicit user confirmation plus a budget cap before any purchase. <br>
Risk: The skill can mutate a live game account through battles and strategy changes. <br>
Mitigation: Verify the intended API host and only run against accounts or services the user is authorized to modify. <br>
Risk: The QA mission includes log inspection and bug-finding behavior against service endpoints. <br>
Mitigation: Run QA tasks only with authorization to inspect service logs and test invalid inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/senti-1000ma/overclock-agent) <br>
- [OVERCLOCK Agent API Reference](resources/API.md) <br>
- [OVERCLOCK QA Mission](MISSION_QA.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue live game-account actions, including battles, strategy updates, log inspection, and card-pack purchases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
