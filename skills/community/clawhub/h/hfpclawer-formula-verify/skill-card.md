## Description:

Verify LaTeX formulas via a multi-layer cross-validation pipeline: SymPy roundtrip, Wolfram CAS comparison, and dimensional consistency, with support for single FID and batch verification with LaTeX report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, engineers, developers, and physics modelers use this skill to check LaTeX formulas for syntax, algebraic consistency, and dimensional consistency before publication or implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and invokes the broader hfpclawer research CLI, not only the formula verification commands.

Mitigation: Install it only when the full hfpclawer CLI is acceptable for the environment, and review available commands before use.

Risk: Optional Zotero, LLM, graph, and scholarly API integrations can introduce additional data flows.

Mitigation: Enable only the integrations intentionally needed for the workflow, and keep private API, Zotero, profile, and local configuration values outside shared files.

Risk: The tool may create or update local configuration, registry data, profiles, and generated reports.

Mitigation: Review the configured storage locations and generated LaTeX reports before sharing or committing outputs.

Risk: Unpinned one-off CLI launches can run an unexpected package version.

Mitigation: Pin uvx or tool-run invocations to the intended hfpclawer version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/hfpclawer-formula-verify)
- [hfpclawer project homepage](https://github.com/diamond2nv/hfpapers-crawler)
- [hfpclawer PyPI package](https://pypi.org/project/hfpclawer/)
- [Wolfram Engine](https://www.wolfram.com/engine/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local config, formula registry entries, verification runs, and LaTeX report files.]

## Skill Version(s):

0.19.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
