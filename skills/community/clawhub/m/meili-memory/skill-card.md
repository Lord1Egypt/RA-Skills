## Description: <br>
Local full-text search for OpenClaw memory recall using MeiliSearch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enjuguna](https://clawhub.ai/user/enjuguna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index local memory files, query them through MeiliSearch, and optionally distill recent facts into MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer uses sudo to create a persistent MeiliSearch systemd service and adds an hourly cron job. <br>
Mitigation: Review install.sh before installation and install only on systems where persistent local indexing is acceptable. <br>
Risk: The skill indexes OpenClaw MEMORY.md and daily memory notes into MeiliSearch. <br>
Mitigation: Keep MEILI_HOST bound to a trusted local endpoint and verify that sensitive memory content is excluded before relying on the index. <br>
Risk: The installer prints a generated MeiliSearch master key and configures scripts to use it. <br>
Mitigation: Protect or rotate the printed master key after installation and store active credentials only in the workspace .env file. <br>
Risk: Distillation can append extracted facts to MEMORY.md when run with --apply. <br>
Mitigation: Run distillation in dry-run mode first and manually inspect the proposed facts before using --apply. <br>
Risk: A full reindex deletes and recreates the MeiliSearch indexes. <br>
Mitigation: Use the --full operation only with the explicit --force flag after confirming index recreation is intended. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub release page](https://clawhub.ai/enjuguna/meili-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions, shell command output, and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes query metadata, matched filters, tiers searched, result counts, and ranked memory results.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
