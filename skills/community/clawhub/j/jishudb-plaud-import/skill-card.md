## Description:

Archives selected Plaud recordings, audio, transcripts, and meeting summaries in JishuDB from an authorized connector or local export while preserving source associations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

People archiving meetings use this skill to import selected Plaud audio, transcripts, or summaries into JishuDB, retain source associations, and optionally compare imported meetings with cited project material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled JishuDB Desktop installation and launch can make substantial changes to the local machine; the Windows helper's PowerShell/WSH use conflicts with its setup documentation.

Mitigation: Review the concrete installation plan, source, paths, permissions, and Windows helper behavior before approving installation.

Risk: Meeting recordings and transcripts may contain sensitive material and are transferred to the selected knowledge base.

Mitigation: Confirm the selected recordings, account, destination, and write authorization before transfer; retain only approved material.

## Reference(s):

- [Skill homepage (release metadata)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb-plaud-import)
- [ClawHub skill listing](https://clawhub.ai/bowen-aijishu/skills/jishudb-plaud-import)
- [Plaud MCP documentation](https://docs.plaud.ai/plaud-mcp-cli/mcp)
- [Connection and transfer guide](references/connection-and-transfer.md)
- [JishuDB setup quickstart](references/jishudb-setup/references/setup-quickstart.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown status report with saved IDs and cited comparisons when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves associations among separately archived audio, transcripts, summaries, and provenance records.]

## Skill Version(s):

0.1.17 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
