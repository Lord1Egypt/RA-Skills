## Description: <br>
Installs, launches, and uninstalls Linux desktop apps by resolving the safest supported source first, then running a local helper CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baladoodle](https://clawhub.ai/user/baladoodle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Linux users use this skill to resolve, install, launch, and uninstall desktop applications through supported package sources while seeing exact commands and higher-risk fallback labels before approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real Linux install, launch, and uninstall actions through local package tooling. <br>
Mitigation: Review the resolved source, package ID, and exact commands before approving any install or removal action. <br>
Risk: Some package sources may require sudo or package-manager bootstrap steps. <br>
Mitigation: Approve sudo prompts only when they match the requested application and expected package manager operation. <br>
Risk: Unreviewed community suggestions are not trusted install metadata. <br>
Mitigation: Keep unsafe community installs disabled unless the package source has been independently reviewed and the explicit unsafe opt-in is intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baladoodle/linux-installer) <br>
- [README.md](artifact/README.md) <br>
- [CATALOG_GUIDE.md](artifact/CATALOG_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes resolved package source, package ID, launch command, uninstall command, warnings, and confirmation requirements when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
