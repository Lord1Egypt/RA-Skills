## Description: <br>
Orchestrates NotebookLM source ingestion, structured SKILL.md extraction, validation, testing, and iteration for creating Claude Code skills from user-provided source materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidcvs](https://clawhub.ai/user/kidcvs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn curated PDFs, URLs, YouTube links, and other domain sources into reusable Claude Code skills. It guides source collection, NotebookLM extraction, local installation, validation, security review, testing, and iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can upload confidential documents, private URLs, or internal videos to NotebookLM as source material. <br>
Mitigation: Review source sensitivity before use, prefer a scratch workspace, and avoid adding confidential materials unless the user has approved that handling. <br>
Risk: The workflow can install model-generated instructions into a persistent agent skills directory. <br>
Mitigation: Inspect the generated SKILL.md and approve the exact contents and target skill name before moving it into the persistent skills directory. <br>


## Reference(s): <br>
- [NotebookLM CLI](https://github.com/UseClawPro/notebooklm) <br>
- [Skill Extraction Prompt Template](references/skill-extraction-prompt.md) <br>
- [ClawHub skill page](https://clawhub.ai/kidcvs/notebooklm-skill-factory) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated SKILL.md content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided source materials and NotebookLM responses to create, validate, and refine local skill files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
