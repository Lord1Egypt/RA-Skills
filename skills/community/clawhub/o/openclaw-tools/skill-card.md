## Description:

Search and discover OpenClaw skills from various sources for users who want to find available skills, search for specific functionality, or discover new skills to install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-liu-lang](https://clawhub.ai/user/mr-liu-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to locate available skills across ClawHub, directories, marketplaces, GitHub, and community sources before deciding what to install or evaluate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples use unpinned npx commands for the ClawHub CLI, which can execute the currently resolved package version.

Mitigation: Use a verified local ClawHub install or pin the clawhub package to a reviewed version before running examples in sensitive workspaces.

Risk: Installing skills from discovery sources can introduce unreviewed third-party instructions into an agent workspace.

Mitigation: Read each discovered skill's documentation and test new skills in isolation before production or sensitive use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-liu-lang/skills/openclaw-tools)
- [ClawHub](https://clawhub.com)
- [OpenClaw Directory skills](https://www.openclawdirectory.dev/skills)
- [LobeHub Skills Marketplace](https://lobehub.com/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides search strategies, source links, installation evaluation tips, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
