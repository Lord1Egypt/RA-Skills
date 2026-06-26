## Description: <br>
帮助用户收集发明信息并撰写符合格式要求的中文专利交底书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changye](https://clawhub.ai/user/changye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, inventors, and patent-facing technical teams use this skill to gather required invention details, draft Chinese patent disclosure documents, and optionally prepare Mermaid-based figures and Word exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent ideas, implementation details, names, and contact information may be shared with the agent and saved into local Markdown or Word files. <br>
Mitigation: Use placeholders or redact contact details until final export, and review the generated folder before sharing it. <br>
Risk: Optional Word and PNG generation can create additional local artifacts from the same sensitive disclosure content. <br>
Mitigation: Confirm pandoc and mmdc are intentionally available, and inspect generated documents and images before distribution. <br>
Risk: A patent disclosure draft can be incomplete or misleading if the collected invention details are vague or unconfirmed. <br>
Mitigation: Confirm the collected information and outline before drafting, then have qualified patent counsel review the result before filing. <br>


## Reference(s): <br>
- [Patent_Writing.md](references/Patent_Writing.md) <br>
- [patent_example.md](references/patent_example.md) <br>
- [Mermaid Live Editor](https://mermaid.live/) <br>
- [ClawHub skill page](https://clawhub.ai/changye/patent-disclosure-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents, Mermaid diagrams, optional PNG images, and optional Word document exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a dated local project folder and depends on pandoc and mmdc for optional Word and PNG generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
