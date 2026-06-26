## Description: <br>
Delegates tasks to Gemini or Qwen with quota tracking and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to delegate token-heavy, low-complexity work to external LLM services while retaining local reasoning, validation, and integration control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External LLM delegation can expose sensitive prompts, files, secrets, or private data. <br>
Mitigation: Confirm the task is low-risk before delegation, remove secrets and private data from prompts or files, and use local processing for authentication, cryptography, and security-sensitive work. <br>
Risk: Delegated output can be incorrect, misleading, poorly formatted, or difficult to integrate. <br>
Mitigation: Define the expected output and validation method before delegation, then review and validate results before integrating them. <br>
Risk: Audit logs can retain full unsanitized prompts or responses. <br>
Mitigation: Avoid saving full unsanitized prompts or responses in audit logs; log only the minimum useful usage and outcome details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conjure-delegation-core) <br>
- [Conjure plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [Task assessment module](artifact/modules/task-assessment.md) <br>
- [Handoff patterns module](artifact/modules/handoff-patterns.md) <br>
- [Cost estimation module](artifact/modules/cost-estimation.md) <br>
- [Troubleshooting module](artifact/modules/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, decision matrices, templates, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces delegation plans, validation criteria, cost estimates, and troubleshooting guidance for external LLM workflows.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
