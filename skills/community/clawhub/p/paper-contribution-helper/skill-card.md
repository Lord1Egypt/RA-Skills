## Description: <br>
Build and use a modular paper contribution helper from target papers, research fields, years, and paper sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and developer agents use this skill to analyze paper contribution framing, diagnose novelty risk, prepare reviewer defenses, and build portable helper skills from reference-paper corpora. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process confidential paper, review, or reply content through external or local LLM backends. <br>
Mitigation: Use local-file processing where possible, avoid external APIs for confidential unpublished work unless explicitly permitted, and review saved artifacts before sharing. <br>
Risk: Optional command and command-file provider paths can execute user-configured local commands. <br>
Mitigation: Use those provider paths only with trusted executables, controlled environment variables, and reviewed command templates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/c-narcissus/paper-contribution-helper) <br>
- [Module index](references/module_index.md) <br>
- [Build workflow](references/build_workflow.md) <br>
- [Project corpus direct workflow](references/project_corpus_direct_workflow.md) <br>
- [Current-assistant local deep-read workflow](references/assistant_local_deep_read_workflow.md) <br>
- [Generated skill contract](references/generated_skill_contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON/JSONL records, generated skill files, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local analysis artifacts, manifests, and packaged helper-skill files when invoked for corpus processing.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
