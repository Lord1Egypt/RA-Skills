## Description: <br>
Coding guidelines inspired by Andrej Karpathy that help agents avoid overcomplication, make precise edits, surface assumptions, and define verifiable success criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wasinc](https://clawhub.ai/user/wasinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill while writing, reviewing, or refactoring code to keep changes simple, precise, and tied to explicit success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill influences broad coding behavior and can bias an agent toward caution over speed on simple tasks. <br>
Mitigation: Apply the guidance when code quality, review, refactoring, or complex implementation decisions are relevant, and allow judgment for small routine changes. <br>
Risk: The skill suggests optional reflection through a self-improvement workflow and updates to references/learnings.md, which can introduce extra local documentation changes. <br>
Mitigation: Decide before use whether the agent may invoke self-improvement or edit local learning notes, and review any resulting file changes before commit. <br>


## Reference(s): <br>
- [Karpathy source observation](https://x.com/karpathy/status/2015883857489522876) <br>
- [ClawHub skill page](https://clawhub.ai/wasinc/karpathy-guidelines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and concise task plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; may recommend tests or local notes updates but does not execute code itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
