## Description:

Generates or updates tutorials from VHS tapes and Playwright specs with dual-tone markdown and GIF recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to create or refresh user-facing tutorials from terminal tapes and browser specs, including recorded GIFs and brief and detailed Markdown guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that tape-command validation can run commands from tutorial tapes on the local system.

Mitigation: Inspect every VHS Type command before validation, and run reviewed commands in a disposable, isolated project environment.

Risk: The security assessment calls for review of README update behavior and flags behavior outside the skill's stated tutorial-generation purpose.

Mitigation: Review README changes before applying them and confirm that updates affect only the intended demo content.

Risk: The security scan was partial, so it does not establish that the skill is safe.

Mitigation: Treat the security assessment as incomplete and defer installation until the remaining component and flagged behavior have been reviewed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-sanctum-tutorial-updates)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Markdown, GIF files]

**Output Format:** [Markdown tutorial files and animated GIF recordings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create brief project documentation and detailed book documentation, update a README demo section, and integrate generated tutorial assets.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
