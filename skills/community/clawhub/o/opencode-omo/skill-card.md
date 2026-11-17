## Description:

Turn coding requests into completed work. Plan with Prometheus, execute with Atlas, and iterate with Sisyphus in OpenCode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iisweetheartii](https://clawhub.ai/user/iisweetheartii)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run coding tasks through OpenCode and Oh-My-OpenCode workflows, including one-shot implementation, planning with Prometheus, and execution with Atlas through Sisyphus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may ask an agent to change code or run commands in a repository.

Mitigation: Run it only in the intended repository and review proposed diffs and commands before accepting changes.

Risk: The artifact references helper scripts that were not present in the submitted files.

Mitigation: Confirm any referenced helper scripts are available and trustworthy before relying on those commands.

## Reference(s):

- [Opencode Omo ClawHub page](https://clawhub.ai/iisweetheartii/skills/opencode-omo)
- [agent-selfie ClawHub integration](https://clawhub.org/skills/agent-selfie)
- [gemini-image-gen ClawHub integration](https://clawhub.org/skills/gemini-image-gen)
- [agentgram ClawHub integration](https://clawhub.org/skills/agentgram)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenCode, git, and clawhub command-line tools; no bundled executable code was present in the artifact.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
