## Description:

Write fast, memory-efficient numerical code with arrays, broadcasting, vectorization, and linear algebra.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to get practical NumPy guidance for array operations, broadcasting, vectorization, dtype selection, linear algebra, and numerical data manipulation in Python.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to save NumPy activation preferences and brief context in shared MAIN memory, while its privacy text also emphasizes local ~/numpy/ storage.

Mitigation: Make shared-memory use opt-in, keep saved context narrowly scoped to NumPy activation preferences, and remove it if the user declines or later asks to stop.

Risk: Local ~/numpy/ storage can retain user preferences, snippets, and workflow notes across sessions.

Mitigation: Store only information the user explicitly shares or asks to save, and keep the local memory file and snippets removable.

## Reference(s):

- [ClawHub NumPy skill page](https://clawhub.ai/ivangdavila/skills/numpy)
- [NumPy skill homepage](https://clawic.com/skills/numpy)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python code blocks and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local ~/numpy/ memory and snippets when the user opts in.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
