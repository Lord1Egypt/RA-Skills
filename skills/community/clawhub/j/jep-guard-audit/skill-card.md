## Description: <br>
Provides API endpoints and Python components for ingesting JEP/JAC-style audit events, inspecting chains, and exporting compliance-oriented reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to prototype judgment-event audit ingestion, chain inspection, violation summaries, and compliance-oriented report exports. Review the implementation before relying on its output for legal, regulatory, security, or tamper-evident audit evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may overstate security and compliance guarantees. <br>
Mitigation: Treat generated reports as prototype analysis until the skill is reviewed for the intended legal, regulatory, and security context. <br>
Risk: The security evidence says not to rely on the skill for tamper-evident audit evidence without additional hardening. <br>
Mitigation: Add and review real JWS/signature verification, authentication, deployment hardening, sensitive-data handling guidance, and locked dependency versions before production use. <br>
Risk: The artifact accepts and stores audit events through API endpoints, which can include sensitive decision data. <br>
Mitigation: Deploy only in controlled environments with access controls, input validation, retention rules, and data-handling review appropriate to the logged data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/schchit/jep-guard-audit) <br>
- [README](artifact/jep-guard-audit-skill/README.md) <br>
- [CHANGELOG](artifact/jep-guard-audit-skill/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses, compliance report text, Python interfaces, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include event-ingestion status, chain inspection results, violation and warning summaries, findings, recommendations, and raw compliance report text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, frontmatter, manifest, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
