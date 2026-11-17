## Description:

Build and use a modular paper contribution helper from target papers, research fields, years, and paper sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Researchers, paper authors, and research-support agents use this skill to package a paper's contribution, diagnose novelty risk, prepare reviewer defenses, and build portable helper skills from reference papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full papers, reviews, replies, and an API credential to a configurable LLM endpoint.

Mitigation: Use only trusted LLM endpoints, verify OPENAI_API_BASE before use, and avoid untrusted command or acpx backends.

Risk: The skill reads and writes project files and generated helper-skill outputs in the workspace.

Mitigation: Run it in a controlled workspace and review generated reports, JSON records, and skill packages before reuse or distribution.

Risk: The skill enforces a fixed first assistant response before normal task routing begins.

Mitigation: Treat the first response as a mode-selection prompt and confirm the intended workflow before relying on substantive analysis.

## Reference(s):

- [Module Index](references/module_index.md)
- [Context Loading Policy](references/context_loading_policy.md)
- [Build Workflow](references/build_workflow.md)
- [Project Corpus Direct Workflow](references/project_corpus_direct_workflow.md)
- [Assistant Local Deep Read Workflow](references/assistant_local_deep_read_workflow.md)
- [Source Modes](references/source_modes.md)
- [Target Domain Inference](references/target_domain_inference.md)
- [Reviewer Attack Taxonomy](references/report_playbook/reviewer_attack_taxonomy.md)
- [Rebuttal Pattern Library](references/report_playbook/rebuttal_pattern_library.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON/JSONL records, generated skill files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local paper corpora and write analysis artifacts or generated helper-skill packages in the workspace.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
