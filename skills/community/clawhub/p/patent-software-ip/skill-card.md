## Description: <br>
Generate CN patent documents and software copyright materials from AI or big-data project code, design documents, and research papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaccen](https://clawhub.ai/user/jaccen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IP practitioners, developers, and product teams use this skill to prepare China-focused CNIPA patent drafts and CPCC software copyright materials for AI and big-data projects. It helps classify technical domains, extract invention points, draft claims and specifications, prepare manuals or source-code documents, and run self-checks. <br>

### Deployment Geography for Use: <br>
China (CNIPA patent and CPCC software-copyright workflows) <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat drafted patent or software-copyright material as legal advice. <br>
Mitigation: Use the skill as an IP drafting aid and have qualified counsel or an authorized reviewer validate filing strategy, claim scope, jurisdiction, and final submissions. <br>
Risk: Inputs may contain confidential source code, invention details, credentials, internal addresses, personal information, or proprietary dataset and hardware details. <br>
Mitigation: Review and apply the skill's desensitization guidance before sharing materials in the active agent context, and remove secrets, internal endpoints, personal data, and sensitive implementation identifiers. <br>
Risk: Outputs may be unsuitable if the user intends a jurisdiction or filing workflow other than China CNIPA patent or CPCC software-copyright preparation. <br>
Mitigation: Confirm the intended China/CNIPA/CPCC workflow and output language before invoking the skill, and adapt or reject the output for other jurisdictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaccen/patent-software-ip) <br>
- [AI patent claims guide](references/ai-patent-claims-guide.md) <br>
- [AI patent special guide](references/ai-patent-special.md) <br>
- [AI software copyright guide](references/ai-software-copyright-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown files and prose sections, including patent claims, specifications, abstracts, manuals, source-code documents, prior-art summaries, checklists, and Mermaid diagrams.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When saved, deliverables are organized under outputs/{case-id}/ with patent and software-copyright subfolders.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
