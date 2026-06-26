## Description: <br>
Deconstructs psychology paper Results sections across common study designs using a study-profile-first workflow, adaptive A-I branch rules, source verification, causal-language guardrails, presentation guidance, and optional writer-transfer packets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin77-chris](https://clawhub.ai/user/bin77-chris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, analysts, and academic writers use this skill to inspect pasted Results text, PDF-derived excerpts, figure captions, tables, or screenshots from psychology papers and turn them into source-tagged Markdown analyses. It helps explain result structure, statistical reporting, figure narratives, interpretation boundaries, presentation scripts, and reusable writing patterns while preserving uncertainty where the paper evidence is incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to process user-selected PDFs and paper excerpts that may contain confidential or sensitive research material. <br>
Mitigation: Use uploaded or clearly selected non-confidential PDFs where possible, confirm the intended source material before analysis, and avoid providing documents the agent should not inspect. <br>
Risk: The skill relies on local PDF extraction and file-writing behavior, which can create Markdown outputs and temporary files on disk. <br>
Mitigation: Review the output directory before execution, confirm where files will be written, and check cleanup behavior for long or phased analyses. <br>
Risk: The security summary flags broad local PDF access and shell-based PDF extraction without strong user-control boundaries. <br>
Mitigation: Run the skill only in a workspace where local file access is appropriate, limit inputs to explicitly chosen paper files, and review generated analysis before using it for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bin77-chris/paper-results-reverse-engineer) <br>
- [Prompt templates](references/prompt-templates.md) <br>
- [Function labels](references/function-labels.md) <br>
- [Examples](references/examples.md) <br>
- [Execution constraints](docs/execution-constraints.md) <br>
- [Source verification](docs/source-verification.md) <br>
- [Causal language guardrails](docs/causal-language-guardrails.md) <br>
- [Experimental, survey, RCT, developmental, psychometric, and neuroimaging branch rules](docs/branch-a-b-c-d-e-f.md) <br>
- [Meta-analysis branch rules](docs/branch-g-meta-analysis.md) <br>
- [Qualitative branch rules](docs/branch-h-qualitative.md) <br>
- [Simulation branch rules](docs/branch-i-simulation.md) <br>
- [Module H writer transfer packet specification](docs/module-h-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown analysis files with source tags, tables, checklists, presentation scripts, and concise chat summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File-first workflow; standard mode is the default, with quick and close-reading modes available when requested.] <br>

## Skill Version(s): <br>
3.0.4 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
