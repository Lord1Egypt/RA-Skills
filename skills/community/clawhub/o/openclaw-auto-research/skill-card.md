## Description: <br>
Auto Research Pipeline orchestrates an OpenClaw research workflow that turns a research topic into a draft paper through staged scoping, literature review, synthesis, experiment design, execution, analysis, writing, and finalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang1076](https://clawhub.ai/user/lixiang1076) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical writers use this skill to coordinate a multi-phase research pipeline from an initial topic through literature discovery, experiment planning, execution, analysis, and paper drafting. It is intended for agent-assisted research workflows where a human reviews each phase before continuing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can execute generated Python experiment code. <br>
Mitigation: Review generated experiment code before Phase E and run it only in a sandbox with no secrets, limited filesystem access, and controlled network access. <br>
Risk: The workflow can call external literature services, web tools, and LLMs with research-topic context. <br>
Mitigation: Use non-sensitive topics or approved network paths, and avoid including confidential data in topics, prompts, or generated artifacts. <br>
Risk: The workflow can send phase summaries to Feishu. <br>
Mitigation: Disable or avoid notifications unless explicitly approved for the project and audience. <br>
Risk: The workflow can persist lessons from prior runs. <br>
Mitigation: Review stored lessons and do not persist sensitive project details, credentials, unpublished findings, or personal data. <br>
Risk: Generated analyses, citations, and paper drafts may contain incorrect or unsupported claims. <br>
Mitigation: Human reviewers should check metrics, citations, experimental assumptions, and final claims before publication or external sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lixiang1076/openclaw-auto-research) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Research Domains](artifact/references/domains.yaml) <br>
- [Phase A: Research Scoping](artifact/references/phase-a-scoping.md) <br>
- [Phase B: Literature Discovery](artifact/references/phase-b-literature.md) <br>
- [Phase C: Knowledge Synthesis](artifact/references/phase-c-synthesis.md) <br>
- [Phase D: Experiment Design](artifact/references/phase-d-design.md) <br>
- [Phase E: Experiment Execution](artifact/references/phase-e-execution.md) <br>
- [Phase F: Analysis and Decision](artifact/references/phase-f-analysis.md) <br>
- [Phase G: Paper Writing](artifact/references/phase-g-writing.md) <br>
- [Phase H: Finalization](artifact/references/phase-h-finalize.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research artifacts, JSON or JSONL state files, generated Python experiment code, BibTeX references, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged local files under an auto-research run directory and requires human confirmation at phase gates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
