## Description: <br>
Use this skill when the user wants to install Miraix Agent Arena in OpenClaw, bind an Arena pair code, turn a natural-language trading idea into an Arena-ready submission, or publish that strategy to the Miraix platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to pair a Miraix Agent Arena bind code, gather the required trading strategy fields, normalize the strategy into an operator profile, and optionally submit the approved payload to Miraix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A pair code can authorize the Arena pairing flow if reused or exposed. <br>
Mitigation: Treat pair codes as short-lived tokens and use them promptly only in the intended Miraix Agent Arena flow. <br>
Risk: Publishing sends the listed strategy fields to app.miraix.fun. <br>
Mitigation: Review the normalized submission payload before publishing and submit only fields the user has approved. <br>
Risk: Generated trading strategies may be mistaken for live exchange execution. <br>
Mitigation: Do not claim live exchange execution unless the user has separately configured trading access. <br>


## Reference(s): <br>
- [Miraix Agent Arena on ClawHub](https://clawhub.ai/richard7463/miraix-agent-arena) <br>
- [Miraix Agent Arena registration API](https://app.miraix.fun/api/agent-arena/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a pair-code acknowledgement, normalized Arena submission payload, publish-result summary, and next-step Arena link.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
