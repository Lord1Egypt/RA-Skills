## Description:

Reviews IPO filing materials locally for financial-data consistency, cross-file differences, table arithmetic, evidence locations, and report interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbotaochn](https://clawhub.ai/user/wangbotaochn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and reviewers use this skill to run a local IPO filing review workflow over prospectuses, inquiry responses, audit reports, financial-statement notes, and related disclosure files. It helps prioritize manual review items by surfacing numeric inconsistencies, table arithmetic issues, evidence locations, and diagnostic outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow processes local IPO materials that may contain confidential or sensitive disclosure data.

Mitigation: Install and run the skill only in environments approved for those materials, and keep source documents local as directed by the skill.

Risk: Generated CSV reports may contain untrusted source-document text that could be unsafe when opened in spreadsheet software with formula execution enabled.

Mitigation: Treat generated CSV files as untrusted exports and review them with formula execution disabled unless the CSV writer is hardened.

Risk: Dependency versions are not pinned, which can change parser or document-handling behavior over time.

Mitigation: Review and pin dependencies before deployment, especially for regulated or repeatable review workflows.

Risk: The tool is strongest for numeric consistency checks and may miss narrative or semantic contradictions.

Mitigation: Use its output to prioritize professional manual review rather than as confirmation that a filing is correct.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangbotaochn/skills/ipo-review)
- [Publisher profile](https://clawhub.ai/user/wangbotaochn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and references to generated local HTML, JSON, and CSV reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled tool reads local input files and writes local output reports, including issues.json, financial_facts.csv, evidence_index.json, diagnostic CSV files, run_log.txt, and an HTML report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
