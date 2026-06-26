## Description: <br>
AI-powered legal document automation for law firms, including contract clause extraction, document summarization, legal research, and deadline tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manas-io-ai](https://clawhub.ai/user/manas-io-ai) <br>

### License/Terms of Use: <br>
Commercial <br>


## Use Case: <br>
Attorneys, paralegals, legal operations teams, and law-firm staff use LegalDoc AI to review legal documents, extract contract clauses, summarize matters, research legal authorities, and track deadlines. Outputs are intended to assist legal professionals and require independent review before use in legal work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal analysis, extracted clauses, summaries, citations, and deadlines may be incomplete or incorrect. <br>
Mitigation: Independently verify all outputs against source documents, applicable law, court rules, and professional legal judgment before relying on them. <br>
Risk: Real matter data may contain privileged, confidential, regulated, or client-sensitive information. <br>
Mitigation: Verify the publisher and any claimed SOC 2, HIPAA, GDPR, privilege, or enterprise terms before processing real client data, and avoid sending privileged facts to external research services unless approved. <br>
Risk: Deadline tracking may create local records that expose matter information or become stale. <br>
Mitigation: Protect and periodically delete the local ~/.legaldoc deadline database, use least-privilege API keys, and confirm all calculated deadlines before use. <br>


## Reference(s): <br>
- [LegalDoc AI ClawHub page](https://clawhub.ai/manas-io-ai/legaldoc-ai) <br>
- [Full Documentation](https://docs.legaldoc.ai) <br>
- [API Reference](https://docs.legaldoc.ai/api) <br>
- [Clause Type Glossary](https://docs.legaldoc.ai/clauses) <br>
- [Integration Guides](https://docs.legaldoc.ai/integrations) <br>
- [Best Practices](https://docs.legaldoc.ai/best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, tables, command-line text, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce legal analysis, risk notes, suggested revisions, citations, deadline alerts, and local deadline records; outputs require human legal review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and clawdhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
