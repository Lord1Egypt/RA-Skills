## Description:

Launch unpacked Codex Desktop builds with debug ports and optional SSH host autostart using launch_codex_unpacked.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivansslo](https://clawhub.ai/user/ivansslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to launch Codex Desktop from an unpacked app.asar with controlled inspect and remote debugging ports, optional SSH host autostart, and temporary artifact preservation for debugging or investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced launch_codex_unpacked.sh script is not present in the submitted artifact, and any local script with that name would run with broad access to Codex Desktop files and state.

Mitigation: Verify the exact launcher script before execution and install or run the skill only in a controlled debugging environment.

Risk: Auto-install behavior can make Homebrew-managed tool changes on the host.

Mitigation: Set AUTO_INSTALL_TOOLS=0 when host package changes are not acceptable.

Risk: SSH autostart can persist Codex state and patch the unpacked application bundle.

Mitigation: Avoid SSH autostart unless those persistent state and bundle modifications are acceptable for the debugging session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivansslo/skills/launch-codex-unpacked)
- [Server-resolved GitHub source](https://github.com/ivansslo/codex-web-ui/tree/main/skills/launch-codex-unpacked)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports app directory, user data directory, final command line, and whether SSH host mode was enabled.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
