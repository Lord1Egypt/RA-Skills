## Description: <br>
Summarize GitHub Actions matrix job failures across runs so you can spot unstable OS/runtime axes fast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to analyze exported GitHub Actions run JSON, group repeated matrix failures, and identify unstable workflow axes for triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RUN_GLOB can select unintended local GitHub Actions export files. <br>
Mitigation: Review RUN_GLOB before use and point it only at run JSON exports intended for analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-failure-matrix) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local GitHub Actions run JSON exports selected by RUN_GLOB and optional filter environment variables.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
