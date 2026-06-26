## Description: <br>
Manage VoIP calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage VoIP calls, automate voice-related tasks, and support communication operations through a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VoIP API keys may grant access to call management actions or provider account data. <br>
Mitigation: Use a dedicated least-privilege VOIP_API_KEY and keep it out of prompts, logs, and shared output. <br>
Risk: Call-changing actions such as placing, ending, forwarding, or recording calls can affect real users. <br>
Mitigation: Require explicit confirmation before performing call-changing operations. <br>
Risk: The artifact describes command-line use but does not include the referenced VoIP manager script. <br>
Mitigation: Install only when the intended VoIP provider and script implementation are known and reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOIP_API_KEY and returns JSON-formatted results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
