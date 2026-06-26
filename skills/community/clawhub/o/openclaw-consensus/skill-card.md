## Description: <br>
Run a fixed 2-round cross-model deliberation through the repo-local OpenClaw Consensus runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pstepien-labs](https://clawhub.ai/user/pstepien-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run one agreed brief through a bounded, explicitly selected set of API-backed models and receive a final synthesis that preserves consensus, disagreement, uncertainty, and escalation points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefs and model outputs are sent to explicitly selected API-backed model providers. <br>
Mitigation: Use the skill only with content that may be shared with those providers under the applicable agreements; avoid secrets, regulated data, and proprietary material unless permitted. <br>
Risk: Consensus output may still be incorrect or incomplete. <br>
Mitigation: Preserve disagreement and uncertainty in the final synthesis and use narrow expert escalation for high-stakes decisions. <br>
Risk: Local run artifacts remain on disk after execution. <br>
Mitigation: Review generated run directories and remove artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pstepien-labs/openclaw-consensus) <br>
- [Publisher Profile](https://clawhub.ai/user/pstepien-labs) <br>
- [README](artifact/README.md) <br>
- [Runtime Contract](artifact/docs/RUNTIME_CONTRACT.md) <br>
- [Prompt Contract](artifact/docs/PROMPT_CONTRACT.md) <br>
- [Commands](artifact/docs/COMMANDS.md) <br>
- [Validation Notes](artifact/validation/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, files, guidance] <br>
**Output Format:** [Markdown synthesis with local Markdown and JSON run artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local run artifacts including the brief, run metadata, round outputs, and final synthesis.] <br>

## Skill Version(s): <br>
0.1.2 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
