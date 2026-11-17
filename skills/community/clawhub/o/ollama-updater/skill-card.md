## Description:

Ollama Updater helps agents install or update Ollama with resumable downloads, automatic retries, progress display, old-version cleanup, and GPU detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newolf20000](https://clawhub.ai/user/newolf20000)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to install or update Ollama on Linux or macOS, especially when large downloads may be interrupted. It is intended for environments where resumable downloads and retry behavior reduce failed installs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater may require privileged execution and can make system-wide changes, including installing files, creating or modifying services, and changing users or groups.

Mitigation: Review the packaged shell script before running it, execute it only on systems where those changes are acceptable, and avoid sudo unless system-wide installation is intended.

Risk: Mutable main-branch install URLs can change after review.

Mitigation: Prefer the packaged ClawHub artifact or a pinned release source rather than a raw main-branch URL.

Risk: GPU driver and kernel-module installation paths can affect host stability.

Mitigation: Confirm GPU driver changes are desired, review distribution-specific package actions, and be prepared to reboot or roll back if driver installation is attempted.

Risk: Old Ollama installation paths may be removed during update.

Mitigation: Inspect or back up existing Ollama installation and data paths before running update or uninstall commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newolf20000/skills/ollama-updater)
- [Ollama](https://ollama.com)
- [Ollama official install script](https://ollama.com/install.sh)
- [NVIDIA CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and shell script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged installation commands and environment-variable configuration such as OLLAMA_VERSION.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
