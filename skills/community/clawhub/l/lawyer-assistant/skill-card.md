## Description: <br>
Lawyer Assistant structures Chinese legal case facts, suggests legal research paths, and produces case analysis, risk, evidence, and litigation-strategy guidance. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yang222265](https://clawhub.ai/user/yang222265) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal professionals and users preparing a Chinese-law matter use this skill to organize case facts, identify likely legal relationships and statutes, plan case research, and draft a structured analysis for human review. It is an aid only and does not replace advice from a licensed lawyer. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive legal facts and stores user-contributed case data in local JSON files. <br>
Mitigation: Use redacted or fictionalized facts unless privacy notices, consent, retention controls, and deletion or redaction safeguards are in place. <br>
Risk: The skill may perform external legal-case lookups or rely on API-labeled sources whose reliability is not fully established. <br>
Mitigation: Use HTTPS-only trusted providers where possible and verify all cited cases and legal authorities against authoritative legal databases before relying on them. <br>
Risk: Some example or generated case data may be mistaken for verified legal authority. <br>
Mitigation: Label generated or example cases clearly and require professional review before using the analysis in client matters or proceedings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang222265/lawyer-assistant) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Legal Research Method](artifact/LEGAL_RESEARCH_METHOD.md) <br>
- [v3.0 Release Notes](artifact/v3.0 发布说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown-style legal analysis report and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include legal basis summaries, case-search suggestions, evidence guidance, risk warnings, and strategy recommendations.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
