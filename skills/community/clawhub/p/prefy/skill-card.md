## Description: <br>
Connect to Prefy AI platform for multi-model AI routing, server management, web search, image generation, events lookup, and AI-assisted phone calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runrelay](https://clawhub.ai/user/runrelay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Prefy when they need an agent to call Prefy APIs for model routing, search, image generation, server control, travel or event lookups, or venue phone calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prefy gives an agent access to server-control and real phone-call capabilities. <br>
Mitigation: Use revocable least-privilege credentials and require explicit approval before shell commands, cron or bot changes, paid checkout actions, and outbound phone calls. <br>
Risk: The agent API can use memory and may receive sensitive user information. <br>
Mitigation: Avoid sending sensitive information unless retention and deletion controls are understood and acceptable for the deployment. <br>


## Reference(s): <br>
- [Prefy documentation](https://prefy.com/docs) <br>
- [Prefy skill page](https://clawhub.ai/runrelay/prefy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API examples, JSON request bodies, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce requests that use Prefy credentials and can trigger server actions, paid checkout flows, or outbound phone calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
