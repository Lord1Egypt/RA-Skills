## Description: <br>
Parallel file download and optional tar extraction using the pget CLI for single URLs or multifile manifests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelvincai522](https://clawhub.ai/user/kelvincai522) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate pget installation, download, extraction, and multifile manifest commands for high-throughput file transfer workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a CLI binary with elevated privileges can place unverified code on the system. <br>
Mitigation: Prefer package-manager installation when available, or verify the release source and checksum when possible; avoid sudo unless system-wide installation is required. <br>
Risk: Downloads, tar extraction, manifest destination paths, and --force can write or overwrite user-controlled filesystem locations. <br>
Mitigation: Review URLs, destination paths, extraction targets, and overwrite flags before executing generated pget commands. <br>


## Reference(s): <br>
- [pget CLI reference](references/pget.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for pget installation, single-file downloads, tar extraction, and multifile manifests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
