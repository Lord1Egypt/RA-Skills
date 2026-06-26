## Description: <br>
Classifies French accounting documents such as invoices and bank statements into client, year, month, and document-type folders while maintaining client records and a processing report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
French accounting firms and their agents use this skill to process incoming invoices, bank statements, and related accounting documents, classify them into a client folder tree, and surface questions when client attribution is ambiguous. <br>

### Deployment Geography for Use: <br>
France <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive accounting emails, attachments, and client records and persists them in a workspace. <br>
Mitigation: Use a dedicated accounting inbox and workspace, restrict access to that workspace, and review persisted client records before broader deployment. <br>
Risk: Automatic or bulk processing can classify many documents before a human notices ambiguous client attribution. <br>
Mitigation: Require confirmation for bulk runs and ambiguous cases, and review _report.json questions and incomplete items before relying on the classification. <br>
Risk: External company lookup can send company identifiers to a public company API. <br>
Mitigation: Disable or remove external company lookup unless the user explicitly approves sending identifiers outside the workspace. <br>
Risk: Broad Gmail, Drive, or password-manager access would increase exposure if granted to the skill environment. <br>
Mitigation: Grant only tightly scoped Gmail, Drive, and credential access needed for the accounting workflow. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Contrat d'invocation et sources](references/contrat-io.md) <br>
- [Reforme de la facturation electronique 2026](references/reforme-facturation-2026.md) <br>
- [Structure cible et conventions de nommage](references/structure-cible.md) <br>
- [Extraction et validation comptable francaise](references/validation-fr.md) <br>
- [Roadmap](references/roadmap.md) <br>
- [Skill page](https://clawhub.ai/trendex/organisation-documents) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-language summaries with shell commands, JSON reports, and file-organization outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates client document folders, clients.json, _index.json, and _report.json.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
