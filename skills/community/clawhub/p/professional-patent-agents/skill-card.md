## Description: <br>
Professional Patent Agents is a bilingual multi-agent suite for patent idea mining, prior-art search, inventiveness evaluation, drafting, claim design, audit, valuation, and document conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigpipihua](https://clawhub.ai/user/bigpipihua) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn invention ideas, draft patents, or agency feedback into patent work products such as technical disclosures, search reports, inventiveness assessments, optimized claims, audit reports, valuation reports, and converted Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent work may contain sensitive invention details that could be retained through broad learning, memory, or work-record mining. <br>
Mitigation: Disable or tightly scope continuous learning and memory/work-record mining unless the user explicitly wants persistence for the current project. <br>
Risk: Prior-art search may send invention details to external search providers or patent APIs. <br>
Mitigation: Use only approved providers, redact confidential details where possible, and confirm user consent before external searches. <br>
Risk: Runtime skill installation can expand the behavior and trust boundary of the agent. <br>
Mitigation: Review and approve any additional skill before installation or use. <br>
Risk: Document conversion may invoke Pandoc, Mermaid CLI, Chromium, or Puppeteer, including reduced browser sandboxing when run as root. <br>
Mitigation: Run conversion as a non-root user in an isolated workspace or container, and avoid no-sandbox browser execution where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigpipihua/professional-patent-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and patent drafts, Word documents, Mermaid diagrams, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Markdown, DOCX, and image files during document conversion; may use installed search skills or patent APIs when configured by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
