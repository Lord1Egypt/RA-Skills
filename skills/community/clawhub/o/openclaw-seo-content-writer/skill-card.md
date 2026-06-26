## Description: <br>
Write and ship SEO blog posts with Tony + Peter workflow, publish QA, deploy verification, and GSC indexing. SEO博客写作/发布/部署/谷歌收录 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, developers, and site operators use this skill to run a repeatable SEO blog production workflow from brief and draft generation through publish QA, deployment verification, Google Search Console submission, and indexing-status receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may trigger production deploys or Google Search Console submissions. <br>
Mitigation: Use least-privilege deployment and GSC credentials, review changes before production actions, and submit only URLs that pass the indexability gate. <br>
Risk: Receipts and generated artifacts could accidentally include sensitive operational details or credentials. <br>
Mitigation: Do not put secrets in receipts or generated artifacts, and keep credentials configured only in the user's controlled environment. <br>
Risk: Thin or weakly evidenced content can be published if QA gates are bypassed. <br>
Mitigation: Require structural preflight, content-quality audit, and bounded recovery research before source publish. <br>


## Reference(s): <br>
- [Tony pipeline](references/tony-pipeline.md) <br>
- [Peter closeout](references/peter-closeout.md) <br>
- [GSC indexing](references/gsc-indexing.md) <br>
- [Receipt contracts](references/receipt-contracts.md) <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/openclaw-seo-content-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured receipts and inline commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow instructions, QA gates, deployment and indexability checks, and receipt records; it does not bundle credentials.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
