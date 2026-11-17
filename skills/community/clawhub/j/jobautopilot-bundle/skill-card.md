## Description:

Installs the full Job Autopilot pipeline for searching jobs, tailoring resumes, and submitting applications through the jobautopilot-search, jobautopilot-tailor, and jobautopilot-submitter skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerronl](https://clawhub.ai/user/jerronl)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-focused users use this bundle to install and configure an end-to-end OpenClaw workflow for job search, resume tailoring, and application submission. It is primarily an installer and setup helper for the three dependent Job Autopilot skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches or updates mutable dependent skills from the registry.

Mitigation: Review jobautopilot-search, jobautopilot-tailor, and jobautopilot-submitter before running install.sh, and run the bundle only when the publisher and current registry packages are trusted.

Risk: The setup script can overwrite an OpenClaw config path for special username input such as '.' or '..'.

Mitigation: Use a normal alphanumeric username and avoid '.' or '..' when setup prompts for the OpenClaw user.

Risk: The generated config stores personal, resume, and EEOC defaults that later automation may place into job applications.

Mitigation: Treat the config as sensitive, review values before application submission, and keep the generated file owner-readable only.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jerronl/skills/jobautopilot-bundle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs dependent skills, writes local user configuration, initializes tracker and handoff files, and prints setup guidance.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter lists 1.3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
