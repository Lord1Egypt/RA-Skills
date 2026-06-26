## Description: <br>
Pipeline comptable orchestrates a local accounting-document workflow from incoming mail or document batches through analysis, client identification, filing, and payment reconciliation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting teams and their agents use this skill to process incoming invoices, bank statements, and expense reports into client folders while surfacing ambiguous items for accountant review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and files local accounting documents from the selected email or inbox path. <br>
Mitigation: Run it only on the intended client directory or email file and keep normal access controls around financial documents. <br>
Risk: Automatic payment reconciliation runs after filing unless disabled. <br>
Mitigation: Use --no-rapprochement when payment reconciliation should not run for a batch. <br>
Risk: Ambiguous client identification can require accountant judgment. <br>
Mitigation: Review the surfaced questions and summary before relying on filed documents or reconciled results. <br>


## Reference(s): <br>
- [Pipeline comptable on ClawHub](https://clawhub.ai/trendex/pipeline-comptable) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON report on stdout with a human-readable summary on stderr; agent-facing instructions in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes a local email JSON file or inbox directory and can optionally skip payment reconciliation with --no-rapprochement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
