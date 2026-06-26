## Description: <br>
Provides an M-Flow-based memory workflow for adding, indexing, searching, and distilling agent memory across lexical, vector, and triplet search modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sora-mury](https://clawhub.ai/user/sora-mury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to M-Flow memory operations, including memory capture, indexing, multimode recall, and session distillation into knowledge points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and index conversation content with unclear consent, retention, deletion, and sharing boundaries. <br>
Mitigation: Review the deployment before installing, use only non-sensitive content until storage and access boundaries are verified, and confirm deletion and retention behavior before production use. <br>
Risk: Memory distillation may summarize or retain raw transcripts depending on the local M-Flow setup. <br>
Mitigation: Verify whether distillation stores summaries, raw transcripts, or both, and document who or what agents can search retained memories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sora-mury/m-flow-memory) <br>
- [Publisher profile](https://clawhub.ai/user/sora-mury) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment variables, dependency versions, local service endpoints, and memory workflow steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
