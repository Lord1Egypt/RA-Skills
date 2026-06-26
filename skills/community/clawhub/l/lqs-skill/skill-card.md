## Description: <br>
LQS Skill is a prompt, schema, and template driven artifact generator for the LQS codebase that guides manual generation of RequirementDraft, Spec, RenderPlan, and preview diff outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantasy0102](https://clawhub.ai/user/fantasy0102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn free-text or exported requirement text into structured LQS Admin boilerplate plans, generated code artifacts, preview diffs, and change reports. The workflow is designed for human review before file writes or migration use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated files or migrations may be incorrect for the target LQS project conventions. <br>
Mitigation: Review the preview diff, target paths, assumptions, and generated migrations before approving file writes or running migrations. <br>
Risk: The skill includes a Google Doc ingest contract, but automatic fetching can expose document links or sensitive text if added by an external workflow. <br>
Mitigation: Use pasted or exported document text, avoid storing credentials or sensitive URL parameters, and keep document retrieval outside the skill unless separately reviewed. <br>
Risk: Ambiguous requirements can lead to default CRUD behavior, path choices, or hard-delete behavior that does not match business intent. <br>
Mitigation: Resolve listed ambiguities and validate assumptions before accepting the generated RenderPlan or ChangeReport. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fantasy0102/lqs-skill) <br>
- [LQS Skill Quickstart](artifact/quickstart.md) <br>
- [LQS Skill Implementation Spec](artifact/skill_spec.md) <br>
- [Implementation Runbook](artifact/implementation_runbook.md) <br>
- [MVP Delivery Checklist](artifact/mvp_delivery_checklist.md) <br>
- [Google Doc Ingest Contract](artifact/examples/google_doc_ingest_contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, unified diff text, and generated source-file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include assumptions, evidence, confidence, ambiguities, target paths, and review-before-write change reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
