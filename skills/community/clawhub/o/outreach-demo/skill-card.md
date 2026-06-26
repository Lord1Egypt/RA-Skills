## Description: <br>
Research a business website, produce a concise prospect report, recommend concrete OpenClaw use cases, and draft a tailored outreach email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lexAlex36](https://clawhub.ai/user/lexAlex36) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales, growth, or demo operators use this skill to turn a business website URL and contact email into evidence-based OpenClaw opportunity materials. It produces a prospect report, outreach email drafts, and optional delivery artifacts while requiring approval before real email is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real email through a configured Gmail/gog account, and the send script does not itself enforce the approval gate described by the skill instructions. <br>
Mitigation: Require a manual preview and explicit user approval for each recipient/message before invoking the send script; use --dry-run first when validating setup. <br>
Risk: PDF rendering uses headless Chromium with --no-sandbox. <br>
Mitigation: Render only trusted, locally generated HTML, or run PDF conversion inside an isolated environment when handling untrusted content. <br>
Risk: Outreach recommendations may overstate business needs if website observations are treated as verified internal facts. <br>
Mitigation: Keep claims grounded in visible public website evidence and phrase uncertain conclusions as likely, apparent, or suggested. <br>


## Reference(s): <br>
- [Outreach Demo Report Format](references/report-format.md) <br>
- [Outreach Demo Email Template](references/email-template.md) <br>
- [Value-First Outreach Mode](references/value-first-outreach.md) <br>
- [Visual Delivery Mode](references/visual-delivery.md) <br>
- [Follow-Up Sequence](references/follow-up-sequence.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON, Markdown reports, plain-text or HTML email drafts, HTML/PDF briefs, preview manifests, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-first outreach workflow with optional Gmail send after explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
