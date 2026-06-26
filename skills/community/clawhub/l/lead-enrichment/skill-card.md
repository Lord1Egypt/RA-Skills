## Description: <br>
Lead Enrichment generates prospect dossiers from a name, company, email, or LinkedIn URL, including profile details, company context, contact guesses, source links, and talking points. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[audsmith28](https://clawhub.ai/user/audsmith28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, recruiting, partnerships, and investor workflows can use this skill to prepare prospect research, summarize company context, and draft personalized outreach talking points. Current evidence shows the implementation returns mock dossiers, so users should treat outputs as demonstrations until the enrichment logic is replaced and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill advertises real lead enrichment while the current implementation returns mock dossiers. <br>
Mitigation: Treat generated dossiers as non-factual demonstrations until the publisher replaces the mock implementation and validates enrichment results against real sources. <br>
Risk: The security guidance warns that batch mode should not be run on untrusted CSV files. <br>
Mitigation: Use only reviewed input files, inspect batch commands before execution, and require the publisher to remove the bash-c CSV path before processing untrusted lead lists. <br>
Risk: The security guidance calls for clearer credential checks and privacy/export controls before use with real leads. <br>
Mitigation: Review configuration, credential handling, retention settings, and export destinations before using the skill with personal or commercial contact data. <br>


## Reference(s): <br>
- [Lead Enrichment Skill Page](https://clawhub.ai/audsmith28/lead-enrichment) <br>
- [Publisher Profile](https://clawhub.ai/user/audsmith28) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON lead dossiers, Markdown summaries, CSV exports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include locally stored lead profiles, export files, source URLs, and generated talking points.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
