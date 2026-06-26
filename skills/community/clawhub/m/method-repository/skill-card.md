## Description: <br>
Stores epidemiology study designs, statistical methods, concepts, and paper table layouts from paper-analysis conversations into a local SQLite knowledge base with duplicate prevention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chircken891](https://clawhub.ai/user/chircken891) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agents use this skill to save epidemiological research methods and paper-derived schema notes into a local knowledge base when the user explicitly asks to preserve them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save sensitive, confidential, personal, or unverified information from a conversation into a local database. <br>
Mitigation: Use explicit save requests, review the completion report, and avoid saving confidential, personal, or unverified information. <br>
Risk: Incorrectly extracted study designs, methods, concepts, or table layouts could be persisted as research notes. <br>
Mitigation: Review extracted fields before relying on saved records and mark uncertain fields for supplementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chircken891/method-repository) <br>
- [OpenClaw homepage](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status report with SQL and Python snippets for local SQLite writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes user-approved method summaries to a local SQLite database and reports inserted, skipped, and current record counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
