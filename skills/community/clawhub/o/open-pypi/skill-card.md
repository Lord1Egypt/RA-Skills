## Description:

Open the Python Package Index (PyPI) in Brave. Use when the user asks to use PyPI for this purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to open the Python Package Index in Brave, reuse an appropriate existing browser tab or session, and confirm the PyPI page is visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can focus or reuse an existing Brave session while navigating to PyPI.

Mitigation: Review browser context before use and rely on the skill's scope to open only PyPI and verify the destination.

Risk: A login page or account prompt could appear during browser navigation.

Mitigation: Stop at authentication prompts and do not enter passwords, authentication codes, API keys, payment details, or other credentials.

## Reference(s):

- [PyPI](https://pypi.org/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-pypi)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown instructions with YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens PyPI in Brave, reuses an appropriate existing tab or session when available, and stops before credential or account actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
