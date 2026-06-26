## Description: <br>
Use when an agent needs to turn evidence-backed behavior into a validated self-intro submission, a share-card JSON payload, and a final screenshot-friendly HTML selfie card with a real 8-bit character image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenghaofan1998](https://clawhub.ai/user/chenghaofan1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and teams use this skill to turn real agent traces, memory, owner feedback, and artifacts into a concise public identity bundle. It helps produce validated self-intro JSON, share-card JSON, image guidance, and a screenshot-ready HTML card without relying on placeholder or generic identity claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memories, traces, owner feedback, saved preferences, images, or URLs may be summarized into public-facing card content. <br>
Mitigation: Review the generated JSON and HTML before publishing, and include only evidence and assets intended for public display. <br>
Risk: Weak or placeholder evidence can produce generic or misleading public identity claims. <br>
Mitigation: Use real, repeated agent evidence and reject example fixtures, placeholder images, and identity claims that are not supported by the evidence. <br>


## Reference(s): <br>
- [Agent Self Extraction Guide](references/agent-self-extraction-guide.md) <br>
- [Agent self-intro submission schema](schemas/agent-self-intro-submission-schema.json) <br>
- [Share-card schema](schemas/share-card-schema.json) <br>
- [ClawHub skill page](https://clawhub.ai/chenghaofan1998/openclaw-shrimpcard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files] <br>
**Output Format:** [Validated JSON payloads, concise prompt and workflow guidance, shell commands, and rendered HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires real agent evidence and a real 8-bit or pixel-art character image before final bundle validation.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
