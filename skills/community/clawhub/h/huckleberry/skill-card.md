## Description:

Track baby sleep, feeding, diapers, and growth via the Huckleberry CLI. Use when the user asks about logging baby activities, starting/stopping sleep, bottle feeding, diaper changes, or growth measurements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayhickey](https://clawhub.ai/user/jayhickey)

### License/Terms of Use:


## Use Case:

External users and caregivers use this skill to get CLI commands for logging baby sleep, feeding, diaper, and growth events in Huckleberry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unofficial unpinned CLI.

Mitigation: Install the CLI in an isolated environment such as pipx or a virtualenv, consider pinning a reviewed package version, and do not run the install or CLI with administrator privileges.

Risk: The CLI may handle sensitive Huckleberry account credentials.

Mitigation: Prefer interactive login or a credential manager over exported passwords, and avoid putting Huckleberry credentials in shell startup files or shared scripts.

## Reference(s):

- [Huckleberry](https://huckleberrycare.com/)
- [huckleberry-api](https://github.com/Woyken/py-huckleberry-api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Huckleberry CLI commands and credential setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
