## Description: <br>
Log meals, check nutrition progress, and manage calorie goals in the OpenCal app hands-free via an AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neikfu](https://clawhub.ai/user/neikfu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenCal users use this skill to let an agent search foods, scale nutrition values, log meals, summarize daily intake, and update calorie or macro goals through the OpenCal API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OpenCal API key that can read meal history, add or delete food entries, and change calorie or macro goals. <br>
Mitigation: Keep OPENCAL_API_KEY private, install only when this account access is acceptable, and rotate the key if it may have been exposed. <br>
Risk: Incorrect food matching, portion scaling, or goal updates can create inaccurate nutrition records. <br>
Mitigation: Review the agent's logged changes and confirmations, and correct entries or goals in OpenCal when needed. <br>
Risk: Setting OPENCAL_BASE_URL to an untrusted endpoint could send nutrition data and credentials outside the intended OpenCal service. <br>
Mitigation: Use the default OpenCal API endpoint unless there is a trusted operational reason to override it. <br>


## Reference(s): <br>
- [OpenCal](https://opencal.ai) <br>
- [ClawHub OpenCal listing](https://clawhub.ai/neikfu/opencal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and OPENCAL_API_KEY; API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
