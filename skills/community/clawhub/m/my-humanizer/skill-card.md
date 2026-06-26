## Description: <br>
Transform AI-generated content into natural, human-sounding writing, measure the improvement, and optionally verify the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itxbilal176](https://clawhub.ai/user/itxbilal176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to rewrite stiff or formulaic AI-assisted drafts into clearer, more natural prose while measuring the before-and-after changes. It is best suited for style transformation and audit trails, not for proving human authorship or bypassing detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake rewritten text or verification output for proof of human authorship. <br>
Mitigation: Treat output as style editing and evaluation support only; do not claim the result proves human authorship. <br>
Risk: Private original or rewritten text could be exposed if sent to an external verifier. <br>
Mitigation: Keep rewriting and evaluation local; if verification is used, send only structured metrics such as counts, deltas, and boolean checks. <br>
Risk: A rewrite may alter meaning or introduce unsupported facts. <br>
Mitigation: Review the rewritten text against the source for meaning preservation, tone fit, and factual accuracy before using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itxbilal176/my-humanizer) <br>
- [Verified Humanizer examples](artifact/references/examples.md) <br>
- [OpenClaw integration notes](artifact/references/openclaw-integration.md) <br>
- [Transformation report template](artifact/assets/TRANSFORMATION-REPORT-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON object with rewritten text, change summary, evaluation metrics, and optional verification status; Markdown reports when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps original and rewritten text local by default; optional verification should use structured metrics only.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
