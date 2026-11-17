## Description:

Hybrid Dev guides agents through a three-phase development workflow where a local model plans, Copilot implements, and a local model validates against acceptance gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyoumo](https://clawhub.ai/user/wangyoumo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure project iterations into planning, Copilot handoff, and validation phases with clear acceptance gates and review outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated task packs may be too specific to the bundled customer registry MVP example.

Mitigation: Review and adapt the task pack scope, domain assumptions, and acceptance criteria before handing work to Copilot.

Risk: Broad triggers may cause the skill to be selected for general iteration or validation requests where its three-phase workflow is not intended.

Mitigation: Confirm the requested task actually needs planning, Copilot handoff, and validation gates before applying the workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown prompts, task packs, implementation summaries, test reviews, coverage matrices, and defect lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow expects phase outputs under openclaw/output/phase-a, openclaw/output/phase-b, and openclaw/output/phase-c.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
