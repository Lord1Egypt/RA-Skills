## Description: <br>
QA remediation auto-fix pipeline for Monet Works content that detects and repairs common content issues: banned phrases, missing disclaimers, missing CTAs, and excessive length, then outputs fixed content and a structured JSON change report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, marketing, and editorial teams use this skill to remediate financial or investment-oriented draft content before publication. It applies automated fixes for supported QA findings and flags tone, strategy, factual, NDA, and other judgment-heavy issues for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated draft edits can change financial, legal, medical, customer-sensitive, or confidential content in ways that are unsuitable for publication. <br>
Mitigation: Review the fixed Markdown and structured JSON report before publishing, and route judgment-heavy issues such as tone, strategy, facts, NDA, and evidence gaps to human review. <br>
Risk: In-place remediation could overwrite the original draft and make changes harder to audit. <br>
Mitigation: Write remediated content to a new output file and preserve the original draft alongside the JSON change report. <br>
Risk: Generated disclaimers and CTAs may not satisfy all regulatory, legal, or brand requirements. <br>
Mitigation: Treat generated disclaimers and CTAs as draft remediation and obtain appropriate editorial, compliance, or legal review before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/monet-works-content-qa-dv) <br>
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Fixed Markdown or text content on stdout with a structured JSON change report on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish all-fixed, partial/manual-review, and error outcomes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
