## Description:

Guides agents in checking, generating, and combining public holiday calendars for countries and subdivisions with the Python holidays package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yting27](https://clawhub.ai/user/yting27)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to answer public-holiday questions, generate holiday calendars, filter date ranges by government-designated holidays, and combine official dates with user-provided custom holidays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Python packages into an active interpreter can alter the environment or conflict with system packages.

Mitigation: Use a dedicated virtual environment and prefer a reviewed, pinned holidays package version.

Risk: Custom holiday files can expose unintended local paths or untrusted file contents if loaded without user intent.

Mitigation: Load custom holiday files only when the user explicitly provides the path, verify the file exists, and skip custom dates when no path is provided.

## Reference(s):

- [ClawHub Global Holidays skill page](https://clawhub.ai/yting27/skills/global-holidays)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include holiday names, date lists, package installation commands, and user-provided custom holiday merge guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
