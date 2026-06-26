## Description: <br>
Generates three-level knowledge-graph learning paths from occupational skill standard documents, with emphasis on Chinese official resources and source labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzp2026](https://clawhub.ai/user/wzp2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, instructors, and agent users working from Chinese occupational skill standards use this skill to produce structured learning paths, source-labelled knowledge nodes, and exportable knowledge-graph files for training planning or qualification study. <br>

### Deployment Geography for Use: <br>
Global; content is focused on Chinese occupational skill standards and domestic reference sources. <br>

## Known Risks and Mitigations: <br>
Risk: Extracted document text and intermediate learning-path state may be stored in local temporary files. <br>
Mitigation: Run the skill in a trusted workspace and clear temporary artifacts after use when source documents contain sensitive content. <br>
Risk: Public reference lookups may send topic terms to external reference sites. <br>
Mitigation: Avoid confidential topic terms in public lookups or review the lookup behavior before using restricted source material. <br>
Risk: Generated learning paths, citations, and source labels are draft material and may include incomplete or non-official references. <br>
Mitigation: Manually verify citations, standards, and source labels before using outputs for certification, compliance, or formal training decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wzp2026/learning-path-builder) <br>
- [Detailed usage guide](references/README.md) <br>
- [Reference source configuration](references/config.yaml) <br>
- [Skills Talent Evaluation Work Network](https://www.osta.org.cn/) <br>
- [National Standards Full-Text Disclosure System](https://openstd.samr.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [JSON, CSV, JSON-LD, Markdown, and progress messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-labelled three-level knowledge graph artifacts and local intermediate progress files.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
