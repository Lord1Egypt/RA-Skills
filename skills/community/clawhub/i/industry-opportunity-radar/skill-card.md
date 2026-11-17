## Description:

Tracks industry changes against saved JishuDB evidence to produce baseline or change briefings, comparable indicators, opportunity hypotheses, and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts use this skill to establish an industry evidence baseline or compare new reports and indicators with saved snapshots, then document changes, opportunity hypotheses, and risks. Recurring monitoring requires separately authorized host scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled setup can install and launch JishuDB Desktop and change the host's MCP client configuration.

Mitigation: Review the setup plan and authorize installation and configuration changes only if JishuDB is intended and the publisher is trusted.

Risk: The Windows helper invokes PowerShell despite documentation saying it does not.

Mitigation: Review the Windows helper and resolve the documentation discrepancy before running it.

Risk: The workflow uses OAuth/client trust and persists research records.

Mitigation: Approve the destination and retention scope, complete trust prompts yourself, and avoid transferring unauthorized or sensitive material.

## Reference(s):

- [Project homepage (listed in release metadata)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/industry-opportunity-radar)
- [Report discovery and evidence contract](artifact/references/evidence-contract.md)
- [JishuDB setup quickstart](artifact/references/jishudb-setup/references/setup-quickstart.md)
- [199IT report discovery category](https://www.199it.com/archives/category/report)

## Skill Output:

**Output Type(s):** [Markdown, CSV, Research guidance]

**Output Format:** [Markdown briefings and evidence records with a CSV of indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists authorized evidence snapshots in JishuDB; a first run establishes a baseline rather than a cross-run trend.]

## Skill Version(s):

0.1.17 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
