## Description: <br>
General life-sciences research copilot bundling 50 modular sub-skills across human genetics, variant interpretation, functional genomics, expression, pathway biology, protein structure, chemistry, clinical evidence, literature, and public study discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, clinicians, and developers use this skill to route life-science questions to public databases and synthesize concise evidence across genetics, variants, expression, pathways, structure, chemistry, clinical evidence, literature, and study discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act as a broad networked research helper and may contact arbitrary URLs. <br>
Mitigation: Use only public, non-sensitive research inputs and review requested API targets before execution. <br>
Risk: Authorization headers, Cookie headers, or private tokens could be exposed through network requests. <br>
Mitigation: Do not pass Authorization or Cookie headers, private tokens, or other sensitive credentials unless the environment and destination are explicitly trusted. <br>
Risk: Full API responses can remain on disk when save_raw or raw_output_path is enabled. <br>
Mitigation: Keep raw output disabled by default; when it is needed, choose a safe temporary location and delete files that contain sensitive or unnecessary data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sciminer/life-science-database-query) <br>
- [Root skill instructions](artifact/SKILL.md) <br>
- [NCBI BLAST Common URL API notes](artifact/skills/ncbi-blast-skill/references/blast-common-url-api.txt) <br>
- [NCBI Entrez GEO reference](artifact/skills/ncbi-entrez-skill/references/geo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON API results, shell command examples, and optional file paths for saved raw responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write raw API responses to user-selected local paths when save_raw is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
