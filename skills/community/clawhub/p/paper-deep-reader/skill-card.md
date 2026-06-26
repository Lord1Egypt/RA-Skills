## Description: <br>
Paper Deep Reader helps agents deeply read one selected research paper or technical report and produce a rigorous markdown reading note, technical summary, critique, or implementation memo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soymilkwinsagain](https://clawhub.ai/user/soymilkwinsagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, engineers, and technical readers use this skill to reconstruct the structure, evidence, assumptions, limitations, and reusable ideas in one selected research paper. It is intended for deep paper notes, critiques, technical summaries, and implementation or reproduction memos rather than shallow abstract rewrites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated notes or helper artifacts may overwrite existing local files if output paths are chosen carelessly. <br>
Mitigation: Choose explicit output paths, review the destination before running scripts, and keep separate artifact directories for draft paper maps, notation tables, claim matrices, and final notes. <br>
Risk: Generated reading notes can contain sensitive paper excerpts, private commentary, or unpublished research analysis. <br>
Mitigation: Keep generated notes private when the source paper, comments, or analysis are sensitive, and review content before sharing outside the intended audience. <br>
Risk: The optional scripts are heuristic drafting aids and can create incomplete or misleading intermediate structures if their output is treated as final. <br>
Mitigation: Review paper maps, notation tables, claim matrices, and limitation ledgers against the source paper before using them in a final note. <br>
Risk: The optional Python scripts import a shared _common helper that is not included in this artifact listing. <br>
Mitigation: Verify that any installed package includes the trusted _common helper before running scripts, and do not substitute an untrusted helper file. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/soymilkwinsagain/paper-deep-reader) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Reading workflow](artifact/references/reading-workflow.md) <br>
- [Routing rules](artifact/references/routing-rules.md) <br>
- [Paper taxonomy](artifact/references/paper-taxonomy.md) <br>
- [Output contract](artifact/references/output-contract.md) <br>
- [Scripts README](artifact/scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown reading notes, technical summaries, critique memos, implementation notes, and optional local markdown or JSON helper artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses structured reading passes, adapter routing, evidence checklists, and optional standard-library Python scripts to scaffold notes, paper maps, notation tables, claim matrices, limitation ledgers, and final markdown notes.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
