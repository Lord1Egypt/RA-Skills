## Description: <br>
Turn a Douyin or Xiaohongshu link into a concise summary, an actionable todo list, and a recommended reminder time. The hosted service handles the platform access on the server side, and the user only needs to paste the link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobobo2026](https://clawhub.ai/user/bobobo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to turn Douyin or Xiaohongshu links they provide into a concise summary, action-oriented todo items, and a proposed reminder time through a hosted transcription service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release metadata advertises unrelated crypto and purchase capabilities. <br>
Mitigation: Do not grant or rely on those capabilities for this skill unless the publisher explains and corrects the mismatch. <br>
Risk: User-provided Douyin or Xiaohongshu links are sent to a hosted service for processing. <br>
Mitigation: Avoid private, tokenized, or sensitive URLs unless the operator accepts that disclosure or self-hosts the service. <br>
Risk: Backend-provided comment candidates may be copied into public channels. <br>
Mitigation: Review suggested comments before using them publicly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bobobo2026/link-transcriber) <br>
- [Hosted public API origin](https://linktranscriber.store) <br>
- [README](README.md) <br>
- [Deployment notes](docs/DEPLOY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style structured text with a summary, todo list, recommended reminder time, and optional comment candidates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled runner can also return JSON for debugging; normal user-facing output should stay concise.] <br>

## Skill Version(s): <br>
0.1.26 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
