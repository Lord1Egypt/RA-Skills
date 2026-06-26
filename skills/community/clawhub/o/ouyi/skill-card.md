## Description: <br>
Ouyi API Tool sends prompts to the Ouyi chat API through a local Node.js script and returns the API response for agent use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlsjzj](https://clawhub.ai/user/dlsjzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to route a prompt to the Ouyi chat API for bilingual chat, investment, technical, or general reasoning tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and task context are sent to the external Ouyi API provider. <br>
Mitigation: Invoke the skill explicitly for Ouyi use and avoid sending confidential, personal, credential, or regulated data. <br>
Risk: API credentials may be exposed if they are edited directly into the script. <br>
Mitigation: Set OUYI_API_KEY in the environment instead of storing credentials in source files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlsjzj/ouyi) <br>
- [Ouyi Chat Completions Endpoint](https://api.rcouyi.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response with content, reasoning token count, model, and error fields; the agent answer is derived from the content field.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Ouyi API key and sends selected prompts to an external API provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
