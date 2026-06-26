## Description: <br>
Convert rough project ideas into a human-readable blueprint and a clean OpenClaw execution packet for safe, scoped implementation and continuation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catcherintheroad-hub](https://clawhub.ai/user/catcherintheroad-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use OpenClaw Pilot to turn rough project goals into a reviewable blueprint and a separate OpenClaw execution packet. It is useful when the user wants scoped implementation planning, continuation, and a packet-only handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated execution packet could contain unsuitable instructions for a specific project even though the skill itself is low risk. <br>
Mitigation: Review each generated OpenClaw execution packet before handing it to an executor. <br>


## Reference(s): <br>
- [OpenClaw Pilot on ClawHub](https://clawhub.ai/catcherintheroad-hub/openclaw-pilot) <br>
- [Publisher profile](https://clawhub.ai/user/catcherintheroad-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Two assistant messages: a human-readable markdown blueprint followed by a packet-only text block.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The second message must contain only an [OPENCLAW_EXECUTION_PACKET v1] block and its closing marker, with no extra prose.] <br>

## Skill Version(s): <br>
0.3.0-beta.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
