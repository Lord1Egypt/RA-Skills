## Description: <br>
Coordinates OpenClaw task triage by routing frontend work to Gemini CLI, backend work to Codex CLI, and final QA review to Claude. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenZhouMing](https://clawhub.ai/user/ChenZhouMing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate OpenClaw work across Claude, Gemini CLI, and Codex CLI, including task classification, delegation, progress tracking, and QA acceptance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private task details may be exposed to delegated CLI agents if their workspace or tool access is broader than intended. <br>
Mitigation: Confirm what Claude, Gemini CLI, and Codex CLI can access before routing sensitive project details through this workflow. <br>
Risk: Keyword-based task routing can misclassify mixed or ambiguous work. <br>
Mitigation: Have the coordinating agent review unclear tasks and split full-stack work before delegation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChenZhouMing/openclaw-team-coordinator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown coordination guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance with no code, persistence, credential access, or hidden behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
