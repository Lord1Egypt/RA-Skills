## Description:

OpenClaw Memory OS helps agents capture, store, search, and recall local personal memories through a Node.js CLI and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to add local conversation memory, note collection, keyword search, and recall workflows to an agent. It is most appropriate when users want explicit local storage under their control and can review what is saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is installed from npm and security evidence recommends verifying the exact package version, tarball integrity, and matching source commit before installation.

Mitigation: Inspect the npm package before installing, compare it with the intended source, and test installation in a sandbox or isolated environment first.

Risk: Stored memories are local JSON files and should be treated as unencrypted local data.

Mitigation: Avoid storing secrets or regulated data, restrict file permissions on the memory directory, and place the memory directory on encrypted storage if confidentiality is required.

Risk: Broad collection paths or auto-trigger behavior can capture more information than intended.

Mitigation: Keep auto-trigger disabled unless reviewed, collect only narrow non-sensitive paths, and regularly inspect and delete unwanted memory files.

Risk: Artifact documentation contains inconsistent claims about versions and security behavior.

Mitigation: Use the ClawHub release metadata as the release version for this card and verify runtime behavior against the installed package before deployment.

## Reference(s):

- [OpenClaw Memory OS Homepage](https://github.com/ZhenRobotics/openclaw-memory-os)
- [OpenClaw Memory OS README](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/README.md)
- [OpenClaw Memory OS Security](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/SECURITY.md)
- [OpenClaw Memory OS npm Package](https://www.npmjs.com/package/openclaw-memory-os)
- [OpenClaw Memory OS ClawHub Page](https://clawhub.ai/zhenstaff/skills/openclaw-memory-os)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or query local JSON memory files through the OpenClaw Memory OS CLI when installed and invoked by the user or agent.]

## Skill Version(s):

0.1.21 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
