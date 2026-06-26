## Description: <br>
Generates vertical WeryAI hydraulic-press crushing videos from text briefs or public HTTPS object images, with prompt expansion, parameter confirmation, and playable video URL results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators use this skill to turn short text briefs or public object images into 9:16 hydraulic-press crushing clips for short-form video workflows. The agent expands the prompt, checks WeryAI model parameters, asks for confirmation, and returns generated video URLs or clear error feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live generation uses a WERYAI_API_KEY and may consume paid WeryAI credits. <br>
Mitigation: Use a revocable or quota-limited API key where possible, review all parameters before confirmation, and avoid unnecessary reruns. <br>
Risk: The required API key is sensitive runtime configuration. <br>
Mitigation: Provide the key only in the execution environment, do not commit it to the skill package, and rotate it if exposure is suspected. <br>
Risk: Generated videos and source images may need rights, content-safety, or platform-compliance review outside the skill's scope. <br>
Mitigation: Review prompts, input images, and outputs before publication or commercial use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/hydraulic-crush-video) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI models registry host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown guidance with JSON command arguments, confirmation tables, and video URLs or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and user confirmation before live paid generation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
