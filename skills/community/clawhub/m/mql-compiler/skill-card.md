## Description:

Compile MQL4 (.mq4) and MQL5 (.mq5) sources to .ex4/.ex5 on Linux with the mql-compiler command, and read its compile errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to compile MQL4 and MQL5 source files on Linux and inspect compiler diagnostics without a Windows environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs remote code, and system-wide installation can run it as root.

Mitigation: Review the installer and removal instructions before installing; understand the commands and privilege level before running them.

Risk: Removing the compiler cache can delete toolchain data shared by all users on the machine.

Mitigation: Review removal instructions and confirm the shared cache can be removed before deleting it.

Risk: Security scanning was partial because some local path-like references could not be resolved.

Mitigation: Review the referenced installation and removal material before use, since the scan does not cover every referenced item.

## Reference(s):

- [Project homepage](https://github.com/psyb0t/docker-mql-compiler)
- [Installation and removal guide](references/installation.md)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/mql-compiler)

## Skill Output:

**Output Type(s):** [Files, Text, Code]

**Output Format:** [Compiled .ex4/.ex5 files and JSON Lines diagnostics by default, with optional text or GNU output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compiled files are written next to their source files.]

## Skill Version(s):

0.5.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
