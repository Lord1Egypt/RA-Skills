## Description:

Private local document AI for Intel hardware that parses PDFs, invoices, screenshots, and diagrams with MinerU 2.5 on OpenVINO GenAI and outputs structured JSON, Markdown, and user-defined invoice fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuo-yoyowz](https://clawhub.ai/user/zhuo-yoyowz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation teams use this skill to parse local PDFs, invoices, receipts, screenshots, and diagrams into grounded artifacts, then derive structured records or draft code and notebook scaffolds while keeping document processing local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent HTTP service is unauthenticated.

Mitigation: Keep it bound to 127.0.0.1, prefer --server-kind ipc or --no-server where possible, and shut it down after use.

Risk: Local document paths and generated artifacts may expose sensitive content on shared machines.

Mitigation: Install and run only on a trusted single-user machine, write outputs to private directories, and delete sensitive artifacts after review.

Risk: Mutable dependency or model setup can change runtime behavior.

Mitigation: Use a virtual environment and pin model and dependency versions before using the skill in repeatable workflows.

Risk: Generated notebooks or code may include remote-code cells or unsafe assumptions.

Mitigation: Review generated notebooks and code before execution, publishing, or connecting them to real systems, and remove trust_remote_code=True unless required.

## Reference(s):

- [Mode Guide](references/mode_guide.md)
- [Output Contracts](references/output_contracts.md)
- [Canonical Document Schema](references/schema.md)
- [MinerU 2.5 Pro OpenVINO INT4 Model Bundle](https://www.modelscope.cn/models/snake7gun/MinerU2.5-Pro-2604-1.2B-int4-ov)
- [ClawHub Skill Page](https://clawhub.ai/zhuo-yoyowz/skills/local-document-ai-openvino)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON, Markdown, HTML reports, Jupyter notebooks, generated code files, and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes per-run artifact folders with parsed.json, parsed.md, result_report.html, task_output files, and traceability where downstream outputs are generated.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
