## Description:

Automatically highlight academic papers by 5 semantic categories - goal, motivation, method, results, contributions - to help you quickly skim a paper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yorch233](https://clawhub.ai/user/yorch233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and paper reviewers use this skill to preflight academic PDFs, select reusable sentences, and create semantically colored PDF highlights with optional summary notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PyMuPDF is installed without a pinned version in the setup instructions.

Mitigation: Pin PyMuPDF or use a reviewed lockfile before deploying the skill in controlled environments.

Risk: The highlighter writes output files and may overwrite paths selected with --output or --report-json.

Mitigation: Review output and report paths before execution, especially when using custom file paths.

Risk: Full-paper pre-reading can consume significant tokens on long or dense PDFs.

Mitigation: Run the documented preflight gate and continue only after the user confirms the estimated processing cost.

Risk: Documentation includes a few mismatched or deprecated note-mode examples.

Mitigation: Use the script's --help output as the source of truth for supported command-line options.

## Reference(s):

- [Paper Highlight Rules](references/highlight-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; highlighted PDF output and optional JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, uv, and PyMuPDF; writes a highlighted PDF by default and can write a JSON report when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
