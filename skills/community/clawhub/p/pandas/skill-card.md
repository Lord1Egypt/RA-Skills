## Description: <br>
Analyze, transform, and clean DataFrames with efficient patterns for filtering, grouping, merging, and pivoting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill for Python tabular data work, including DataFrame cleaning, filtering, grouping, merging, pivoting, and exports. It also helps agents initialize and maintain local user preferences for pandas guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores preference and context memory locally at ~/pandas/memory.md. <br>
Mitigation: Review, edit, or delete ~/pandas/memory.md if stored information should not be reused across sessions. <br>
Risk: Generated pandas guidance or code may transform data incorrectly if assumptions about columns, missing values, or merge keys are wrong. <br>
Mitigation: Validate row counts, missing-value handling, and merge constraints before relying on transformed results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/pandas) <br>
- [Pandas skill homepage](https://clawic.com/skills/pandas) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local preference memory at ~/pandas/memory.md; no external upload behavior is described.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
